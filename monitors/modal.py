import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

modal_collection = database["modal"]
keywords = [
    "Internship",
    "internship",
    "New Grad",
    "new grad",
    "Co-op",
    "co-op",
]


def modal_monitor():
    try:
        r = requests.get("https://api.ashbyhq.com/posting-api/job-board/modal")
        data = json.loads(r.text)["jobs"]
    except:
        print("Modal: request failed")
        return

    for job in data:
        if any(keyword in job["title"] for keyword in keywords) and not read_mongo(
            modal_collection, job["id"]
        ):
            send_webhook(
                "modal",
                job["title"],
                job["jobUrl"],
                job["employmentType"],
            )

            write_mongo(modal_collection, job["id"])
