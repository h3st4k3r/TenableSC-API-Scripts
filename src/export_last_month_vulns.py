#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Vulnerability Export Script (from environment config)

Extracts vulnerabilities from the past N days from Tenable.sc and exports them to CSV.
Configuration is pulled from environment variables set by main_controller.

Author: h3st4k3r
Version: 1.1
"""

import os
import requests
import time
import pandas as pd
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = os.environ.get("TENABLE_SC_URL") + "/rest/analysis"
api_key = os.environ.get("TENABLE_SC_APIKEY")
headers = {
    "x-apikey": api_key,
    "Content-Type": "application/json"
}

body = {
    "query": {
        "name": "",
        "description": "",
        "context": "",
        "createdTime": 0,
        "modifiedTime": 0,
        "groups": [],
        "type": "vuln",
        "tool": "vulndetails",
        "sourceType": "cumulative",
        "startOffset": 0,
        "endOffset": 1000,
        "filters": [
            {
                "filterName": "firstSeen",
                "operator": "=",
                "value": "0:30"
            },
            {
                "filterName": "repository",
                "operator": "=",
                "value": [
                    { "id": 1133 }
                ]
            }
        ]
    },
    "sourceType": "cumulative",
    "sortField": "severity",
    "sortDir": "desc",
    "columns": [
        { "name": "acceptedRiskComment" },
        { "name": "agentId" },
        { "name": "bid" },
        { "name": "checkType" },
        { "name": "cpe" },
        { "name": "crossReferences" },
        { "name": "cve" },
        { "name": "cvssV2BaseScore" },
        { "name": "cvssV2TemporalScore" },
        { "name": "cvssV2Vector" },
        { "name": "cvssV3BaseScore" },
        { "name": "cvssV3TemporalScore" },
        { "name": "cvssV3Vector" },
        { "name": "cvssV4BaseScore" },
        { "name": "cvssV4Supplemental" },
        { "name": "cvssV4ThreatScore" },
        { "name": "cvssV4ThreatVector" },
        { "name": "cvssV4Vector" },
        { "name": "description" },
        { "name": "dnsName" },
        { "name": "exploitEase" },
        { "name": "exploitFrameworks" },
        { "name": "exploitPredictionScoringSystemEpss" },
        { "name": "exploit" },
        { "name": "family" },
        { "name": "firstDiscovered" },
        { "name": "hostId" },
        { "name": "ipAddress" },
        { "name": "lastObserved" },
        { "name": "macAddress" },
        { "name": "nessusWebTests" },
        { "name": "netbiosName" },
        { "name": "patchPublicationDate" },
        { "name": "plugin" },
        { "name": "pluginModificationDate" },
        { "name": "pluginName" },
        { "name": "pluginOutput" },
        { "name": "pluginPublicationName" },
        { "name": "port" },
        { "name": "protocol" },
        { "name": "recastRiskComment" },
        { "name": "repository" },
        { "name": "riskFactor" },
        { "name": "scanAccuracy" },
        { "name": "score" },
        { "name": "securityEndOfLifeDate" },
        { "name": "seeAlso" },
        { "name": "severity" },
        { "name": "stepsToRemediate" },
        { "name": "stigSeverity" },
        { "name": "synopsis" },
        { "name": "thoroughTests" },
        { "name": "total" },
        { "name": "version" },
        { "name": "vulnPublicationDate" },
        { "name": "vulnerabilityPriorityRating" },
        { "name": "exportDate" }
    ],
    "type": "vuln"
}

def fetch_all_results():
    all_results = []
    offset = 0
    page_size = 1000
    total_records = None
    print("Starting vulnerability extraction...")
    while True:
        print(f"Requesting results from {offset} to {offset + page_size - 1}...")
        body["query"]["startOffset"] = offset
        body["query"]["endOffset"] = offset + page_size
        response = requests.post(url, headers=headers, json=body, verify=False)
        print(f"HTTP status: {response.status_code}")
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            break
        data = response.json()
        results = data.get("response", {}).get("results", [])
        print(f"Results obtained in this page: {len(results)}")
        if not results:
            print("No more results, ending pagination.")
            break
        all_results.extend(results)
        if total_records is None:
            total_records = int(data.get("response", {}).get("totalRecords", 0))
            print(f"Total records to extract: {total_records}")
        offset += page_size
        if offset >= total_records:
            print("All records have been extracted.")
            break
        time.sleep(1)
    print(f"Extraction complete. Total vulnerabilities extracted: {len(all_results)}")
    return all_results

def flatten_json_fields(results):
    for r in results:
        for field in r:
            if isinstance(r[field], dict) and "name" in r[field]:
                r[field] = r[field]["name"]
    return results

def convert_timestamps(results):
    time_fields = [
        "firstSeen", "lastSeen", "firstDiscovered", "lastObserved",
        "patchPublicationDate", "pluginPublicationDate", "pluginModificationDate",
        "vulnPublicationDate", "exportDate"
    ]
    for r in results:
        for field in time_fields:
            if field in r and isinstance(r[field], (int, float, str)):
                try:
                    ts = int(r[field])
                    r[field] = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
    return results

if __name__ == "__main__":
    try:
        user_input_repo = input("Enter repository ID (or press Enter to use default 1133): ").strip()
        user_input_days = input("Enter number of days to extract (default 30): ").strip()

        if user_input_repo:
            body["query"]["filters"][1]["value"][0]["id"] = int(user_input_repo)

        if user_input_days:
            body["query"]["filters"][0]["value"] = f"0:{int(user_input_days)}"

        results = fetch_all_results()
        results = flatten_json_fields(results)
        results = convert_timestamps(results)
        print(f"Total extracted results: {len(results)}")
        df = pd.DataFrame(results)
        print("DataFrame columns:")
        print(df.columns.tolist())
        df.to_csv("exportsc_vulns.csv", index=False)
        print("Export to exportsc_vulns.csv completed.")
    except Exception as e:
        print(f"[!] Error occurred: {e}")
