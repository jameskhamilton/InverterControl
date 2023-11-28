import asyncio
import json
import http.client
import base64
from datetime import datetime, timezone

filePath = 'C:\\test\\octopusSecurity.json'
now = datetime.now(timezone.utc)

with open(filePath, 'r') as file:
    securityData = json.load(file)

apiKey = securityData['apiKey']
accountNumber = securityData['accountNumber']
url = f'https://api.octopus.energy/v1/accounts/{accountNumber}/'

def parseDatetime(datetimeString: str) -> datetime:
    """
    Parameter:
    - datetime value as a string

    Returns:
    - datetime value yyyy-mm-dd hh:mm:ss z
    """
    if datetimeString is not None:
        try:
            return datetime.strptime(datetimeString, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            pass
        
        raise ValueError('Unsupported datetime format')
    else:
        return None

async def apiCall(url: str, apiKey: str = None) -> json:
    """
    Parameter:
    - url
    - api key (optional - when included this builds the Authorization string, otherwise no Authorization is passed)

    Returns:
    - JSON dataset
    """
    # Parse the URL to extract the hostname and path
    urlParts = http.client.urlsplit(url)
    hostname = urlParts.hostname
    path = urlParts.path

    conn = http.client.HTTPSConnection(hostname)

    try:
        if apiKey is None:
            conn.request('GET', url)
        else:
            authHeader = 'Basic ' + base64.b64encode(apiKey.encode('utf-8')).decode('utf-8')
            headers = {'Authorization': authHeader,}
            conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.status >= 400:
            print(f'Error: {response.status} - {data}')
        else:
            return json.loads(data)
    except http.client.HTTPException as e:
        print(f'Error: {e}')
    finally:
        conn.close()

resultJSON = asyncio.run(apiCall(url, apiKey))

properties = resultJSON['properties']

metersList = []

for propertyData in properties:
    propertyId = propertyData['id']
    
    for meterPoint in propertyData['electricity_meter_points']:
        mpan = meterPoint['mpan']
        export = meterPoint['is_export']
        
        for meter in meterPoint['meters']:
            serialNumber = meter['serial_number']
            agreements = meterPoint['agreements']
            
            for agreement in agreements:
                tariffCode = agreement['tariff_code']
                validFrom = agreement['valid_from']
                validTo = agreement['valid_to']
                
                validFrom = parseDatetime(validFrom)
                validTo = parseDatetime(validTo)
        
                metersList.append({
                    'Property Id': propertyId,
                    'MPAN': mpan,
                    'Serial Number': serialNumber,
                    'Tariff Code': tariffCode,
                    'Tariff Valid From':validFrom,
                    'Tariff Valid To': validTo,
                    'Export Meter': export
                })

filteredSet = set()

filteredSet.update(
    item['Tariff Code']
    for item in metersList
    if item.get('Tariff Valid From') <= now
    and (item.get('Tariff Valid To') is None or item.get('Tariff Valid To') >= now)
    and 'agile' in item.get('Tariff Code', '').lower() #agile tarrif
    and not item.get('Export Meter', False) #import meter
)

if len(filteredSet) > 1:
    raise IndexError(f'The tarrif list has more codes than expected: \n {filteredSet}')

tariffCode = list(filteredSet)[0]

print(tariffCode)

url = ('https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/' + 
         'electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-N/standard-unit-rates/' + 
         '?period_from=2023-11-28T15:00Z&period_to=2023-11-28T15:30Z')
resultJSON = asyncio.run(apiCall(url))

print(json.dumps(resultJSON, indent=2, sort_keys=True))

# url = 'https://api.octopus.energy/v1/products'
# r = requests.get(url)
# output_dict = r.json()

# print(json.dumps(output_dict, indent=2, sort_keys=True))