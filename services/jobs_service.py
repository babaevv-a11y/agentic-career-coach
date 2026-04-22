import json
from pathlib import Path


# Reads mock job data and applies simple filters.
def fetch_jobs_from_file(role=None, location=None, keyword=None):
    data_path = Path(__file__).resolve().parent.parent / "data" / "mock_jobs.json"

    with open(data_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    results = jobs

    if role:
        results = [job for job in results if role.lower() in job["title"].lower()]

    if location:
        results = [job for job in results if location.lower() in job["location"].lower()]

    if keyword:
        results = [
            job for job in results
            if keyword.lower() in job["title"].lower()
            or keyword.lower() in job["company"].lower()
            or keyword.lower() in job["location"].lower()
        ]

    return results