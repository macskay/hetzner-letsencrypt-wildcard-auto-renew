import os
import sys
import requests
import json

BASE_URL = "https://dns.hetzner.com/api/v1"
TOKEN = "HETZNER_TOKEN" in os.environ and os.environ["HETZNER_TOKEN"]
RECORD_NAME = "_acme-challenge"

def get_zone(domain):
    try:
        response = requests.get(
            url=f"{BASE_URL}/zones",
            headers={
                "Auth-API-Token": TOKEN,
            },
        )
        if (response.status_code != 200):
            sys.exit("Error on fetching zone, please check your token")
        content = json.loads(response.content.decode("utf-8"))
        if "zones" in content:
            zones = content["zones"]
            return next(item for item in zones if item["name"] == domain)
        else:
            sys.exit("No zones!")
    except requests.exceptions.RequestException:
        sys.exit("Get Zones HTTP Request failed")

def get_acme_record(zone):
    try:
        response = requests.get(
            url=f"{BASE_URL}/records",
            params={
                "zone_id": zone["id"],
            },
            headers={
                "Auth-API-Token": TOKEN,
            },
        )
        if (response.status_code != 200):
            sys.exit("Error on fetching acme record, please check your token")
        content = json.loads(response.content.decode("utf-8"))
        if ("records" in content):
            records = content["records"]
            return next((item for item in records if item["name"] == RECORD_NAME), { "value": "" })
        else:
            sys.exit("No records!")
    except requests.exceptions.RequestException:
        sys.exit("Get Records HTTP Request failed")

def save_acme_record(zone, record, value):
    payload = json.dumps({
        "value": value,
        "ttl": 86400,
        "type": "TXT",
        "name": RECORD_NAME,
        "zone_id": zone["id"]
    })
    try:
        if ("id" in record):
            response = requests.put(
                url = f"{BASE_URL}/records/" + record["id"],
                headers = {
                    "Content-Type": "application/json",
                    "Auth-API-Token": TOKEN,
                },
                data = payload
            )
        else:
            response = requests.post(
                url = f"{BASE_URL}/records",
                headers = {
                    "Content-Type": "application/json",
                    "Auth-API-Token": TOKEN,
                },
                data = payload
            )
        if (response.status_code != 200):
            sys.exit("Error on saving acme record")
        return json.loads(response.content.decode("utf-8"))
    except requests.exceptions.RequestException:
        sys.exit("HTTP Request failed")
