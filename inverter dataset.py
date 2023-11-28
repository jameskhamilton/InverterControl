import requests
import json
import asyncio
import solis_functions as sf

filePath = 'C:\\test\\security.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

keyId = securityData['keyId']
secretKey = securityData['secretKey'].encode('utf-8') #bytes literal
stationId = securityData['stationId']

url = 'https://www.soliscloud.com:13333'
resource = "/v1/api/inveterList"

async def dataset() -> str:
    """
    Purpose:
    - makes API call to obtain the full JSON result from inverterList

    Returns:
    - JSON string
    """
    body = f'{{"stationId":"{stationId}"}}'

    header = { "Content-MD5":sf.base64Hash(body),
                "Content-Type":sf.contentType(),
                "Date":sf.currentDateTime(0),
                "Authorization":sf.authValue(keyId, secretKey, body, resource)
                }

    req = url + resource
    result = requests.post(req, data=body, headers=header)

    jsonData = result.json()
    return jsonData

async def main() -> list:
    """
    Returns:
    - list containing
        - Inverter ID
        - Data Timestamp (when the datalogger made the dataset available, following values are all as at this point in time)
        - SoC
        - Battery Discharge KwH
        - PV Yield KwH
        - Grid Usage KwH
        - House Load KwH
    """
    records = []
    jsonData = await dataset()

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

    return records

records = asyncio.run(main())
print(records)