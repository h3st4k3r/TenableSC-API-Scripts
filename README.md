# TenableSC API Toolkit

Scripts to interact with Tenable.sc via its REST API. This toolkit includes modular components to extract vulnerability data, download reports, and fetch user and dashboard information. A centralized launcher script (`main.py`) handles configuration and execution.

## Project Structure

```

├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── src
    ├── download_completed_reports.py
    ├── export_last_month_vulns.py
    ├── extract_dashboards.py
    └── extract_users.py
```

## Requirements

- Python 3.x
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies used:

```
requests
pandas
urllib3
```

## Usage

The entry point for the toolkit is `main.py`. It includes the configuration for Tenable.sc and dispatches execution to the selected module.

### Configure the API (inside `main.py`)

```python
TENABLE_SC_URL = "https://your-tenablesc-url.com"
TENABLE_SC_APIKEY = "accesskey=XXXXXXXXXXXXXX; secretkey=YYYYYYYYYYYYYY;"
```

These values are exported via environment variables to be used by all modules.

### Run a module

From the project root:

```bash
python3 main.py vulns       # Export vulnerability data
python3 main.py reports     # Download completed reports (pdf-csv during period of time)
python3 main.py users       # Extract user data
python3 main.py dashboards  # Extract dashboard data
```

Each module handles its own logic, API calls, pagination, formatting, and output.

## Contributing

Feel free to fork and contribute. Focus areas for future improvement:

- Add unit tests with mock responses
- Implement logging instead of print statements
- Support `.env` or secure credential storage (optional)
- Dockerize execution (optional)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[h3st4k3r](https://github.com/h3st4k3r)
