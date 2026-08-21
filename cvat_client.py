import requests

from config import BASE_URL, API_TOKEN


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/vnd.cvat+json",
}
def get_tasks():
    response = requests.get(
        f"{BASE_URL}/tasks",
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])
def get_jobs(task_id):
    response = requests.get(
        f"{BASE_URL}/jobs",
        headers=HEADERS,
        params={"task_id": task_id},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])
def get_annotations(job_id):
    response = requests.get(
        f"{BASE_URL}/jobs/{job_id}/annotations",
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()