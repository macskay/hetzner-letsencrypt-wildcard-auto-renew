# Let's Encrypt Wildcard Auto-Renewal with Hetzner Zone-File DNS Challenge

The provided scripts will auto-renew your Let's Encrypt Wildcard Certificates. For the renewal a DNS Challenge is needed and the certbot-auto asks for a TXT Record named *_acme-challenge* to be set to a random generated string.

The scripts will update the Zone File within the Hetzner Robot Web-GUI to that new string and await the DNS change to take effect before proceeding with the re-issuing of the certificates.

## Prerequisites

- Python 3.7+
- certbot-auto

## Installation

In order for the scripts to work some 3rd party modules are required. They can be installed as follows:

```
$ pip3 install -r requirements.txt
```

## Configuration

The scripts need to know your login data and the installation path of certbot-auto to function correctly. The Installation Path to certbot-auto has to be set in the `certbot.py` file. Just edit the `CERTBOT_AUTO` global variable.

The credentials for the Hetzner Robot can be set in the function auth within the `hetzner.py` file. Simply replace `YOUR-HETZNER-USER` and `YOUR-HETZNER-PASS` with your details.



## Usage

The Usage is quite simple. Just call the renew.py script with the TLD for which the Zone-File needs to be updated, i.e. the TLD the certificate is due for renewal. In my setup for example I have the following cronjob active

```
@monthly /root/.virtualenvs/hetzner/bin/python /opt/hetzner/renew.py macskay.com
```

You can run the script monthly. If the certbot-auto returns a `Certificate is not yet due for renewal` the script will stop immediately, otherwise the renewal process is started.


# Disclaimer

Even though the scripts are used in production on my system and are tested on a Ubuntu 18.04.02 system I do neither claim correctness nor completeness on these scripts. Use at your own risk!
