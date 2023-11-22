# pylint: disable=missing-docstring import-error

from typing import Union

from datetime import datetime, date
import json
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    id: float
    is_holiday: Union[bool, None] = None


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
async def api_coverage_year(year: int):
    """Return current data coverage in the API for a given year"""
    return {
        "coverage": "ok",
        "year": year,
        "total_holidays": 10,  # TODO: calculate number
        "last_updated": "2023-01-01",
    }  # TODO: change date


@app.get("/api/v1/check_holiday")
async def check_holiday(year: int, month: int, day: int, response: Response):
    """Return whether a given date is a holiday or not"""
    try:
        date_to_check = date(year, month, day)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "invalid date"}
    except TypeError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "invalid date format"}

    # open corresponding json file and check for date
    filename = f"json/{year}.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            holiday_data = json.load(file)
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"date": date_to_check, "error": "requested year not available"}

    for holiday in holiday_data:
        start_date = datetime.strptime(holiday["start"], "%Y-%m-%d").date()
        end_date = datetime.strptime(holiday["end"], "%Y-%m-%d").date()

        if start_date <= date_to_check < end_date:
            response.status_code = status.HTTP_200_OK
            return {
                "date": date_to_check,
                "response": True,
            }

    response.status_code = status.HTTP_200_OK
    return {"date": date_to_check, "response": False}


@app.get("/api/v1/holiday_info")
async def holiday_info(year: int, month: int, day: int, response: Response):
    """Return information about a given holiday"""
    try:
        date_to_check = date(year, month, day)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "invalid date"}
    except TypeError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "invalid date format"}

    # open corresponding json file and check for date
    filename = f"json/{year}.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            holiday_data = json.load(file)
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"date": date_to_check, "error": "requested year not available"}

    for holiday in holiday_data:
        start_date = datetime.strptime(holiday["start"], "%Y-%m-%d").date()
        end_date = datetime.strptime(holiday["end"], "%Y-%m-%d").date()

        if start_date <= date_to_check < end_date:
            response.status_code = status.HTTP_200_OK
            return {
                "date": date_to_check,
                "day": date_to_check.strftime("%A"),
                "week": date_to_check.strftime("%W"),
                "month": date_to_check.strftime("%B"),
                "is_holiday": True,
                "id": holiday["uid"],
                "holiday": holiday["summary"],
                "type": holiday["catagories"],
                "holiday_start": holiday["start"],
                "holiday_end": holiday["end"],
            }

    response.status_code = status.HTTP_200_OK
    return {
        "date": date_to_check,
        "is_holiday": False,
        "error": "date is not a holiday",
    }


@app.get("/api/v1/holidays")
async def holidays_list(item_id: int):
    """Return list of holidays for a given year/month"""
    return {"item_id": item_id}


# TEMP ROUTES
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
