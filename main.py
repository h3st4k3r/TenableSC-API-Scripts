#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc API Script Launcher (Hardcoded Configuration with src/ layout)

Executes specific modules depending on command-line arguments.
The API URL and key are defined directly in this file and made available
via environment variables for other scripts to access.

Author: h3st4k3r
"""

import argparse
import os
import sys

# Hardcoded configuration (safe values for repo)
TENABLE_SC_URL = "https://your-tenablesc-url.com"
TENABLE_SC_APIKEY = "accesskey=XXXXXXXXXXXXXX; secretkey=YYYYYYYYYYYYYY;"

# Export config for downstream scripts to access
os.environ["TENABLE_SC_URL"] = TENABLE_SC_URL
os.environ["TENABLE_SC_APIKEY"] = TENABLE_SC_APIKEY

# Add src directory to sys.path for module resolution
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, SRC_PATH)

# Entry point dispatcher
def main():
    parser = argparse.ArgumentParser(description="Tenable.sc Script Controller")
    parser.add_argument(
        "module",
        choices=["vulns", "reports", "users", "dashboards"],
        help="Module to run: 'vulns', 'reports', 'users', or 'dashboards'"
    )
    args = parser.parse_args()

    if args.module == "vulns":
        import export_last_month_vulns
        export_last_month_vulns.main(repo_id=1133, days=30)
    elif args.module == "reports":
        import download_completed_reports
    elif args.module == "users":
        import extract_users
    elif args.module == "dashboards":
        import extract_dashboards
    else:
        print("[ERROR] Unknown module.")
        sys.exit(1)

if __name__ == "__main__":
    main()
