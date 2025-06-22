# TenableSC-API-Scripts
Scripts to connect to Tenable.sc using the REST API

# 1. Tenable.sc Vulnerability Export Tool

This script connects to Tenable.sc using the REST API and extracts vulnerability data for the last 30 days. It supports pagination, processes nested JSON fields (e.g., severity, repository, plugin), and exports all relevant fields to a CSV file.

## Features

- Connects to Tenable.sc using an API key
- Executes a `vulndetails` query scoped to the last 30 days
- Applies pagination to retrieve all matching records
- Flattens nested fields (e.g., `severity.name`) into plain values
- Exports full vulnerability details into a structured CSV format

## Requirements

- Python 3.x
- `requests`
- `pandas`
- `urllib3`

Install dependencies with:

```bash
pip install requests pandas urllib3
```

## Usage

1. Edit the script to configure the `url` and `x-apikey` headers with your Tenable.sc instance and credentials.
2. Run the script:

```bash
python3 export_last_month_vulns.py
```

![image](https://github.com/user-attachments/assets/2ef12413-2798-4c95-97b7-e965bc6cea8d)


![image](https://github.com/user-attachments/assets/f9466bfb-c6af-4f3d-92c6-524062c5fe52)


3. The script will:
   - Request all vulnerability data seen in the last 30 days
   - Flatten all JSON fields that include a `name` key (e.g., `severity`, `repository`)
   - Save the output to `exportsc_vulns.csv`

## Output

The resulting CSV file includes a full list of vulnerabilities with all exported fields, including:

- IP address
- Plugin name
- Severity (flattened as text)
- Repository (flattened as text)
- CVEs, BID, protocol, port
- CVSS metrics (v2/v3/v4)
- Description, synopsis, solution, etc.

## Notes

- This script uses `firstSeen = 0:30` as a dynamic filter to collect vulnerabilities first seen in the past 30 days.
- The query is scoped to a specific repository ID. Adjust it as needed.
- All data is exported to a single CSV file in the working directory.

## Author

h3st4k3r

# 2. Tenable.sc Completed Reports Downloader

This script connects to a Tenable.sc instance via its REST API to download all reports marked as `Completed` for a specified month and year.
Downloads are organized into folders by year and month, and redundant downloads are skipped. The script checks for minimum free disk space (500MB) before proceeding.

## Features

- Connects to Tenable.sc using API Key authentication
- Filters only reports with status `Completed`
- Asks the user to input year and month for filtering
- Automatically creates target folders in the structure `./reportsResults/YYYY_MM/`
- Prevents downloading files that already exist
- Verifies that at least 500MB of disk space is free before each download

## Requirements

- Python 3.x
- `requests`
- `urllib3`

You can install dependencies using:

```bash
pip install requests urllib3
```

## Usage

1. Open the script and set your Tenable.sc base URL and API key in the variables:
   - `url_base`
   - `api_key`

2. Run the script:

```bash
python3 download_completed_reports.py
```

3. Enter the desired **year** and **month** when prompted (e.g. `2025` and `6` for June 2025).

4. Reports will be saved under:

```
./reportsResults/2025_06/
```

## Notes

- The script avoids re-downloading any report whose filename already exists in the output directory.
- Disk space check prevents download if free space is lower than 500MB.
- If the report name contains special characters, they will be sanitized to ensure valid filenames.

## Author

h3st4k3r

