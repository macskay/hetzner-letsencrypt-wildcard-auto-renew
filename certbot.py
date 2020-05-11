import os
import sys
import pexpect
import hetzner
import time
import subprocess

def get_acme_challenge(domain):
    return subprocess.check_output(["dig", "-t", "txt", f"_acme-challenge.{domain}", "+short"]).decode("utf-8").replace('"', "")

def renew(zone, record, domain, cetbot_path):
    record = hetzner.get_acme_record(zone)
    old = record["value"]
    child = pexpect.spawn(f"/bin/bash -c {cetbot_path} certonly -d *.{domain} --server https://acme-v02.api.letsencrypt.org/directory --manual --preferred-challenges dns --manual-public-ip-logging-ok", encoding="utf-8")
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

            if hetzner.save_acme_record(zone, record, new):
                print("DNS Change Invoked")
                print("Waiting for DNS Change to come through")
                while old == get_acme_challenge(domain):
                    print(".", end="")
                    time.sleep(1)

        child.sendline()
        child.expect("Congratulations!")
