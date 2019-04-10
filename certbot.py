import sys
import pexpect
import re
import hetzner
import dns.resolver
import time
import subprocess

def get_old_acme_entry(zone):
    for line in zone.get_text().splitlines():
        if "_acme-challenge" in line:
            return re.findall('"([^"]*)"', line)[0]

def get_acme_challenge(domain):
    return subprocess.check_output(["dig", "-t", "txt", f"_acme-challenge.{domain}", "+short"]).decode("utf-8").replace('"', '')

def renew(session, zonepage, id, domain):
    zone = zonepage.select_one('textarea[name="zonefile"]')
    csrf = zonepage.select_one('input[name="_csrf_token"]')["value"]

    old = get_old_acme_entry(zone)
    child = pexpect.spawn(f"/bin/bash -c '/opt/certbot/certbot-auto certonly -d *.{domain} --server https://acme-v02.api.letsencrypt.org/directory --manual --preferred-challenges dns --manual-public-ip-logging-ok", encoding="utf-8")
    child.logfile_read = sys.stdout

    ex = child.expect(["Before continuing", "Cert not yet due for renewal"])
    if ex == 1:
        print("Cert not due for renewal. Exiting.")
        sys.exit(0)
    elif ex == 0:
        spl = child.before.split("\n")
        new = spl[-3].strip()
        if old != new:
            print(f"\n\n\nReplacing {old} with {new}")
            new_zone = zone.get_text().replace(old, new)
            print(new_zone)

            if hetzner.save_new_zone(session, new_zone, id, csrf):
                print("DNS Change Invoked")
                print("Waiting for DNS Change to come through")
                while old == get_acme_challenge(domain):
                    print(".", end='')
                    time.sleep(1)
            
        child.sendline()
        child.expect("Congratulations!")
            

