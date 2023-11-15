# pylint: disable=missing-docstring import-error

import csv
import os
import sys
from icalendar import Calendar

CSV_DIR_NAME = "csv"


def ics_to_csv(file_path):
    """Convert the provided iCalendar file to CSV format"""
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    csv_dir = os.path.abspath(os.path.join(os.curdir, os.pardir, CSV_DIR_NAME))
    print(f"CSV files will be saved in {csv_dir}")
    os.makedirs(csv_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the CSV file path
    csv_file_path = os.path.join(csv_dir, f"{file_name}.csv")
    print(f"Saving CSV file to {csv_file_path}")

    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "UID",
            "Summary",
            "Catagories",
            "Start",
            "End",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for component in cal.walk():
            if component.name == "VEVENT":
                writer.writerow(
                    {
                        "UID": component.get("uid"),
                        "Summary": component.get("summary"),
                        "Catagories": component.get("description"),
                        "Start": component.decoded("dtstart"),
                        "End": component.decoded("dtend"),
                    }
                )


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_csv(ics_file_path)
