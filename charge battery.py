
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

controlResource = '/v2/api/control'
loginResource = '/v2/api/login'

chargeStart = '01:00'
chargeEnd = '05:00'
dischargeStart = '00:00'
dischargeEnd = '00:00'

async def login(usernameValue: str, passwordValue: str, keyIdValue: str, secretKeyValue:str) -> str:
    """
    Returns:
    - Login token
    """
    body = f'{{"userInfo":"{usernameValue}","passWord":"{sf.hexMD5(passwordValue)}"}}'

    try: 
        dttime = sf.currentDateTime(0)
    except ValueError as e:
        print(e)

    header = { "Content-MD5":sf.base64Hash(body),
        "Content-Type":sf.contentType(),
        "Date":dttime,
        "Authorization":sf.authValue(keyIdValue, secretKeyValue, body, loginResource)
        }

    resultJSON = await sf.solisAPICall(loginResource, body, header)

    return resultJSON["csrfToken"]

async def controlMain(functionValue: int) -> str:
    """
    Parameters:
    - 0 (int) updates the charge settings with times passed in global variable
    - 1 (int) updates the inverter time to current datetime
    
    Returns:
    - JSON result from the web request
    """
    if functionValue == 0:
        # set the charge datetimes
        body = f'{{"inverterId":"{inverterId}","cid":"103","value":"50,50,{chargeStart},{chargeEnd},{dischargeStart},{dischargeEnd},50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00"}}'
    elif functionValue == 1:
        # set the inverter time
        dttime = None
        try: 
            dttime = sf.currentDateTime(1)
        except ValueError as e:
            print(e)

        body = f'{{"inverterId":"{inverterId}","cid":56,"value":"{dttime}"}}'
    else:
        raise ValueError(f"Incorrect (int) value passed to main(): {function}\nExpected values are 0,1")

    token = await login(username, password, keyId, secretKey)

    dttime = None
    try: 
        dttime = sf.currentDateTime(0)
    except ValueError as e:
        print(e)

    header = { "Content-MD5":sf.base64Hash(body),
                "Content-Type":sf.contentType(),
                "Date":dttime,
                "Authorization":sf.authValue(keyId, secretKey, body, controlResource),
                "Token":token
                }

    resultJSON = await sf.solisAPICall(controlResource, body, header)  

    print(json.dumps(resultJSON, indent=2, sort_keys=True))
    
try:
    asyncio.run(controlMain(0))
except ValueError as e:
    print(e)