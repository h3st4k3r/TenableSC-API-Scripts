# TenableSC API Toolkit

This project provides a collection of Python scripts for interacting with **Tenable.sc** via its REST API. The toolkit allows security teams to extract vulnerabilities, download completed reports, retrieve user and dashboard metadata, and more.

---

## Project Structure

```
.
├── main.py                    # Main launcher script
├── requirements.txt           # Project dependencies
├── LICENSE                    # MIT License
├── README.md                  # This documentation file
├── src/                       # All functional modules
│   ├── export_last_month_vulns.py
│   ├── download_completed_reports.py
│   ├── extract_users.py
│   └── extract_dashboards.py
└── .github/workflows/         # GitHub Actions CI
    └── run-tests.yml
```

---

## Features

* Query Tenable.sc REST API
* Export vulnerabilities from the last 30 days
* Download completed reports by year and month
* Retrieve metadata on users and dashboards
* All modules are launched via a unified CLI controller (`main.py`)
* Simple environment-based configuration (no external secrets file required)

---

## Requirements

* Python 3.10+
* Modules:

  * `requests`
  * `pandas`
  * `urllib3`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run a module with:

```bash
python main.py <module>
```

Available modules:

* `vulns` — Export vulnerabilities from the last 30 days
* `reports` — Download completed reports for a user-defined month/year
* `users` — Retrieve all users and export to CSV
* `dashboards` — Retrieve all dashboards and export to CSV

### Example:

```bash
python main.py reports
```

Then provide input:

```
Enter the year (YYYY): 2025
Enter the month (1-12): 6
```

---

## Configuration

Edit `main.py` and set your Tenable.sc base URL and API key directly:

```python
TENABLE_SC_URL = "https://your-tenablesc-url.com"
TENABLE_SC_APIKEY = "accesskey=XXXXXXXXXXXXXX; secretkey=YYYYYYYYYYYYYY;"
```

These values are exported as environment variables and accessed in all `src/*.py` modules.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Created by **h3st4k3r** — Hacking, Cyber Intelligence && Threat Hunting tools | From the comunity to the comunity.
