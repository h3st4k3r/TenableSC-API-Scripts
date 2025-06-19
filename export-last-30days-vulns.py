#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Vulnerability Export Script

This script extracts vulnerability data from Tenable.sc over the past 30 days,
applies pagination, flattens nested fields (e.g. severity, plugin, repository),
and exports the results to a CSV file.

Author: h3st4k3r
Version: 1.0
"""

import requests
import time
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://XXXXXXXXXXXXX.com/rest/analysis"
headers = {
    "x-apikey": "accesskey=XXXXXXXXXXX; secretkey=XXXXXXXXXXXX",
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

results = fetch_all_results()
results = flatten_json_fields(results)
print(f"Total extracted results: {len(results)}")
df = pd.DataFrame(results)
print("DataFrame columns:")
print(df.columns.tolist())
df.to_csv("exportsc_vulns.csv", index=False)
print("Export to exportsc_vulns.csv completed.")
