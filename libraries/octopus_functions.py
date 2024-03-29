import json
import http.client
import base64
from datetime import datetime
import os

tarrifType = 'agile'

def secrets() -> tuple:
    """
    Returns:
     
    apiKey, accountNumber
    """
    directoryFolder = 'credentials'
    inverterFile = 'octopus_config.json'
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    parentDirectory = os.path.abspath(os.path.join(scriptDirectory, os.pardir))

    filePath = os.path.join(parentDirectory, directoryFolder, inverterFile)
    
    with open(filePath, 'r') as file:
        securityData = json.load(file)

    apiKey = securityData['API Key']
    accountNumber = securityData['Account Number']

    return apiKey, accountNumber

def parseDatetime(datetimeValue: str) -> datetime:
    """
    Parameter:
    - datetime value as a string

    Returns:
    - datetime value yyyy-mm-dd hh:mm:ss z
    """
    if datetimeValue is None:
        return None
    try:
        return datetime.strptime(datetimeValue, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        pass
    raise ValueError(f'Unsupported datetime format: {datetimeValue}')

async def apiCall(urlValue: str, apiKeyValue: str = None) -> json:
    """
    Parameter:
    - url
    - api key (optional - when included this builds the Authorization string, otherwise no Authorization is passed)

    Returns:
    - JSON dataset
    """
    # Parse the URL to extract the hostname and path
    urlParts = http.client.urlsplit(urlValue)
    hostname = urlParts.hostname
    path = urlParts.path

    conn = http.client.HTTPSConnection(hostname)

    try:
        if apiKeyValue is None:
            conn.request('GET', urlValue)
        else:
            authHeader = 'Basic ' + base64.b64encode(apiKeyValue.encode('utf-8')).decode('utf-8')
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

def parseTarrifDataset(jsonValue: json) -> dict:
    """
    Parameter:
    - takes the json result from Octopus account call
    - json includes the past and current products held

    Returns:
    - a dict containing products held and when they were held
    """
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

def parseAgileCode(datasetValue: list, nowValue: datetime) -> str:
    """
    Parameter:
    - dict of products held and when they were held
    - current date time

    Returns:
    - a filtered list for current products with AGILE in the name
    - the result should be 1 value and throws an error otherwise
    - assuming you only have 1 meter with 1 agile tarrif
    """
    filteredSet = set()

    validFromCondition = lambda item: item.get('Tariff Valid From') <= nowValue
    validToCondition = lambda item: item.get('Tariff Valid To') is None or item.get('Tariff Valid To') >= nowValue
    tariffTypeCondition = lambda item: tarrifType.lower() in item.get('Tariff Code', '').lower()
    exportMeterCondition = lambda item: not item.get('Export Meter', False)

    filteredSet.update(
        item['Tariff Code']
        for item in datasetValue
        if validFromCondition(item)
        and validToCondition(item)
        and tariffTypeCondition(item)
        and exportMeterCondition(item)
    )

    if len(filteredSet) > 1:
        raise IndexError(f'The tarrif list has more codes than expected: \n {filteredSet}')
    else:
        return list(filteredSet)[0]

def parseProductCode(tarrifCodeValue: str) -> str:
    """
    Parameter:
    - string with the AGILE tarrif code

    Returns:
    - the agile tarrif product code which doesn't contain regional values
    """
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
    
def parsePrices(agileDatasetValue: json) -> list:
    """
    Parameters:
    - json from the call for prices

    Returns:
    - a list containing the prices for each time period
    """
    records = []

    for record in agileDatasetValue['results']:
        priceExclVAT = record['value_exc_vat']
        priceInclVAT = record['value_inc_vat']
        fromDateTime = record['valid_from']
        toDateTime = record['valid_to']

        records.append({
                'priceExclVAT': priceExclVAT,
                'priceInclVAT': priceInclVAT,
                'fromDateTime': fromDateTime,#datetime.strptime(fromDateTime.split(' (UTC')[0], '%Y-%m-%d %H:%M:%S'),
                'toDateTime': toDateTime#datetime.strptime(toDateTime.split(' (UTC')[0], '%Y-%m-%d %H:%M:%S')
        })

    return records