import hetzner
import certbot
import requests
import sys
import dns.resolver
import subprocess
import os

def main():
    domain = sys.argv[1]
    session = requests.session()
    res = hetzner.login(session)
    id = hetzner.get_zone_id(session, domain)

    zone = hetzner.get_zone(session, id)
    certbot.renew(session, zone, id, domain)

    os.system("apache2ctl gracfeul")


if __name__ == "__main__":
    main()

