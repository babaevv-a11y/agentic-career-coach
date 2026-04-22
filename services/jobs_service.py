import json
from pathlib import Path


# This service handles the fetch_jobs tool.
# For the class project, job data is coming from a local mock JSON file instead of a live API.
def fetch_jobs_from_file(role=None, location=None, keyword=None):
    # Build the path to the mock data file in a way that works no matter where the project is opened from.
    data_path = Path(__file__).resolve().parent.parent / "data" / "mock_jobs.json"

    # Load all mock job entries into memory.
    with open(data_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    # Start with the full job list, then narrow it down if filters are provided.
    results = jobs

    # Filter by role/title if a role was passed in.
    if role:
        results = [job for job in results if role.lower() in job["title"].lower()]

    # Filter by location if a location was passed in.
    if location:
        results = [job for job in results if location.lower() in job["location"].lower()]

    # Keyword is broader than role/location.
    # It checks title, company, and location to make search a little more flexible.
    if keyword:
        results = [
            job for job in results
            if keyword.lower() in job["title"].lower()
            or keyword.lower() in job["company"].lower()
            or keyword.lower() in job["location"].lower()
        ]

    return results