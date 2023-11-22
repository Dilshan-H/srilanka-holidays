# pylint: disable=missing-docstring import-error
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
    return {"message": "Hello World"}


@app.get("/api/v1/status")
async def api_status():
    """Return status of the API"""
    return {"status": "ok"}


@app.get("/api/v1/version")
async def api_version():
    """Return version of the API"""
    return {"version": "1.0.0"}  # TODO: change version


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


async def get_holiday_info(year: int, month: int, day: int):
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


@app.get("/api/v1/holidays")
async def holidays_list(item_id: int):
    """Return list of holidays for a given year/month"""
    return {"item_id": item_id}


# TEMP ROUTES
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: int):
    return {"item_name": item.name, "item_id": item_id}
