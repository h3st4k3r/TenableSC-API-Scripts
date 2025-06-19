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
