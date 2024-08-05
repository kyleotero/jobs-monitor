import requests
import json
from utils import send_webhook, database, read_mongo, write_mongo, keywords

ramp_collection = database["ramp"]
query = {
    "operationName": "ApiJobBoardWithTeams",
    "variables": {"organizationHostedJobsPageName": "ramp"},
    "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n  jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}",
}
base_url = "https://jobs.ashbyhq.com/ramp/"


def ramp_monitor():
    try:
        r = requests.post(
            "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams",
            json=query,
        )
        data = json.loads(r.text)["data"]["jobBoard"]["jobPostings"]
    except:
        print("Ramp: request failed", r.text)
        return

    for job in data:
        if (
            any(keyword in job["title"].split() for keyword in keywords)
            or any(keyword in job["employmentType"].split() for keyword in keywords)
        ) and not read_mongo(ramp_collection, job["id"]):
            send_webhook(
                "ramp",
                job["title"],
                base_url + job["id"],
                job["employmentType"],
            )

            write_mongo(ramp_collection, job["id"])
