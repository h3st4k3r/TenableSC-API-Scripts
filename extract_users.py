#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Users Extractor

This script retrieves all users from Tenable.sc and exports their details
into a CSV file. Useful for auditing or identity inventory.

Author: h3st4k3r
Version: 1.0
"""

import os
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = os.environ.get("TENABLE_SC_URL")
api_key = os.environ.get("TENABLE_SC_APIKEY")
headers = {
    "x-apikey": api_key,
    "Content-Type": "application/json"
}

def extract_users():
    print("Extracting users from Tenable.sc...")
    endpoint = f"{url}/rest/user"
    response = requests.get(endpoint, headers=headers, verify=False)
    if response.status_code != 200:
        print(f"Failed to retrieve users: {response.status_code}")
        return
    users = response.json().get("response", {}).get("usable", [])
    print(f"Users extracted: {len(users)}")
    df = pd.DataFrame(users)
    df.to_csv("tenable_users.csv", index=False)
    print("Exported users to tenable_users.csv")

if __name__ == "__main__":
    extract_users()
