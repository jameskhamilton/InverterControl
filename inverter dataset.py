import hashlib
from hashlib import sha1
import hmac
import base64
from datetime import datetime
from datetime import timezone
import requests
import json

filePath = 'C:\\test\\security.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

keyId = securityData['keyId']
secretKey = securityData['secretKey'].encode('utf-8') #bytes literal
stationId = securityData['stationId']

method = "POST"
now = datetime.now(timezone.utc)
dttime = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
contentType = "application/json"
url = 'https://www.soliscloud.com:13333'
resource = "/v1/api/inveterList"

body = f'{{"stationId":"{stationId}"}}'

contentMD5 = base64.b64encode(hashlib.md5(body.encode('utf-8')).digest()).decode('utf-8')

encryptStr = (method + "\n"
    + contentMD5 + "\n"
    + contentType + "\n"
    + dttime + "\n"
    + resource)

h = hmac.new(secretKey, msg=encryptStr.encode('utf-8'), digestmod=hashlib.sha1)

sign = base64.b64encode(h.digest())

auth = "API " + keyId + ":" + sign.decode('utf-8')

header = { "Content-MD5":contentMD5,
            "Content-Type":contentType,
            "Date":dttime,
            "Authorization":auth
            }

req = url + resource
result = requests.post(req, data=body, headers=header)

jsonData = result.json()

records = []

for record in jsonData['data']['page']['records']:

    recordId = record['id']
    recordTimestamp = record['dataTimestampStr']
    recordSoC = record['batteryCapacitySoc']
    recordDischarge = -record['batteryPower'] #flipping negation to make discharge the positive value, charging a negative
    recordPVYield = record['pac']
    recordGridUsage = -record['psum'] #flipping negation to make grid usage a positive, sending to grid a negative

records.append({
        'Inverter ID': recordId,
        'Data Timestamp': recordTimestamp,
        'SoC': recordSoC,
        'Battery Discharge KwH': recordDischarge,
        'PV Yield KwH': recordPVYield,
        'Grid Usage KwH': recordGridUsage,
        'House Load KwH': recordDischarge + recordPVYield + recordGridUsage
})

print(records)
