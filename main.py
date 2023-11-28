"""
Sri Lanka Holidays API

Main module for the API - V0.1.10
Author: Dilshan-H (https://github.com/Dilshan-H)
License: MIT License
URL: https://github.com/Dilshan-H/srilanka-holidays

API endpoints.
    - / (home page)
    - /api/v1/status (status of the API)
    - /api/v1/version (version of the API)
    - /api/v1/coverage/{year} (data coverage for a given year)
    - /api/v1/check_holiday (check whether a given date is a holiday or not)
    - /api/v1/holiday_info (information about a given holiday)
    - /api/v1/holidays (list of holidays for a given year/month)

Docs:
    - /docs (Swagger UI)
    - /redoc (ReDoc)
"""

# pylint: disable=import-error
from typing import Annotated
import os
from datetime import datetime, date
import json
from fastapi import FastAPI, Response, status, Path, Query


app = FastAPI()


@app.get("/")
async def root():
    """Return home page"""
    # TODO: deliver home page
    return {"response": "Under construction"}


@app.get("/api/v1/status")
async def api_status():
    """Return status of the API"""
    return {"status": "ok"}


@app.get("/api/v1/version")
async def api_version():
    """Return version of the API"""
    return {"version": "0.1.10"}


@app.get("/api/v1/coverage/{year}")
async def api_coverage_year(
    year: Annotated[int, Path(title="The year to be checked", ge=2000, le=3000)]
):
    """Return current data coverage in the API for a given year"""
    filename = f"json/{year}.json"
    # check if data exists
    if os.path.isfile(filename):
        return {
            "year": year,
            "coverage": "ok",
        }

    return {
        "year": year,
        "coverage": "data not available",
    }


@app.get("/api/v1/check_holiday")
async def check_holiday(
    year: Annotated[int, Query(ge=2000, le=3000)],
    month: Annotated[int, Query(ge=1, le=12)],
    day: Annotated[int, Query(ge=1, le=31)],
    response: Response,
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
    year: Annotated[int, Query(ge=2000, le=3000)],
    month: Annotated[int, Query(ge=1, le=12)],
    day: Annotated[int, Query(ge=1, le=31)],
    response: Response,
):
    """Return information about a given holiday"""
    date_provided, status_code, result = await get_holiday_info(year, month, day)
    if response:
        response.status_code = status_code
    return {"date": date_provided, "response": result}


@app.get("/api/v1/holidays")
async def holidays_list():
    """Return list of holidays for a given year/month"""
    return {"response": "Under construction"}


async def get_holiday_info(year: int, month: int, day: int):
    """Process provided date and return holiday information with status code"""
    try:
        date_to_check = date(year, month, day)
    except (ValueError, TypeError):
        return None, status.HTTP_400_BAD_REQUEST, {"error": "invalid date"}

    filename = f"json/{year}.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            holiday_data = json.load(file)
    except FileNotFoundError:
        return (
            date_to_check,
            status.HTTP_404_NOT_FOUND,
            {"error": "requested year not available"},
        )

    for holiday in holiday_data:
        start_date = datetime.strptime(holiday["start"], "%Y-%m-%d").date()
        end_date = datetime.strptime(holiday["end"], "%Y-%m-%d").date()

        if start_date <= date_to_check < end_date:
            return (
                date_to_check,
                status.HTTP_200_OK,
                {
                    "day": date_to_check.strftime("%A"),
                    "week": date_to_check.strftime("%W"),
                    "month": date_to_check.strftime("%B"),
                    "is_holiday": True,
                    "id": holiday["uid"],
                    "holiday": holiday["summary"],
                    "type": holiday["catagories"],
                    "holiday_start": holiday["start"],
                    "holiday_end": holiday["end"],
                },
            )

    return (
        date_to_check,
        status.HTTP_200_OK,
        {
            "is_holiday": False,
        },
    )
