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

| Project/App                                                             | Description                                                                        |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [Simple-Calendar](https://github.com/SimpleMobileTools/Simple-Calendar) | A simple calendar with events, tasks, customizable colors, widgets and no ads.     |
| [SriGuide](https://sri-guide.com/?utm_source=srilanka-holidays)         | Open-source web app offering practical, up-to-date tips for travelers in Sri Lanka |

\*Simple-Calendar has been deprecated and moved to **Fossify**: https://github.com/FossifyOrg/Calendar

Add your project/app here? [Contact us](https://srilanka-holidays.vercel.app).

## Why use this API/Data?

Generic holiday libraries often struggle to provide accurate Sri Lankan holiday information due to limited country-specific support, lunar-based observances, and changes introduced through official announcements. This project maintains verified data throughout years, ensuring that developers and users have access to reliable holiday information.

Just a couple more reasons:

- Reliable and accurate local data (see [Data Sources](#data-sources))
- Open-source and free to use
- Updated every year or when holiday changes are announced
- Available as both API and downloadable files [XML, JSON, CSV, ICS]
- Holiday categorizations (Public, Bank, Mercantile, Poya)

## API

<img width="1259" height="171" alt="SLH - Github Update Banner" src="https://github.com/user-attachments/assets/7de22014-a77c-4cf8-9228-c7ec1fa09a8b" />

### Live Service Stats

| Service         	| Status                                                                                  	|
|-----------------	|-----------------------------------------------------------------------------------------	|
| API             	| ![Cron job status](https://api.cron-job.org/jobs/8642056/c28a42b23c352e04/status-0.svg) 	|
| Admin Backend   	| ![Cron job status](https://api.cron-job.org/jobs/8638659/83d7697c7c985c0a/status-0.svg) 	|
| Veloz Connector 	| ![Cron job status](https://api.cron-job.org/jobs/8641700/b11f544bf24ffe45/status-0.svg) 	|



The API is live at https://holidays.sri-guide.com and ready for public use! Built with [FastAPI](https://fastapi.tiangolo.com/), it offers a modern, developer-friendly experience with robust features.

### API Features

- **Holiday Lists**: Retrieve holidays for any year or filter by month and type (public, poya, mercantile, bank).
- **Date Checker**: Check if a specific date is a holiday with detailed info (e.g., holiday name, type).
- **API Key Authentication**: Secure access using `X-API-Key` header.
- **Redis Caching**: Lightning-fast responses with cached data.
- **Interactive Docs**: Explore endpoints at `/docs` or `/redoc`.
- **Self-Host**: Deploy on your favorite platform

### Using the Public API

1. **Obtain an API Key**:
   - Contact us to [request a free API key](https://holidays.sri-guide.com)
   - Include your key in every request: `X-API-Key: your-key`.

2. **Explore Endpoints**:
   - **List Holidays**: `GET /api/v1/holidays?year=2025` (optional: `month`, `type`, `format=simple/full`)

     Example:

     ```curl
     curl -H "X-API-Key: your-key" https://holidays.sri-guide.com/api/v1/holidays?year=2025
     ```

   - **Check Date**: `GET /api/v1/check_holiday?year=2025&month=5&day=1`

     Example:

     ```curl
     `curl -H "X-API-Key: your-key" https://holidays.sri-guide.com/api/v1/check_holiday?year=2025&month=5&day=1
     ```

3. **Read the Docs**:
   - Visit https://holidays.sri-guide.com/docs for interactive Swagger UI or https://srilanka-holidays.vercel.app/redoc for ReDoc.

4. **Use Caching in Your App**:
   - Since holiday data is updated less frequently, consider caching responses in your application to reduce API calls and improve performance.

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

   ```env
   REDIS_HOST=your-redis-host.com
   REDIS_PORT=redis-port-number
   REDIS_PASSWORD=redis-password
   REDIS_USERNAME=redis-username
   API_KEYS=backup-key-hash-1,backup-key-hash-2,...
   ENV=DEV
   ```

   > `API_KEYS` is used as the backup key store in case of Redis authentication method failure. Only hashed keys should go in here as a comma-separated list. `ENV` must be set to `DEV` only on local development setups.

6. Store API KEYS in REDIS
   
   The API uses Redis for API key validation, usage counters, and a holiday cache. Use `Redis Insight` or the Redis CLI to store the API keys.

   1. API keys

      Each key is a Redis hash named after the SHA-256 hex digest of the key. The plaintext key is never stored.

      ```bash
      v3:key:<sha256_hex_of_api_key>
      active = "1"    # valid
               "0"    # revoked/suspended
      ```

      > All API keys must be properly hashed. Otherwise, the API will not recognize them.

      If you are using Redis CLI, you can set the key like this:

      ```bash
      KEY="your-secret-api-key"
      HASH=$(printf '%s' "$KEY" | sha256sum | cut -d' ' -f1)
      redis-cli HSET "v3:key:$HASH" active 1
      ```

      Revoke a key by setting `active` to `0`.

      ```bash
      redis-cli HSET "v3:key:$HASH" active 0
      ```

   2. Usage counters (written automatically)

      The API automatically tracks usage counts for each key in Redis. You do not need to set these manually.

      ```bash
      v3:usage:d:<YYYYMMDD>
      <first 16 chars of key hash>:<route template>  ->  request count
      ```

   3. Holiday cache (written automatically)

      The API caches holiday data in Redis for faster responses. You do not need to set these manually.

      ```bash
      holidays:<year> # string containing JSON for that year's holidays
      ```



7. Start app with:

   ```bash
   fastapi dev app.py
   ```

</details>

> [!NOTE]
> Please note that the API key management system and statistics dashboard are private internal components and are not publicly available on this repository.

## Direct Downloadable Files

From here you can download the list of holidays in several file formats and integrate with your applications directly without using the API.

### Tentative Holiday Data

This section provides tentative holiday data files, which are available for early implementation. While these datasets are sourced from official channels, they remain incomplete as the finalized holiday data is typically released by the government in the final months of the year. Currently, these holidays are offered only as downloadable ICS files, and the data in this section is not yet integrated into the API.

- **Year 2027 Tentative Holiday Data**

  Upcoming data will be posted here after verification.

  https://github.com/Dilshan-H/srilanka-holidays/Tentative-Holiday-Data/2027-Tentative.ics

  > Notes: Mercantile Holiday values are estimated from earlier holiday data and should not be considered confirmed.

  > **Source**: The Gazette of the Democratic Socialist Republic of Sri Lanka, Government Notifications: No. 2493/05 - Tuesday, June 16, 2026

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
- Department of Government Printing, Sri Lanka - https://www.documents.gov.lk/

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

## Citation

If these data files or this API are used in your project or research, please consider citing it as

```bibtex
@software{dilshan2023slhapi,
  author = {Dilshan-H},
  title  = {SLHAPI: Sri Lanka Holidays API and Data},
  year   = {2023},
  url    = {https://github.com/Dilshan-H/srilanka-holidays}
}
```
