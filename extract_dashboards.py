#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Dashboards Extractor

This script retrieves all dashboards metadata from Tenable.sc.
Useful for auditing dashboard configurations and components.

Author: h3st4k3r
Version: 1.0
"""

import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = os.environ.get("TENABLE_SC_URL")
api_key = os.environ.get("TENABLE_SC_APIKEY")
headers = {
    "x-apikey": api_key,
    "Content-Type": "application/json"
}

def extract_dashboards():
    print("Extracting dashboards from Tenable.sc...")
    endpoint = f"{url}/rest/dashboard"
    response = requests.get(endpoint, headers=headers, verify=False)
    if response.status_code != 200:
        print(f"Failed to retrieve dashboards: {response.status_code}")
        return
    dashboards = response.json().get("response", {}).get("usable", [])
    print(f"Dashboards extracted: {len(dashboards)}")
    with open("dashboards_metadata.json", "w") as f:
        json.dump(dashboards, f, indent=4)
    print("Exported dashboards to dashboards_metadata.json")

if __name__ == "__main__":
    extract_dashboards()
