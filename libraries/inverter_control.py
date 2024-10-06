
import json
import asyncio
import inverter_functions as sf
import unit_tests as ut

keyId,secretKey,_,password,username,inverterSn,inverterId = sf.secrets()

controlResource = '/v2/api/control'
loginResource = '/v2/api/login'

chSt0 = '00:00'
chEn0 = '00:00'
dischSt0 = '00:00'
dischEn0 = '00:00'
chSt1 = '00:00'
chEn1 = '00:00'
dischSt1 = '00:00'
dischEn1 = '00:00'
chSt2 = '00:00'
chEn2 = '00:00'
dischSt2 = '00:00'
dischEn2 = '00:00'

chargeTimes = f"50,50,{chSt0},{chEn0},{dischSt0},{dischEn0},50,50,{chSt1},{chEn1},{dischSt1},{dischEn1},50,50,{chSt2},{chEn2},{dischSt2},{dischEn2}"

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

def controlBody(functionValue: int, chargeValue: str = None) -> str:
    """
    Parameters:
    - takes the function and charge values from controlMain
    - check that function for more detail about those parameters

    Returns:
    - body value that's passed in the web request
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
    
    return body

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
    body = controlBody(functionValue, chargeValue)

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