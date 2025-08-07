# Replace IP addres and API Token to execute Create Firewall address

import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_url = 'https://10.128.42.89/api/v2/cmdb/system/dns-database'

#api_url = 'https://10.128.41.106:4455/api/v2/cmdb/system/dns-database'

#api_url = 'https://192.168.20.99:9443/api/v2/cmdb/system/dns-database'

# FortiGate API token(FortiWIFI-60E)
#api_token = 'rzpfcQqq0rmsyb68s076gjH3m6t8wh'

# FortiGate API token(FG-HUB)
api_token = 'c6gysxN9b4887f76G7n8hsGsHN4kNd'

# Domain Name

#domain_name = 'reuters.com'

# Read domain from a notepad file
ip_file_path = "domainlist.txt"
with open(ip_file_path, "r") as file:
    ip_addresses = file.read().splitlines()

print(f" Domain: {ip_addresses}")


# Set the 'Authorization' header with the API token
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# Create the JSON payload for the Domain name
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
    # Send the API request to create the Domain name
    response = requests.post(api_url, headers=headers, json=dns_data, verify=False)    

# Check the response status
if response.status_code == 200:
    print('Domain name created successfully.')
else:
    print('Failed to create domain. Error:', response.text) 
