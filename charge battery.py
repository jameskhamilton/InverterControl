import requests
import json
import asyncio
import solis_functions as sf

filePath = 'C:\\test\\security.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

keyId = securityData['keyId']
secretKey = securityData['secretKey'].encode('utf-8') #bytes literal
password = securityData['password']
username = securityData['username']
inverterSn = securityData['inverterSn']
inverterId = securityData['inverterId']

url = 'https://www.soliscloud.com:13333'
controlResource = '/v2/api/control'
loginResource = '/v2/api/login'

chargeStart = "00:00"
chargeEnd = "00:00"
dischargeStart = "00:00"
dischargeEnd = "00:00"

async def login(usernameValue: str, passwordValue: str, keyIdValue: str, secretKeyValue:str) -> str:
    """
    Returns:
    - Login token
    """
    body = f'{{"userInfo":"{usernameValue}","passWord":"{sf.hexMD5(passwordValue)}"}}'

    header = { "Content-MD5":sf.base64Hash(body),
        "Content-Type":sf.contentType(),
        "Date":sf.currentDateTime(0),
        "Authorization":sf.authValue(keyIdValue, secretKeyValue, body, loginResource)
        }
    
    req = url + loginResource
    result = requests.post(req, data=body, headers=header)

    resultJSON = result.json()

    return resultJSON["csrfToken"]

async def main(function: int) -> str:
    """
    Parameters:
    - 0 (int) updates the charge settings with times passed in global variable
    - 1 (int) updates the inverter time to current datetime
    
    Returns:
    - JSON result from the web request
    """
    if function == 0:
        # set the charge datetimes
        body = f'{{"inverterId":"{inverterId}","cid":"103","value":"50,50,{chargeStart},{chargeEnd},{dischargeStart},{dischargeEnd},50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00"}}'
    else:
        # set the inverter time
        body = f'{{"inverterId":"{inverterId}","cid":56,"value":"{sf.currentDateTime(1)}"}}'

    token = await login(username, password, keyId, secretKey)

    print(body)

    header = { "Content-MD5":sf.base64Hash(body),
                "Content-Type":sf.contentType(),
                "Date":sf.currentDateTime(0),
                "Authorization":sf.authValue(keyId, secretKey, body, controlResource),
                "Token":token
                }

    req = url + controlResource
    result = requests.post(req, data=body, headers=header)

    print(json.dumps(result.json(), indent=2, sort_keys=True))

asyncio.run(main(0))
