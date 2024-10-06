import re
import json

def checkFormat(chargeTestValue: str) -> bool:
    """
    Checks the charge time string contains correct time values
    
    Makes sure the amps are <= 50
    """
    pattern = re.compile(
        r'^([0-4]?\d|50),([0-4]?\d|50),(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,'
        r'([0-4]?\d|50),([0-4]?\d|50),(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,'
        r'([0-4]?\d|50),([0-4]?\d|50),(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d,(0[0-9]|1[0-9]|2[0-3]):[0-5]\d'
    )

    return bool(pattern.match(chargeTestValue))

def checkJSONFormat(json_string):
    try:
        json_data = json.loads(json_string)
        print("Valid JSON")
        return json_data
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        return None