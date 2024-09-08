import json
import requests
import sys
import public_ip

def getRecords(zone):
    endpoint = "https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/"
    response = requests.get(endpoint, headers=headers)
    validateResponse(response, zone, "List DNS Records")
    return response.json()["result"]

def updateRecord(zone, record):
    endpoint = "https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records/" + record["id"]
    body = json.dumps({"content": ip})
    response = requests.patch(endpoint, headers=headers, data=body)
    if validateResponse(response, zone, "Update DNS Record"):
        return response.json()["result"]
    else:
        return False

def validateResponse(response, zone, requestType):
    if response.status_code != 200:
        print("Bad request - " + requestType + " for zone ID " + zone)
        print(response.json()["errors"])
        print(response.raise_for_status())
        return False
    elif not response.json()["success"]:
        print("Errors - " + requestType + " for zone ID " + zone)
        print(response.json()["errors"])
        raise ValueError(requestType + " request was not successful")
        return False
    else:
        return True



config = json.load(open(sys.argv[1]))
headers = {"Authorization": "Bearer " + config["bearerToken"]}
ip = public_ip.get()
recordNames = []

for domain in config["domains"]:
    for record in getRecords(domain["zoneId"]):
        newRecord = updateRecord(domain["zoneId"], record)
        if newRecord:
            recordNames.append(newRecord["name"])

print("Updated the following records to " + ip + ":")
for name in recordNames:
    print(name)
