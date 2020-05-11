import hetzner
import certbot
import sys
import os

def main():
    print("Let's Encrypt Wildcard Auto-Renewal with Hetzner\n")

    if (len(sys.argv) != 2):
        print("Domain name is missing\n")
        print("Usage: python renew.py example.com")
        exit()

    if (not "HETZNER_TOKEN" in os.environ):
        sys.exit("HETZNER_TOKEN environment variable is missing!")

    if ("CERTBOT_PATH" in os.environ):
        certbot_path = os.environ["CERTBOT_PATH"]
    else:
        certbot_path = "/opt/certbot/certbot-auto"

    if (os.path.exists(certbot_path)):
        domain = sys.argv[1]
        zone = hetzner.get_zone(domain)
        record = hetzner.get_acme_record(zone)
        certbot.renew(zone, record, domain, certbot_path)
    else:
        sys.exit("`certbot/certbot-auto` executable not found please set CERTBOT_PATH environment variable. Path `" + certbot_path + "` doesn't exist")

if __name__ == "__main__":
    main()
