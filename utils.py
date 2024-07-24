import os
import requests
import json
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

webhook = os.getenv("webhook")


def get_database():
    mongo_uri = os.getenv("mongo")
    client = MongoClient(mongo_uri, server_api=ServerApi("1"))

    return client["job_postings"]


database = get_database()


def send_webhook(company, title, url, type):
    embed = {
        "title": f"job found at {company} plz apply",
        "color": 0xFF0000,
        "fields": [
            {"name": "Job Title", "value": title, "inline": True},
            {"name": "Type", "value": type, "inline": True},
            {"name": "Link", "value": url, "inline": True},
        ],
    }

    message = {
        "username": "employment bot",
        "content": "<@&1247731582450794607>",
        "embeds": [embed],
    }

    if company == "roblox":
        message["content"] = "<@&1247731582450794607> <@&1265702582014316684>"

    headers = {"Content-Type": "application/json"}

    payload = json.dumps(message)

    try:
        temp = requests.post(webhook, headers=headers, data=payload)
        print(company, title, temp.status_code)
    except:
        print(f"{company}: webhook failed to send")


def read_mongo(collection, key):
    return collection.count_documents({"id": key}) > 0


def write_mongo(collection, key):
    collection.insert_one({"id": key})
