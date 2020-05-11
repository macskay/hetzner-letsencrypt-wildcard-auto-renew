import os
import requests
import json

BASE_URL = "https://dns.hetzner.com/api/v1"
TOKEN = os.environ['HETZNER_TOKEN']

def get_zone(domain):
    try:
        response = requests.get(
            url=f"{BASE_URL}/zones",
            headers={
                "Auth-API-Token": TOKEN,
            },
        )
        if (response.status_code != 200):
            exit("Error on fetching zone, please check your token")
        return next(item for item in json.loads(response.content.decode('utf-8'))["zones"] if item["name"] == domain)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

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
            exit("Error on fetching acme record, please check your token")
        return next(item for item in json.loads(response.content.decode('utf-8'))["records"] if item["name"] == '_acme-challenge')
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def save_acme_record(zone, record, value):
    try:
        response = requests.put(
            url=f"{BASE_URL}/records/" + record["id"],
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": TOKEN,
            },
            data=json.dumps({
                "value": value,
                "ttl": 0,
                "type": "TXT",
                "name": "_acme-challenge",
                "zone_id": zone["id"]
            })
        )
        if (response.status_code != 200):
            exit("Error on saving acme record")
        return json.loads(response.content.decode('utf-8'))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
