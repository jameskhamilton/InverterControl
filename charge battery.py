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

async def login(usernameValue: str, passwordValue: str, keyIdValue: str, secretKeyValue:str) -> str:
    """
    Returns - login token
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

async def main() -> str: #returns the json result of the control request
    
    # set the time (works)
    # dttimeUpdate = sf.currentDateTime(1)
    # body = f'{{"inverterId":"{inverterId}","cid":56,"value":"{dttimeUpdate}"}}'
    #

    # set the charge datetimes (works)
    body = f'{{"inverterId":"{inverterId}","cid":"103","value":"50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00"}}'

    token = await login(username, password, keyId, secretKey)

    print(body)
    print(token)

    header = { "Content-MD5":sf.base64Hash(body),
                "Content-Type":sf.contentType(),
                "Date":sf.currentDateTime(0),
                "Authorization":sf.authValue(keyId, secretKey, body, controlResource),
                "Token":token
                }

    req = url + controlResource
    result = requests.post(req, data=body, headers=header)

    print(json.dumps(result.json(),indent=2, sort_keys=True))


asyncio.run(main())
