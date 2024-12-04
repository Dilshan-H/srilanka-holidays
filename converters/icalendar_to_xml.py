"""
This module provides a function to convert an iCalendar file to XML format.

Author: Dilshan-H (https://github.com/Dilshan-H)
License: MIT License
URL: https://github.com/Dilshan-H/srilanka-holidays
"""

# pylint: disable=import-error

import os
import sys
import xml.etree.ElementTree as ET
from icalendar import Calendar

XML_DIR_NAME = "xml"


def ics_to_xml(file_path):
    """
    Convert the prepared iCalendar file to XML format.

    Args:
        file_path (str): The path to the iCalendar file.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    root = ET.Element("CalendarEvents")

    for component in cal.walk():
        if component.name == "VEVENT":
            event = ET.SubElement(root, "Event")
            summary = ET.SubElement(event, "Summary")
            summary.text = str(component.get("summary"))
            description = ET.SubElement(event, "Categories")
            description.text = str(component.get("description"))
            start = ET.SubElement(event, "Start")
            start.text = str(component.decoded("dtstart"))
            end = ET.SubElement(event, "End")
            end.text = str(component.decoded("dtend"))

    tree = ET.ElementTree(root)

    xml_dir = os.path.abspath(
        os.path.join(os.curdir, os.pardir, "srilanka-holidays", XML_DIR_NAME)
    )
    os.makedirs(xml_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the XML file path
    xml_file_path = os.path.join(xml_dir, f"{file_name}.xml")

    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_xml(ics_file_path)
