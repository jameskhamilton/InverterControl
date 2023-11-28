import hashlib
from hashlib import sha1
import hmac
import base64
from datetime import datetime
from datetime import timezone
import requests
import json
import asyncio

filePath = 'C:\\test\\security.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

keyId = securityData['keyId']
secretKey = securityData['secretKey'].encode('utf-8') #bytes literal
password = securityData['password']
username = securityData['username']
inverterSn = securityData['inverterSn']
inverterId = securityData['inverterId']

method = "POST"
now = datetime.now(timezone.utc)
dttime = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
dttimeUpdate = now.strftime("%Y-%m-%d %H:%M:%S")
contentType = "application/json"

url = 'https://www.soliscloud.com:13333'
controlResource = '/v2/api/control'
loginResource = '/v2/api/login'

def base64Hash(bodyValue: str) -> str:
    hashValue = base64.b64encode(hashlib.md5(bodyValue.encode('utf-8')).digest()).decode('utf-8')
    return hashValue

def hexMD5(passwordValue: str) -> str:
    hexValue = hashlib.md5(passwordValue.encode('utf-8')).hexdigest()
    return hexValue

def hmacEncrypt(secretKeyValue: str, encryptStrValue: str) -> str:
    h = hmac.new(secretKeyValue, msg=encryptStrValue.encode('utf-8'), digestmod=hashlib.sha1)
    sign = base64.b64encode(h.digest()).decode('utf-8')
    return sign

def authValue(keyIdValue: str, secretKeyValue:str, bodyValue: str, resourceValue: str) -> str: #returns authentication string
    encryptStr = (method + "\n"
        + base64Hash(bodyValue) + "\n"
        + contentType + "\n"
        + dttime + "\n"
        + resourceValue)

    auth = "API " + keyIdValue + ":" + hmacEncrypt(secretKeyValue, encryptStr)

    return auth

async def login(usernameValue: str, passwordValue: str, keyIdValue: str, secretKeyValue:str) -> str: #returns login token
    body = f'{{"userInfo":"{usernameValue}","passWord":"{hexMD5(passwordValue)}"}}'

    header = { "Content-MD5":base64Hash(body),
        "Content-Type":contentType,
        "Date":dttime,
        "Authorization":authValue(keyIdValue, secretKeyValue, body, loginResource)
        }
    
    req = url + loginResource
    result = requests.post(req, data=body, headers=header)

    resultJSON = result.json()

    return resultJSON["csrfToken"]

async def main() -> str: #returns the json result of the control request
    
    # set the time (works)
    # body = f'{{"inverterId":"{inverterId}","cid":56,"value":"{dttimeUpdate}"}}'
    #

    # set the charge datetimes (works)
    body = f'{{"inverterId":"{inverterId}","cid":"103","value":"50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00"}}'

    token = await login(username, password, keyId, secretKey)

    print(body)
    print(token)

    header = { "Content-MD5":base64Hash(body),
                "Content-Type":contentType,
                "Date":dttime,
                "Authorization":authValue(keyId, secretKey, body, controlResource),
                "Token":token
                }

    req = url + controlResource
    result = requests.post(req, data=body, headers=header)

    print(json.dumps(result.json(),indent=2, sort_keys=True))


asyncio.run(main())
