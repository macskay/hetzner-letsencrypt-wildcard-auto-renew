import requests
import pudb
import json
import bs4
import re

ROBOT = "https://robot.your-server.de"
ACCOUNT = "https://accounts.hetzner.com"

headers = {
    "Cookie": "PHPSESSID=2736c97105cc568d0267ea2f4decbce; cookies_allowed=1"
}

def auth(csrf):
    return {
        '_username': "YOUR-HETZNER-USER",
        '_password': "YOUR-HETZNER-PASS",
        '_csrf_token': csrf
    }


def login(session):
    res = session.get(f"{ACCOUNT}/login")
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    csrf = soup.select_one('input[name="_csrf_token"]')["value"]
    return session.post(f"{ACCOUNT}/login_check", data=auth(csrf))

def get_zone_id(session, domain):
    res = session.post(f"{ROBOT}/dns")
    soup = bs4.BeautifulSoup(res.text, "html.parser")


    x = soup.findAll(text=domain)[0].findParents('table')[0]["onclick"]
    return re.findall('\d{6}', x)[0]


def get_zone(session, id):
    res = session.post(f"{ROBOT}/dns/update/id/{id}")
    return bs4.BeautifulSoup(res.text, "html.parser")


def save_new_zone(session, zone, id, csrf):
    res = session.post(f"{ROBOT}/dns/update", data={'id': id, 'zonefile': zone, '_csrf_token': csrf})
    print(res.text)
    if "Vielen Dank für Ihren Auftrag. Der DNS-Eintrag wird nun geändert" in res.text:
        return True
    return False


