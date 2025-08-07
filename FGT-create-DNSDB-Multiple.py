# Replace IP addres and API Token to execute Create Firewall address

import requests
import json
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Read url from a notepad file
ip_file_path = "login.txt"
with open(ip_file_path, "r") as file:
    url = file.read().splitlines()

print(f" Url: {url}")

# Read domain from a notepad file
ip_file_path = "domainlist.txt"
with open(ip_file_path, "r") as file:
    ip_addresses = file.read().splitlines()

print(f" Domain: {ip_addresses}")

# Read apitoken from a notepad file
ip_file_path = "apitoken.txt"
with open(ip_file_path, "r") as file:
    apitoken = file.read().splitlines()

print(f" Token: {apitoken}")


for api_url,api_token in zip(url,apitoken):
    headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
    }

    for ip_address in ip_addresses:
        dns_data = {
            "name": ip_address,
            "status": "enable",
            "domain": ip_address,
            "allow-transfer": "",
            "type": "primary",
            "view": "shadow",
            "ip-primary": "0.0.0.0",
            "primary-name": "dns",
            "contact": "host",
            "ttl": 86400,
            "authoritative": "disable",
            "forwarder": "\"8.8.8.8\" ",
            "source-ip": "0.0.0.0",
            "rr-max": 16384,
            "dns-entry": []
            } 
            # Send the API request to create the api name
        response = requests.post(api_url, headers=headers, json=dns_data, verify=False)  


# Check the response status
if response.status_code == 200:
    print('Domain name created successfully.')
else:
    print('Failed to create domain. Error:', response.text) 
