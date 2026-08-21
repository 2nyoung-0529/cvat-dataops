import requests

from config import BASE_URL, API_TOKEN


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/vnd.cvat+json",
}

# Reuse a single connection pool across all requests instead of opening
# a new TCP/TLS connection for every call.
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def _get_paginated(url, params=None):
    """Fetch every page of a CVAT list endpoint and return all results.

    CVAT list responses are paginated: each page holds a `results` array and
    a `next` URL (or null on the last page). We follow `next` until it runs out.
    """
    results = []

    while url:
        response = SESSION.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        results.extend(data.get("results", []))

        # `next` is an absolute URL that already carries the paging params,
        # so we drop `params` after the first request to avoid duplicating them.
        url = data.get("next")
        params = None

    return results


def get_tasks():
    return _get_paginated(f"{BASE_URL}/tasks")


def get_jobs(task_id):
    return _get_paginated(f"{BASE_URL}/jobs", params={"task_id": task_id})


def get_annotations(job_id):
    response = SESSION.get(
        f"{BASE_URL}/jobs/{job_id}/annotations",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()
