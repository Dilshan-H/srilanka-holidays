# Sri Lanka Holidays - API & Data

![GitHub license](https://img.shields.io/github/license/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Dilshan-H/srilanka-holidays?style=for-the-badge)

<!-- ![GitHub stars](https://img.shields.io/github/stars/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Dilshan-H/srilanka-holidays?style=for-the-badge) -->

![GitHub Workflow Status](https://github.com/Dilshan-H/srilanka-holidays/actions/workflows/convert_ics.yaml/badge.svg)

## Description

An open-source API to get Sri Lankan holidays and a list of Sri Lankan holidays in several file formats for easy integration with your applications.
Holidays are updated every year and currently contains holidays starting from 2021.

## Powered Projects

| Project/App                                                             | Description                                                                    |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [Simple-Calendar](https://github.com/SimpleMobileTools/Simple-Calendar) | A simple calendar with events, tasks, customizable colors, widgets and no ads. |

## Why use this API/Data?

- Reliable and accurate local data (see [Data Sources](#data-sources))
- Open-source and free to use
- Updated every year
- Available as both API and downloadable files
- Holiday categorizations (Public, Bank, Mercantile, Poya, etc.)

## API

API is under development and will be available soon for public use.  
If you want to use/try the current unstable version of the API, feel free to do so by forking the repository and running the API locally. API is built using [FastAPI](https://fastapi.tiangolo.com/) and dependencies can be installed using `pip install -r requirements.txt` within a virtual environment.

API Docs & testing features will be available at `http://localhost:8000/docs` and `http://localhost:8000/redoc` after running the API.

## Direct Downloadable Files

From here you can download the list of holidays in several file formats and integrate with your applications directly without using the API.

### iCalendar (ics) Format

|    Year     | Download Link                                                                              |
| :---------: | ------------------------------------------------------------------------------------------ |
|    2021     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2021.ics                      |
|    2022     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2022.ics                      |
|    2023     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2023.ics                      |
|    2024     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2024.ics                      |
|    2025     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2025.ics                      |
| 2021 - 2025 | https://github.com/Dilshan-H/srilanka-holidays/releases/download/ics-2021-25/2021-2025.ics |

### Other Formats

These files are generated automatically from the iCalendar files and are available in JSON, CSV, and XML formats.

| Format | Resource                                                      |
| ------ | ------------------------------------------------------------- |
| JSON   | https://github.com/Dilshan-H/srilanka-holidays/tree/main/json |
| CSV    | https://github.com/Dilshan-H/srilanka-holidays/tree/main/csv  |
| XML    | https://github.com/Dilshan-H/srilanka-holidays/tree/main/xml  |

## Data Sources

All the data is collected from verified and reliable sources within the Sri Lankan government. This usually involves the Ministry of Home Affairs, Department of Government Printing and the Gazette papers.

- State Ministry of Home Affairs, Sri Lanka - https://moha.gov.lk/
- Department of Government Printing, Sri Lanka - http://www.documents.gov.lk/

## Holiday Categorization

Holidays are divided into several categories based on the default categorization method of the Sri Lankan government.

The following categories are used:

- **Public Holidays** - Holidays that are celebrated by the general public including poya days.
- **Bank Holidays**
- **Mercantile Holidays**

## Contributing

Got an idea? Found a bug? Feel free to [open an issue](https://github.com/Dilshan-H/srilanka-holidays/issues/new) or submit a pull request.

Fork the repository, make your changes and submit a pull request. It's that much easy! If you're not sure how to do that, here's a [guide](https://opensource.com/article/19/7/create-pull-request-github).

## License

**The MIT License**

This program is free software: you can redistribute it and/or modify it under the terms of the MIT License. See the [LICENSE](LICENSE) file for more details. Attribution is required by leaving the author name and license info intact.
