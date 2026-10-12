"""
Sri Lanka Holidays API

Main module for the API
Author: Dilshan-H (https://github.com/Dilshan-H)
License: MIT License
URL: https://github.com/Dilshan-H/srilanka-holidays

API endpoints:
    [Frontend]
    ------------
    - /public (home page)

    [API - No Auth]
    ------------
    - /api/v1/health (health check - HEAD request)

    [API - With Auth]
    ------------
    - /api/v1/status (status of the API)
    - /api/v1/version (version of the API)
    - /api/v1/coverage (check data coverage for a given year)
    - /api/v1/check_holiday (check whether a given date is a holiday or not)
    - /api/v1/holiday_info (information about a given holiday)
    - /api/v1/holidays (list of holidays for a given year/month)

Docs:
    - /docs (Swagger UI)
    - /redoc (ReDoc)
"""

# pylint: disable=import-error
import hashlib
import json
import logging
import os
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from secrets import compare_digest
from typing import Annotated, Optional

import redis
import redis.asyncio as redis_asyncio
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
logger.info("Loading environment variables from .env file")
load_dotenv()

# Define API version
API_VERSION = "2.0.1"

# Define year limits
YEAR_MIN = 2021
YEAR_MAX = 2026

# Get fallback API keys from environment variables
FALLBACK_API_KEY_HASHES = os.getenv("API_KEYS", "").split(",")
# Initialize Redis client variable
REDIS_CLIENT = None
# Key usage TTL - 30D
USAGE_TTL = 30 * 86400

# Define API key header for authentication
api_key_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global REDIS_CLIENT
    try:
        REDIS_CLIENT = redis_asyncio.Redis(
            host=os.getenv("REDIS_HOST", ""),
            port=int(os.getenv("REDIS_PORT", 0)),
            decode_responses=True,
            username=os.getenv("REDIS_USERNAME", ""),
            password=os.getenv("REDIS_PASSWORD", ""),
        )
        await REDIS_CLIENT.ping()
        logger.info("Redis connection established successfully.")
    except redis.RedisError:
        logger.error("Failed to connect to Redis. Falling back to file reads.")
        REDIS_CLIENT = None
    yield
    if REDIS_CLIENT:
        await REDIS_CLIENT.close()


app = FastAPI(lifespan=lifespan)


async def verify_api_key(
    request: Request, key: Optional[str] = Depends(api_key_header_scheme)
):
    """Validate API key from Redis (V3) or fallback environment variables"""
    if not key:
        logger.warning("API key is missing in the request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Use 'X-API-Key' header with a valid key.",
        )

    # Hash the provided key for comparison
    key_hash = hashlib.sha256(key.encode()).hexdigest()

    # Check Redis if available
    redis_healthy = 0
    state = None
    if REDIS_CLIENT:
        try:
            state = await REDIS_CLIENT.hget(f"v3:key:{key_hash}", "active")
            redis_healthy = 1
        except Exception:
            logger.error("Auth backend failed")

    # Handle Redis response
    if isinstance(state, bytes):
        state = state.decode()
    if state == "1":
        try:
            # Route TEMPLATE (e.g. /items/{id}), never the raw path, so IDs can't explode the field count.
            route = getattr(request.scope.get("route"), "path", None) or "unknown"
            day_key = f"v3:usage:d:{datetime.now(timezone.utc):%Y%m%d}"
            pipe = REDIS_CLIENT.pipeline(transaction=False)
            pipe.hincrby(day_key, f"{key_hash[:16]}:{route[:80]}", 1)
            pipe.expire(day_key, USAGE_TTL)
            await pipe.execute()
        except Exception:
            logger.error("Failed to log usage")
        return key

    if state == "0":
        logger.warning("API key is suspended or revoked")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked API key. Use 'X-API-Key' header with a valid key.",
        )

    # Emergency fallback setup with environment variables
    if not REDIS_CLIENT or redis_healthy == 0:
        logger.warning(
            "Redis is unavailable, using fallback environment variables for API key validation"
        )
        # if no fallback keys OR fallback keys count is less than 3
        if not FALLBACK_API_KEY_HASHES or len(FALLBACK_API_KEY_HASHES) < 3:
            logger.warning(
                "Redis Failure: No fallback API keys found in environment variables"
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Sorry, we're experiencing some issues with the authentication backend. Please try again later.",
            )

        # Check hashed keys in fallback environment variables
        for fallback_key_hash in FALLBACK_API_KEY_HASHES:
            if compare_digest(fallback_key_hash, key_hash):
                logger.info("API key validated via fallback environment variables")
                return key

    logger.warning("Rejecting request with invalid API key")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or revoked API key. Use 'X-API-Key' header with a valid key.",
    )


