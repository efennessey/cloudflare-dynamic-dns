import json
import requests
import sys
import public_ip

def getRecords(zone):
    endpoint = "https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/"
    response = requests.get(endpoint, headers=headers)
    #TODO: validate response
    return response.json()["result"]

def updateRecord(zone, record):
    endpoint = "https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/" + record["id"]
    body = json.dumps({"content": ip})
    response = requests.patch(endpoint, headers=headers, data=body)
    #TODO: validate response
    #TODO: return records that were actually updated



config = json.load(open(sys.argv[1]))
headers = {"Authorization": "Bearer " + config["bearerToken"]}
ip = public_ip.get()
recordNames =[]

for domain in config["domains"]:
    for record in getRecords(domain["zoneId"]):
        updateRecord(domain["zoneId"], record)
        #TODO use recordNames returned from updateRecord
        recordNames.append(record["name"])

print("Updated the following records to " + ip + ":")
for name in recordNames:
    print(name)
