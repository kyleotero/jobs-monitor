import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

ramp_collection = database["ramp"]
keywords = [
    "Internship",
    "internship",
    "New Grad",
    "new grad",
    "Co-op",
    "co-op",
]


def ramp_monitor():
    try:
        r = requests.get("https://api.ashbyhq.com/posting-api/job-board/ramp")
        data = json.loads(r.text)["jobs"]
    except:
        print("Ramp: request failed")
        return

    for job in data:
        if any(keyword in job["title"] for keyword in keywords) and not read_mongo(
            ramp_collection, job["id"]
        ):
            send_webhook(
                "ramp",
                job["title"],
                job["jobUrl"],
                job["employmentType"],
            )

            write_mongo(ramp_collection, job["id"])
