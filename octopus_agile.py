import asyncio
import json
import http.client
import base64
from datetime import datetime, timezone, timedelta

filePath = 'C:\\test\\octopusSecurity.json'
with open(filePath, 'r') as file:
    securityData = json.load(file)

apiKey = securityData['apiKey']
accountNumber = securityData['accountNumber']
tarrifType = 'agile'

now = datetime.now(timezone.utc)

def parseDatetime(datetimeString: str) -> datetime:
    """
    Parameter:
    - datetime value as a string

    Returns:
    - datetime value yyyy-mm-dd hh:mm:ss z
    """
    try:
        return datetime.strptime(datetimeString, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        pass
    raise ValueError(f'Unsupported datetime format: {datetimeString}')

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

def parseTarrifDataset(jsonValue: json) -> list:
    properties = jsonValue['properties']
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

    return metersList

def agileTarrif(datasetValue: list) -> str:
    filteredSet = set()
    filteredSet.update(
        item['Tariff Code']
        for item in datasetValue
        if item.get('Tariff Valid From') <= now
        and (item.get('Tariff Valid To') is None or item.get('Tariff Valid To') >= now)
        and tarrifType.lower() in item.get('Tariff Code', '').lower() #agile tarrif
        and not item.get('Export Meter', False) #import meter
    )

    if len(filteredSet) > 1:
        raise IndexError(f'The tarrif list has more codes than expected: \n {filteredSet}')
    else:
        return list(filteredSet)[0]

def productCode(tarrifCodeValue: str) -> str:
    # split the string based on known prefixes
    parts = tarrifCodeValue.split('-')
    # find the index of "AGILE"
    agileIndex = parts.index(tarrifType.upper())
    # extract the relevant parts to exclude the last value
    product = '-'.join(parts[agileIndex:]).rsplit('-', 1)[0]

    if not(product):
        raise IndexError(f'Pattern not found to extract the product from the tarrif code: \n {tarrifCodeValue}')
    else:
        return product

async def mainOctopusDataset() -> json:
    tomorrow = now + timedelta(days=1)
    tomorrowFormatted = tomorrow.strftime('%Y-%m-%d')

    url = f'https://api.octopus.energy/v1/accounts/{accountNumber}/'
    tarrifsDataset = await asyncio.run(apiCall(url, apiKey))

    # tarrifList = parseTarrifDataset(tarrifsDataset)

    # tarrifCode = agileTarrif(tarrifList)

    # product = productCode(tarrifCode)

    # url = f'https://api.octopus.energy/v1/products/{product}/electricity-tariffs/{tarrifCode}/standard-unit-rates/?period_from={tomorrowFormatted}T00:00Z&period_to={tomorrowFormatted}T23:59Z'
    # agileDataset = asyncio.run(apiCall(url))

    # print(json.dumps(agileDataset, indent=2, sort_keys=True))
    # return agileDataset

    print(tarrifsDataset)

asyncio.run(mainOctopusDataset())