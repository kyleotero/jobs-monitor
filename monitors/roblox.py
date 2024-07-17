import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

roblox_collection = database["janestreet"]
keywords = ["Internship", "internship", "New Grad", "new grad"]


def roblox_monitor():
    try:
        r = requests.get(
            "https://boards-api.greenhouse.io/v1/boards/roblox/jobs?content=true"
        )
        data = json.loads(r.text)["jobs"]
    except:
        print("Roblox: request failed")
        return

    for job in data:
        if (
            any(keyword in job["metadata"][0]["value"] for keyword in keywords)
            or any(keyword in job["title"] for keyword in keywords)
            and not read_mongo(roblox_collection, job["internal_job_id"])
        ):
            send_webhook(
                "roblox",
                job["title"],
                job["absolute_url"],
                job["metadata"][0]["value"],
            )

            write_mongo(roblox_collection, job["internal_job_id"])