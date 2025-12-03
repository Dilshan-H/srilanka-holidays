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

An open-source API that provides accurate Sri Lankan holiday data, offering a comprehensive list of public holidays in multiple file formats for easy integration into your applications.

Holidays are updated every year and currently contains holidays starting from 2021. All records are validated through manual inspection, No AI or scripts!

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

![Uptime Robot status](https://img.shields.io/uptimerobot/status/m801863984-21c7b9399c6e347151e59c53?up_message=Operational&down_message=Unavailable&style=for-the-badge&logo=supabase&logoColor=green&label=API%20Status)

The API is live at https://srilanka-holidays.vercel.app and ready for public use! Built with [FastAPI](https://fastapi.tiangolo.com/), it offers a modern, developer-friendly experience with robust features.

🔺 IMPORTANT: Version `v1.1.0` introduces breaking changes with partial backward compatibility.

- `/api/v1/status` now requires authentication.

- `/api/v1/holiday_info` now returns holidays for a given day as an array.

Please refer to the [release notes](https://github.com/Dilshan-H/srilanka-holidays/releases/latest) for detailed information.

### API Features

- **Holiday Lists**: Retrieve holidays for any year or filter by month and type (public, poya, mercantile, bank).
- **Date Checker**: Check if a specific date is a holiday with detailed info (e.g., holiday name, type).
- **API Key Authentication**: Secure access using `X-API-Key` header.
- **Redis Caching**: Lightning-fast responses with cached data.
- **Interactive Docs**: Explore endpoints at `/docs` or `/redoc`.
- **Self-Host**: Deploy on your favorite platform

### Using the Public API

1. **Obtain an API Key**:

   - Contact us to [request a free API key](https://srilanka-holidays.vercel.app)
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

   - Visit https://srilanka-holidays.vercel.app/docs for interactive Swagger UI or https://srilanka-holidays.vercel.app/redoc for ReDoc.

4. **Homepage**:
   - Check out https://srilanka-holidays.vercel.app for an overview and request a free API key.

### Running & Testing API Locally

<details>
<summary>Click here to read more..</summary>

To test or contribute to the API, run it locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Dilshan-H/srilanka-holidays.git
   cd srilanka-holidays
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows:venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup REDIS database**:

   Visit [Redis Cloud](https://cloud.redis.io) and login to your account. Then make a new database and make a note of your db's REDIS CONNECT URL.

   OR

   If you're using [Vercel](https://vercel.com/), check `Storage` dashboard to connect Redis directly.

5. **Configure Environment Variables**:

   Create a .env file with your variables.
   (Please note that API_KEYS mention here will contain FALLBACK API KEYS just in case if REDIS fails)

   ```env
   REDIS_HOST=your-redis-host.com
   REDIS_PORT=redis-port-number
   REDIS_PASSWORD=redis-password
   REDIS_USERNAME=redis-username
   API_KEYS=test-key-123,prod-key-456
   ```

6. Store API KEYS in REDIS
   Use `Redis Insight` to quickly store data as JSON. Add a new KEY with JSON as the data type. Name the key as `API_KEYS_V2` (you can use other names, but remember to update it in your code as well.)

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
   fastapi dev app.py
   ```

</details>

## Direct Downloadable Files

From here you can download the list of holidays in several file formats and integrate with your applications directly without using the API.

### Tentative Holiday Data

This section provides tentative holiday data files, which are available for early implementation. While these datasets are sourced from official channels, they remain incomplete as the finalized holiday data is typically released by the government in the final months of the year. Currently, these holidays are offered only as downloadable ICS files, and the data in this section is not yet integrated into the API.

- **Year 2027 Tentative Holiday Data**

  Upcoming data will be posted here after verification.

  > Notes: [Additional details/comments]

  > Source: [Data sources]

### iCalendar (ics) Format

|    Year     | Download Link                                                         |
| :---------: | --------------------------------------------------------------------- |
|    2021     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2021.ics |
|    2022     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2022.ics |
|    2023     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2023.ics |
|    2024     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2024.ics |
|    2025     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2025.ics |
|    2026     | https://github.com/Dilshan-H/srilanka-holidays/blob/main/ics/2026.ics |
| 2021 - 2026 | https://github.com/Dilshan-H/srilanka-holidays/releases/latest        |

### Other Formats

These files are generated automatically from the iCalendar files and are available in JSON, CSV, and XML formats.

| Format | Resource                                                      |
| ------ | ------------------------------------------------------------- |
| JSON   | https://github.com/Dilshan-H/srilanka-holidays/tree/main/json |
| CSV    | https://github.com/Dilshan-H/srilanka-holidays/tree/main/csv  |
| XML    | https://github.com/Dilshan-H/srilanka-holidays/tree/main/xml  |

If you're unable to download individual files, please visit the releases page [here](https://github.com/Dilshan-H/srilanka-holidays/releases/) to download specific versions or [download](https://github.com/Dilshan-H/srilanka-holidays/archive/refs/heads/main.zip) the source code as a zip file, which you can extract to find the data inside the respective folders.

## Data Sources

All the data is collected from verified and reliable sources within the Sri Lankan government. This usually involves the Ministry of Home Affairs, Department of Government Printing and the Gazette papers.

- State Ministry of Home Affairs, Sri Lanka - https://moha.gov.lk/
- Department of Government Printing, Sri Lanka - http://www.documents.gov.lk/

## Holiday Categorization

Holidays are divided into several categories based on the default categorization method of the Sri Lankan government.

The following categories are used:

- **Public Holidays**
- **Poya Holidays**
- **Bank Holidays**
- **Mercantile Holidays**

## Contributing

<a href="https://www.buymeacoffee.com/dilshanh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Got an idea? Found a bug? Feel free to [open an issue](https://github.com/Dilshan-H/srilanka-holidays/issues/new) or submit a pull request.

Fork the repository, make your changes and submit a pull request. It's that much easy! If you're not sure how to do that, here's a [guide](https://opensource.com/article/19/7/create-pull-request-github).

## License

**The MIT License**

This program is free software: you can redistribute it and/or modify it under the terms of the MIT License. See the [LICENSE](LICENSE) file for more details. Attribution is required by leaving the author name and license info intact.
