
import json
import asyncio
import solis_functions as sf
import unit_tests as ut

keyId,secretKey,_,password,username,inverterSn,inverterId = sf.secrets()

controlResource = '/v2/api/control'
loginResource = '/v2/api/login'

chargeStart = '00:00'
chargeEnd = '00:00'
dischargeStart = '00:00'
dischargeEnd = '00:00'

chargeTimes = f"50,50,{chargeStart},{chargeEnd},{dischargeStart},{dischargeEnd},50,50,00:00,00:00,00:00,00:00,50,50,00:00,00:00,00:00,00:00"

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

async def controlMain(functionValue: int, chargeValue: str = None) -> json:
    """
    Function parameter:
    - 0 (int) updates the charge settings with times passed in chargeValue variable
    - 1 (int) updates the inverter time to current datetime

    Charge parameter:
    - Amp and time values for when the inverter should charge or discharge.
    - Amp charge 1, Amp discharge 1, Charge start time 1, Change end time 1, Discharge start time 1, Discharge end time 1... 2... 3
        
    Returns:
    - JSON result from the web request
    """
    if functionValue == 0:
        # set the charge datetimes
        if chargeValue == None:
            raise ValueError("No charge times have been passed.")
        elif ut.checkFormat(chargeValue):
            body = f'{{"inverterId":"{inverterId}","cid":"103","value":"{chargeTimes}"}}'
        else:
            raise ValueError(f"Charge times / amps failed validation: {chargeValue}")
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
    return resultJSON

if __name__ == '__main__':
    try:
        asyncio.run(controlMain(0,chargeTimes))
    except ValueError as e:
        print(e)