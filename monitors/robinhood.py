import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

robinhood_collection = database["robinhood"]
keywords = [
    "Internship",
    "internship",
    "New Grad",
    "new grad",
    "Co-op",
    "co-op",
]


def robinhood_monitor():
    try:
        r = requests.get("https://api.greenhouse.io/v1/boards/robinhood/jobs")
        data = json.loads(r.text)["jobs"]
    except:
        print("Robinhood: request failed")
        return

    for job in data:
        if any(keyword in job["title"] for keyword in keywords) and not read_mongo(
            robinhood_collection, job["id"]
        ):
            send_webhook(
                "robinhood",
                job["title"],
                job["absolute_url"],
                "idk lol",
            )

            write_mongo(robinhood_collection, job["id"])
