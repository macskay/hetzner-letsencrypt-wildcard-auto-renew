import hetzner
import certbot
import sys
import os

def main():
    if (len(sys.argv) != 2):
        print("Let's Encrypt Wildcard Auto-Renewal with Hetzner\n")
        print("Domain name is missing\n")
        print("Usage: python renew.py example.com")
        exit()
    domain = sys.argv[1]
    zone = hetzner.get_zone(domain)
    record = hetzner.get_acme_record(zone)
    certbot.renew(zone, record, domain)
    os.system("apache2ctl gracfeul")

if __name__ == "__main__":
    main()
