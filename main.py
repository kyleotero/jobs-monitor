import requests
import json
import time

webhook = "https://discord.com/api/webhooks/1247724016119058465/dqgd7rGizI_CDiw9MgOBE0Gs0HFfZkUu_RnihSwui_z7gZYV9VlH5vTibClYUkv_gMU7"
base_url = "https://www.janestreet.com/join-jane-street/position/"
seen = set()


while True:
    r = requests.get("https://www.janestreet.com/jobs/main.json")
    data = json.loads(r.text)

    for job in data:
        if ("Internship" in job["availability"] or "internship" in job["availability"] or "Full-Time: New Grad" in job["availability"]) and job["id"] not in seen:

            embed = {
            "title": "job found plz apply",
            "description": "i found new job for u",
            "color": 0xFF0000,
            "fields": [
                {
                    "name": "job title",
                    "value": job['position'],
                    "inline": True
                },
                {
                    "name": "term",
                    "value": job["availability"],
                    "inline": True
                },
                {
                    "name": "link",
                    "value": f"{base_url}{job['id']}",
                    "inline": True
                },
            ]
            }
            
            message = {
                "username": "employment bot",
                "content": "<@&1247731582450794607>",
                "embeds": [embed]
            }

            headers = {
            "Content-Type": "application/json"
            }

            payload = json.dumps(message)

            temp = requests.post(webhook, headers=headers, data=payload)
            print(job["id"], job["position"], temp.status_code)

            seen.add(job["id"])

    time.sleep(60)