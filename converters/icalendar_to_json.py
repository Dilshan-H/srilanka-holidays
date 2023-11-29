"""
This module provides a function to convert an iCalendar file to JSON format.

Author: Dilshan-H (https://github.com/Dilshan-H)
License: MIT License
URL: https://github.com/Dilshan-H/srilanka-holidays
"""

# pylint: disable=import-error

import os
import sys
import json
from icalendar import Calendar

JSON_DIR_NAME = "json"


def ics_to_json(file_path):
    """
    Convert the prepared iCalendar file to JSON format.

    Args:
        file_path (str): The path to the iCalendar file.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    json_dir = os.path.abspath(
        os.path.join(os.curdir, os.pardir, "srilanka-holidays", JSON_DIR_NAME)
    )
    os.makedirs(json_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the JSON file path
    json_file_path = os.path.join(json_dir, f"{file_name}.json")

    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event = {
                "uid": component.get("uid"),
                "summary": component.get("summary"),
                "catagories": component.get("description").split(","),
                "start": component.decoded("dtstart").isoformat(),
                "end": component.decoded("dtend").isoformat(),
            }
            events.append(event)

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(events, json_file, indent=2)


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_json(ics_file_path)
