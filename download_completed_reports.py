#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tenable.sc Completed Reports Downloader

This script connects to Tenable.sc and automatically downloads all completed reports
from a specified month and year. It ensures disk space availability, organizes
files by year/month, and avoids redundant downloads.

Author: h3st4k3r
Version: 1.0
"""

import os
import requests
import urllib3
import shutil
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = "https://XXXXXXXXXX.com"
api_key = "accesskey=XXXXXXX; secretkey=XXXXXXX;"
headers = {"x-apikey": api_key, "Content-Type": "application/json"}
MIN_FREE_BYTES = 500 * 1024 * 1024  # Minimum 500MB free space required

def has_sufficient_space(path="."):
    total, used, free = shutil.disk_usage(path)
    return free > MIN_FREE_BYTES

def get_completed_reports():
    url = f"{url_base}/rest/report"
    params = {
        "fields": "id,name,type,status,finishTime",
        "status": "Completed"
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code != 200:
        print(f"Error retrieving reports list: {response.status_code}")
        return []
    return response.json().get("response", {}).get("usable", [])

def download_report_result(report_id, report_name, report_type, finish_time):
    if finish_time:
        dt = datetime.fromtimestamp(int(finish_time))
    else:
        dt = datetime.now()
    month_folder = dt.strftime("%Y_%m")
    safe_report_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in report_name)
    base_path = os.path.join(os.getcwd(), "reportsResults", month_folder)
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, f"{safe_report_name}.{report_type}")
    if os.path.exists(file_path):
        print(f"Already exists: {file_path}, skipping download.")
        return
    url = f"{url_base}/rest/report/{report_id}/download?format={report_type}"
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Saved: {file_path}")
    else:
        print(f"Error downloading report {report_id}: {response.status_code}")
        print("Response:", response.text)

def download_reports_from_month(year, month):
    start_month = datetime(year, month, 1)
    start_epoch = int(start_month.timestamp())
    reports = get_completed_reports()
    print(f"Total completed reports found: {len(reports)}")
    for report in reports:
        finish_time = report.get("finishTime", "")
        if finish_time:
            dt = datetime.fromtimestamp(int(finish_time))
            if dt < start_month:
                continue
        else:
            continue
        if not has_sufficient_space():
            print("Insufficient disk space, stopping download to avoid saturation.")
            break
        report_id = report["id"]
        report_name = report["name"]
        report_type = report.get("type", "pdf")
        print(f"Downloading report {report_id} ({report_type})...")
        download_report_result(report_id, report_name, report_type, finish_time)

if __name__ == "__main__":
    try:
        user_year = int(input("Enter the year (YYYY): "))
        user_month = int(input("Enter the month (1-12): "))
        download_reports_from_month(user_year, user_month)
    except Exception as e:
        print(f"Invalid input or unexpected error: {e}")
