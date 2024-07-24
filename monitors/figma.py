import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

figma_collection = database["figma"]
keywords = [
    "Internship",
    "internship",
    "New Grad",
    "new grad",
    "Co-op",
    "co-op",
]


def figma_monitor():
    try:
        r = requests.get(
            "https://boards-api.greenhouse.io/v1/boards/figma/jobs?content=true"
        )
        data = json.loads(r.text)["jobs"]
    except:
        print("Figma: request failed")
        return

    for job in data:
        if any(keyword in job["title"] for keyword in keywords) and not read_mongo(
            figma_collection, job["id"]
        ):
            send_webhook(
                "figma",
                job["title"],
                job["absolute_url"],
                "idk lol",
            )

            write_mongo(figma_collection, job["id"])