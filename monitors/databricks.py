import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo

base_url = "https://www.janestreet.com/join-jane-street/position/"
databricks_collection = database["databricks"]
keywords = ["Internship", "internship", "New Grad", "new grad"]


def databricks_monitor():
    try:
        r = requests.get(
            "https://www.databricks.com/careers-assets/page-data/company/careers/open-positions/page-data.json?department=University%20Recruiting&location=all"
        )
        data = json.loads(r.text)
    except:
        print("Databricks: request failed")
        return

    for dept in data["result"]["pageContext"]["data"]["allGreenhouseDepartment"][
        "nodes"
    ]:
        if dept["name"] == "University Recruiting":
            data = dept["jobs"]
            break

    for job in data:
        if any(keyword in job["title"] for keyword in keywords) and not read_mongo(
            databricks_collection, job["gh_Id"]
        ):
            send_webhook(
                "databricks",
                job["title"],
                job["absolute_url"],
                "N/A",
            )

            write_mongo(databricks_collection, job["gh_Id"])
