import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

base_url = "https://www.janestreet.com/join-jane-street/position/"
js_collection = database["janestreet"]


def janestreet_monitor():
    try:
        r = requests.get("https://www.janestreet.com/jobs/main.json")
        data = json.loads(r.text)
    except:
        print("Jane Street: request failed")
        return

    for job in data:
        if (
            "Internship" in job["availability"]
            or "internship" in job["availability"]
            or "Full-Time: New Grad" in job["availability"]
        ) and not read_mongo(js_collection, job["id"]):
            send_webhook(
                "jane street",
                job["position"],
                f"{base_url}{job['id']}",
                job["availability"],
            )

            write_mongo(js_collection, job["id"])
