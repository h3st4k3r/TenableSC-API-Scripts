# TenableSC-API-Scripts

Scripts to interact with Tenable.sc via its REST API. Includes modules for extracting vulnerability data, downloading completed reports, extracting user and dashboard metadata, and a central launcher script to handle execution and configuration.

## Project Structure

* `main.py` — Unified launcher with internal config for API key and URL. Dispatches modules.
* `export_last_month_vulns.py` — Extracts vulnerabilities from the last 30 days.
* `download_completed_reports.py` — Downloads completed reports for a specific month.
* `extract_users.py` — Exports Tenable.sc user information to CSV.
* `extract_dashboards.py` — Exports dashboard metadata to JSON.

## Requirements

* Python 3.x
* `requests`
* `pandas`
* `urllib3`

Install dependencies:

```bash
pip install requests pandas urllib3
```

---

## 1. Vulnerability Export Tool

Extracts detailed vulnerability data from Tenable.sc, flattening nested fields and formatting timestamps, then exporting all results to a CSV.

### Features

* Authenticates using environment variables set by the main launcher
* Uses `vulndetails` query with a 30-day filter (`firstSeen = 0:30`)
* Handles pagination to extract all data
* Converts nested JSON fields like `severity`, `repository`, and `plugin` into plain strings
* Converts Unix timestamps to human-readable dates
* CSV output saved as `exportsc_vulns.csv`

### Run

```bash
python3 main.py vulns
```

---

## 2. Completed Reports Downloader

Fetches and downloads all reports with `Completed` status for a user-specified month/year. Organizes output and ensures enough disk space.

### Features

* Reads Tenable.sc config from environment variables
* Prompts user to enter year and month
* Downloads only if at least 500MB free space is available
* Skips files already present
* Saves results under: `./reportsResults/YYYY_MM/`

### Run

```bash
python3 main.py reports
```

You will be prompted:

```text
Enter the year (YYYY): 2025
Enter the month (1-12): 6
```

---

## 3. User Export Tool

Exports all users from Tenable.sc, including details like status, email, and last login date.

### Output

* CSV file: `tenable_users.csv`

### Run

```bash
python3 main.py users
```

---

## 4. Dashboard Metadata Extractor

Retrieves all dashboard metadata and saves the output in structured JSON format.

### Output

* JSON file: `dashboards_metadata.json`

### Run

```bash
python3 main.py dashboards
```

---

## Configuration

The script `main.py` contains the hardcoded configuration:

```python
TENABLE_SC_URL = "https://your-tenablesc-url.com"
TENABLE_SC_APIKEY = "accesskey=XXXXXXXXXXXXXX; secretkey=YYYYYYYYYYYYYY;"
```

These values are passed to other scripts via environment variables:

```python
os.environ["TENABLE_SC_URL"]
os.environ["TENABLE_SC_APIKEY"]
```

No external config files are needed.

---

## Adding More Modules

1. Create a new script that reads `os.environ["TENABLE_SC_URL"]` and `TENABLE_SC_APIKEY`.
2. Add its name to the dispatch block in `main.py`.
3. Use your own CLI prompts or parameters as needed.

---

## Author

**h3st4k3r**