async def get_holiday_info(year: int, month: int, day: int):
    """Process provided date and return holiday information with status code"""
    try:
        date_to_check = date(year, month, day)
    except (ValueError, TypeError):
        logger.error(
            "Invalid date provided: year=%s, month=%s, day=%s", year, month, day
        )
        return None, status.HTTP_400_BAD_REQUEST, {"error": "Invalid date provided"}

    cache_key = f"holidays:{year}"
    holiday_data = None

    # Try Redis cache
    if REDIS_CLIENT:
        try:
            logger.info("Checking Redis cache for %s", cache_key)
            holiday_data_cached = await REDIS_CLIENT.get(cache_key)
            if holiday_data_cached:
                logger.info("Cache hit for %s in Redis", cache_key)
                holiday_data = json.loads(holiday_data_cached)  # type: ignore
        except redis.RedisError:
            logger.error(
                "Redis cache failed for %s, falling back to file read", cache_key
            )
            pass
        except json.JSONDecodeError:
            logger.error("Failed to decode cached data for %s in Redis", cache_key)
            pass

    # If Redis cache is not available or no cache hit, read from file
    if holiday_data is None:
        logger.info(
            "No cache hit for %s, reading from file for year %s", cache_key, year
        )
        base_dir = Path("json")
        filename = base_dir / f"{year}.json"

        # Resolve the path to prevent directory traversal
        resolved_path = filename.resolve()

        # Ensure the resolved path is within the intended directory
        if not resolved_path.parent.samefile(base_dir.resolve()):
            logger.warning("Invalid file path received: %s", resolved_path)
            return (
                date_to_check,
                status.HTTP_400_BAD_REQUEST,
                {"error": "Invalid file path"},
            )

        try:
            with open(resolved_path, "r", encoding="utf-8") as file:
                holiday_data = json.load(file)
                # Cache in Redis with 24-hour TTL
                if REDIS_CLIENT:
                    try:
                        await REDIS_CLIENT.setex(
                            cache_key, 86400, json.dumps(holiday_data)
                        )
                        logger.info("Cached %s in Redis", cache_key)
                    except redis.RedisError:
                        logger.error("Failed to cache %s in Redis", cache_key)
                        pass  # Continue without caching if Redis fails
        except FileNotFoundError:
            logger.error("Data file not found for year %s", year)
            return (
                date_to_check,
                status.HTTP_404_NOT_FOUND,
                {"error": "Data for requested year not available"},
            )
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in file for year %s", year)
            return (
                date_to_check,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {
                    "error": "Invalid data format for requested year. Please notify the admin."
                },
            )

    # Process holiday data (from cache or file)
    matches = []
    for holiday in holiday_data:
        try:
            start_date = datetime.strptime(holiday["start"], "%Y-%m-%d").date()
            end_date = datetime.strptime(holiday["end"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            logger.warning("Invalid holiday entry detected: %s", holiday)
            continue  # Skip invalid holiday entries

        if start_date <= date_to_check < end_date:
            matches.append(
                {
                    "id": holiday.get("uid"),
                    "holiday": holiday.get("summary"),
                    "type": holiday.get("categories"),
                    "holiday_start": holiday.get("start"),
                    "holiday_end": holiday.get("end"),
                }
            )

    if matches:
        result = {
            "day": date_to_check.strftime("%A"),
            "week": date_to_check.strftime("%W"),
            "month": date_to_check.strftime("%B"),
            "is_holiday": True,
            "count": len(matches),
            "holidays": matches,
        }

        return date_to_check, status.HTTP_200_OK, result

    return date_to_check, status.HTTP_200_OK, {"is_holiday": False}


@app.head("/api/v1/health")
async def api_health_head():
    """Return status of the API (HEAD request)"""
    redis_healthy = False
    if REDIS_CLIENT:
        try:
            await REDIS_CLIENT.ping()
            redis_healthy = True
        except Exception:
            logger.warning("Health check: Redis ping failed")

    # if Redis is down and fallback key count is not greater than 2
    # Default 2 fallback keys: Dev key, Test key.
    if not redis_healthy and not len(FALLBACK_API_KEY_HASHES) > 2:
        logger.warning(
            "Health check failed: Redis down and no fallback API keys configured"
        )
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    # Canary check [Known Holiday]: 2025-02-04 - Sri Lanka National Day
    try:
        _, status_code, result = await get_holiday_info(2025, 2, 4)
    except Exception:
        logger.warning(
            "Health check failed: get_holiday_info raised an exception", exc_info=True
        )
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    if status_code != status.HTTP_200_OK or not result.get("is_holiday"):
        logger.warning(
            f"Health check failed: holiday API returned status={status_code}, "
            f"is_holiday => {result.get('is_holiday') if result else None}"
        )
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    logger.info("=== Health check passed ===")
    return Response(status_code=status.HTTP_200_OK)


@app.get("/api/v1/status")
async def api_status(
    api_key: str = Depends(verify_api_key),
):
    """Return status of the API"""
    return {
        "status": "ok",
        "api_version": API_VERSION,
        "API_Key_Validation": "successful",
        "timestamp": datetime.now().isoformat(),
        "redis_connected": REDIS_CLIENT is not None,
        "data_store_year_min": YEAR_MIN,
        "data_store_year_max": YEAR_MAX,
    }


@app.get("/api/v1/version")
async def api_version(
    api_key: str = Depends(verify_api_key),
):
    """Return version of the API"""
    return {
        "version": API_VERSION,
        "data_store_year_min": YEAR_MIN,
        "data_store_year_max": YEAR_MAX,
    }


@app.get("/api/v1/coverage")
async def api_coverage_year(
    year: Annotated[int, Query(ge=YEAR_MIN, le=YEAR_MAX)],
    api_key: str = Depends(verify_api_key),
):
    """Return current data coverage in the API for a given year"""
    base_dir = Path("json")
    filename = base_dir / f"{year}.json"

    # Resolve the path to prevent directory traversal
    resolved_path = filename.resolve()

    # Ensure the resolved path is within the intended directory
    if not resolved_path.parent.samefile(base_dir.resolve()):
        return {
            "year": year,
            "error": "Invalid file path",
        }

    # Check if the file exists
    if resolved_path.is_file():
        return {
            "year": year,
            "coverage": "ok",
        }

    return {
        "year": year,
        "coverage": "Data not available for requested year.",
    }


@app.get("/api/v1/check_holiday")
async def check_holiday(
    year: Annotated[int, Query(ge=YEAR_MIN, le=YEAR_MAX)],
    month: Annotated[int, Query(ge=1, le=12)],
    day: Annotated[int, Query(ge=1, le=31)],
    response: Response,
    api_key: str = Depends(verify_api_key),
):
    """Return whether a given date is a holiday or not"""
    date_provided, status_code, result = await get_holiday_info(year, month, day)
    if response:
        response.status_code = status_code
    if status_code != status.HTTP_200_OK:
        return {"response": result}
    if result["is_holiday"]:
        return {"date": date_provided, "response": True}
    return {"date": date_provided, "response": False}


@app.get("/api/v1/holiday_info")
async def holiday_info(
    year: Annotated[int, Query(ge=YEAR_MIN, le=YEAR_MAX)],
    month: Annotated[int, Query(ge=1, le=12)],
    day: Annotated[int, Query(ge=1, le=31)],
    response: Response,
    api_key: str = Depends(verify_api_key),
):
    """Return information about a given holiday"""
    date_provided, status_code, result = await get_holiday_info(year, month, day)
    if response:
        response.status_code = status_code
    return {"date": date_provided, "response": result}


@app.get("/api/v1/holidays")
async def holidays_list(
    year: Annotated[int, Query(ge=YEAR_MIN, le=YEAR_MAX)],
    response: Response,
    month: Annotated[Optional[int], Query(ge=1, le=12)] = None,
    type: Annotated[Optional[str], Query()] = None,
    format: Annotated[str, Query()] = "full",
    api_key: str = Depends(verify_api_key),
):
    """Return list of holidays for a given year or year/month, optionally filtered by type"""
    # Validate format
    if format not in ["simple", "full"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Invalid format. Use 'simple' or 'full'"}

    # Safely construct file path
    base_dir = Path("json")
    filename = base_dir / f"{year}.json"
    resolved_path = filename.resolve()

    # Ensure path is within json directory
    if not resolved_path.parent.samefile(base_dir.resolve()):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Invalid file path"}

    # Load holiday data
    try:
        with open(resolved_path, "r", encoding="utf-8") as file:
            holiday_data = json.load(file)
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Data for requested year not available"}
    except json.JSONDecodeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "error": "Invalid data format for requested year. Please notify the admin."
        }

    # Filter and format holidays
    result = []
    # Track seen dates when returning simple format to avoid duplicates
    seen_dates = set()
    for holiday in holiday_data:
        try:
            if "start" not in holiday or "end" not in holiday:
                continue  # Skip invalid holiday entries
            start_date = datetime.strptime(holiday["start"], "%Y-%m-%d").date()
            # Filter by month if provided
            if month and start_date.month != month:
                continue
            # Filter by type if provided
            if type and type.lower() not in [
                cat.lower() for cat in holiday.get("categories", [])
            ]:
                continue
            # Format output
            if format == "simple":
                # Avoid adding the same date multiple times
                if holiday["start"] in seen_dates:
                    continue
                seen_dates.add(holiday["start"])
                result.append(holiday["start"])
            else:
                result.append(
                    {
                        "date": holiday["start"],
                        "name": holiday["summary"],
                        "type": holiday["categories"],
                        "start": holiday["start"],
                        "end": holiday["end"],
                        "id": holiday["uid"],
                    }
                )
        except (ValueError, KeyError):
            continue  # Skip holidays with invalid data
    response.status_code = status.HTTP_200_OK
    return {"holidays": result}


@app.get("/privacy-policy", include_in_schema=False)
async def privacy_policy():
    """Redirect to privacy policy page"""
    return RedirectResponse(url="/privacy-policy.html", status_code=307)


@app.get("/terms-of-use", include_in_schema=False)
async def terms_of_use():
    """Redirect to terms of use page"""
    return RedirectResponse(url="/terms-of-use.html", status_code=307)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to home page"""
    return RedirectResponse(url="/index.html", status_code=307)


# Mount static files on dev server
if os.getenv("ENV") == "DEV":
    logger.info("Mounting static files for DEV environment")
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
