# Sri Lanka Holidays - API & Data

![GitHub license](https://img.shields.io/github/license/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Dilshan-H/srilanka-holidays?style=for-the-badge)

![GitHub stars](https://img.shields.io/github/stars/Dilshan-H/srilanka-holidays?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Dilshan-H/srilanka-holidays?style=for-the-badge)

![GitHub Workflow Status](https://github.com/Dilshan-H/srilanka-holidays/actions/workflows/convert_ics.yaml/badge.svg)
![API](https://img.shields.io/badge/api-red)
![csv](https://img.shields.io/badge/csv-blue)
![ics](https://img.shields.io/badge/ics-blue)
![json](https://img.shields.io/badge/json-blue)
![xml](https://img.shields.io/badge/xml-blue)

![Sri Lanka Holidays - Free API and Holiday Data](https://github.com/user-attachments/assets/2992203b-9a09-44d2-bca8-fece9aff129d)


## Description

An open-source API to get Sri Lankan holidays and a list of Sri Lankan holidays in several file formats for easy integration with your applications.

Holidays are updated every year and currently contains holidays starting from 2021.

## Powered Projects

| Project/App                                                             | Description                                                                    |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [Simple-Calendar](https://github.com/SimpleMobileTools/Simple-Calendar) | A simple calendar with events, tasks, customizable colors, widgets and no ads. |

\*Simple-Calendar has been deprecated and moved to **Fossify**: https://github.com/FossifyOrg/Calendar

## Why use this API/Data?

- Reliable and accurate local data (see [Data Sources](#data-sources))
- Open-source and free to use
- Updated every year
- Available as both API and downloadable files
- Holiday categorizations (Public, Bank, Mercantile, Poya, etc.)

## API

The API is live at https://srilanka-holidays.vercel.app and ready for public use! Built with [FastAPI](https://fastapi.tiangolo.com/), it offers a modern, developer-friendly experience with robust features.

### API Features

- **Holiday Lists**: Retrieve holidays for any year or filter by month and type (e.g., public, religious).
- **Date Checker**: Check if a specific date is a holiday with detailed info (e.g., holiday name, type).
- **API Key Authentication**: Secure access using `X-API-Key` header.
- **Redis Caching**: Lightning-fast responses with cached data.
- **Interactive Docs**: Explore endpoints at `/docs` or `/redoc`.
- **Self-Host**: Deploy on your favorite platform

### Using the Public API

1. **Obtain an API Key**:

   - Contact us to [request a key](https://srilanka-holidays.vercel.app)
   - Include your key in every request: `X-API-Key: your-key`.

2. **Explore Endpoints**:

   - **List Holidays**: `GET /api/v1/holidays?year=2025` (optional: `month`, `type`, `format=simple|full`)

     Example:

     ```curl
     curl -H "X-API-Key: your-key" https://srilanka-holidays.vercel.app/api/v1/holidays?year=2025
     ```

   - **Check Date**: `GET /api/v1/check_holiday?year=2025&month=5&day=1`

     Example:

     ```curl
     `curl -H "X-API-Key: your-key" srilanka-holidays.vercel.app/api/v1/check_holiday?year=2025&month=5&day=1
     ```

3. **Read the Docs**:

   - Visit `https://srilanka-holidays.vercel.app/docs` for interactive Swagger UI or `https://srilanka-holidays.vercel.app/redoc` for ReDoc.

4. **Homepage**:
   - Check out `https://srilanka-holidays.vercel.app` for an overview and quick start guide.

### Running & Testing API Locally

<details>
<summary>Click here to read more..</summary>

To test or contribute to the API, run it locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/sri-lanka-holidays-api.git
   cd sri-lanka-holidays-api
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows:venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements-api.txt
   ```

4. **Setup REDIS database**:

   Visit [Redis Cloud](https://cloud.redis.io) and login to your account. Then make a new database and make a note of your db's REDIS CONNECT URL.

   OR

   If you're using [Vercel](https://vercel.com/), check `Storage` dashboard to connect Redis directly.

5. **Configure Environment Variables**:

   Create a .env file with your variables.
   (Please note that API_KEYS mention here will contain FALLBACK API KEYS just in case if REDIS fails)

   ```env
   REDIS_URL=redis://default:your-password@your-redis-host:port
   API_KEYS=test-key-123,prod-key-456
   ```

6. Store API KEYS in REDIS
   Use `Redis Insight` to quickly store data as JSON.

   ```json
   {
     "api_keys": [
       {
         "key": "API_KEY",
         "created": 1749841807,
         "username": "USERNAME",
         "description": "DESCRIPTION"
       }
     ]
   }
   ```

7. Start app with:

   ```bash
   fastapi dev main.py
   ```

</details>

## Direct Downloadable Files

From here you can download the list of holidays in several file formats and integrate with your applications directly without using the API.

### [NEW] Tentative Holiday Data

This section provides tentative holiday data files, which are available for early implementation. While these datasets are sourced from official channels, they remain incomplete as the finalized holiday data is typically released by the government in the final months of the year. Currently, these holidays are offered only as downloadable ICS files, and the data in this section is not yet integrated into the API.

- **Year 2026 Tentative Holiday Data**

  https://github.com/Dilshan-H/srilanka-holidays/Tentative-Holiday-Data/2026-Tentative.ics

  > Mercantile Holiday values are not accurate. 'Poya' category has been added for future release.

  > Source: The Gazette of the Democratic Socialist Republic of Sri Lanka, Government Notifications: No. 2438/22 - Tuesday, May 27, 2025

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

<a href="https://www.buymeacoffee.com/dilshanh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Got an idea? Found a bug? Feel free to [open an issue](https://github.com/Dilshan-H/srilanka-holidays/issues/new) or submit a pull request.

Fork the repository, make your changes and submit a pull request. It's that much easy! If you're not sure how to do that, here's a [guide](https://opensource.com/article/19/7/create-pull-request-github).

## License

**The MIT License**

This program is free software: you can redistribute it and/or modify it under the terms of the MIT License. See the [LICENSE](LICENSE) file for more details. Attribution is required by leaving the author name and license info intact.
