#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Vulnerability Export Script (from environment config)


Extracts vulnerabilities from the past N days from Tenable.sc and exports them to CSV.
Configuration is pulled from environment variables set by main_controller.


Author: h3st4k3r
Version: 1.2 (fixed __name__ issue and improved robustness)
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
"value": "0:30" # default, overridden in main()
},
{
"filterName": "repository",
"operator": "=",
"value": [
{"id": 1133} # default, overridden in main()
]
}
]
},
"sourceType": "cumulative",
"sortField": "severity",
"sortDir": "desc",
"columns": [
{"name": "acceptedRiskComment"},
{"name": "agentId"},
{"name": "bid"},
{"name": "checkType"},
{"name": "cpe"},
{"name": "crossReferences"},
{"name": "cve"},
{"name": "cvssV2BaseScore"},
{"name": "cvssV2TemporalScore"},
{"name": "cvssV2Vector"},
{"name": "cvssV3BaseScore"},
{"name": "cvssV3TemporalScore"},
{"name": "cvssV3Vector"},
{"name": "cvssV4BaseScore"},
{"name": "cvssV4Supplemental"},
{"name": "cvssV4ThreatScore"},
{"name": "cvssV4ThreatVector"},
{"name": "cvssV4Vector"},
{"name": "description"},
{"name": "dnsName"},
{"name": "exploitEase"},
{"name": "exploitFrameworks"},
{"name": "exploitPredictionScoringSystemEpss"},
{"name": "exploit"},
{"name": "family"},
{"name": "firstDiscovered"},
{"name": "hostId"},
{"name": "ipAddress"},
{"name": "lastObserved"},
{"name": "macAddress"},
{"name": "nessusWebTests"},
{"name": "netbiosName"},
{"name": "patchPublicationDate"},
{"name": "plugin"},
{"name": "pluginModificationDate"},
{"name": "pluginName"},
{"name": "pluginOutput"},
main()
