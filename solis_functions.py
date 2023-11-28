import hashlib
from hashlib import sha1
import hmac
import base64
from datetime import datetime, timezone
import http.client
import json

url = 'www.soliscloud.com'
port = '13333'
apiMethod = 'POST'

def contentType() -> str:
    return 'application/json'

def currentDateTime(format: int) -> str:
    """
    Parameters:
    - 0 (int) to return the authentication format
    - 1 (int) to return the update format
    """
    now = datetime.now(timezone.utc)
    dttime = None
    if format == 0:
        dttime = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    elif format == 1:
        dttime = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError("Incorrect (int) value passed to currentDateTime(): {format}\nExpected values are 0,1")
    return dttime

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

def authValue(keyIdValue: str, secretKeyValue:str, bodyValue: str, resourceValue: str) -> str:
    """
    Returns:
    - authentication string
    """
    dttime = None
    try: 
        dttime = currentDateTime(0)
    except ValueError as e:
        print(e)

    encryptStr = (apiMethod + "\n"
        + base64Hash(bodyValue) + "\n"
        + contentType() + "\n"
        + dttime + "\n"
        + resourceValue)
    auth = "API " + keyIdValue + ":" + hmacEncrypt(secretKeyValue, encryptStr)
    return auth

async def solisAPICall(resourceValue: str, bodyValue: str, headerValue: str) -> str:
    """
    Parameter:
    - resource path
    - http request body
    - http request header

    Returns:
    - JSON string
    """
    try:
        conn = http.client.HTTPSConnection(url, port)
        conn.request(apiMethod, resourceValue, bodyValue, headerValue)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.code >= 400:
            print(f'Error: {response.code} - {resultJSON}')
        else:
            return json.loads(data) 
    except http.client.HTTPException as e:
        print(f'Error: {e}')
    finally:
        conn.close()