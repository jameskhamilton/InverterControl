import asyncio
import json
import octopus_functions as of
from datetime import datetime, timezone, timedelta

apiKey, accountNumber = of.secrets()

def parsePrices(agileDataset: json) -> list:
    """
    Parameters:
    - json from the call for prices

    Returns:
    - a list containing the prices for each time period
    """
    records = []

    for record in agileDataset['results']:
        priceExclVAT = record['value_exc_vat']
        priceInclVAT = record['value_inc_vat']
        fromDateTime = record['valid_from']
        toDateTime = record['valid_to']

        records.append({
                'priceExclVAT': priceExclVAT,
                'priceInclVAT': priceInclVAT,
                'fromDateTime': fromDateTime,
                'toDateTime': toDateTime
        })

    return records

async def mainReturnRates(dateOffsetValue: int) -> json:
    """
    Parameters:
    - int value to offset the date when getting price values
    - pass 1 to look at tomorrow
    - pass 0 to look at today
    """
    now = datetime.now(timezone.utc)
    dateOffset = now + timedelta(days=dateOffsetValue)
    dateOffsetFormatted = dateOffset.strftime('%Y-%m-%d')

    if dateOffsetValue > 1:
        raise ValueError("Cannot check for prices more than 1 day in advance.")

    url = f'https://api.octopus.energy/v1/accounts/{accountNumber}/'
    tarrifsDataset = await of.apiCall(url, apiKey)

    tarrifList = of.parseTarrifDataset(tarrifsDataset)
    
    try:
        tarrifCode = of.parseAgileCode(tarrifList, now)
    except IndexError as e:
        print(e)
    try:
        product = of.parseProductCode(tarrifCode)
    except IndexError as e:
        print(e)

    url = f'https://api.octopus.energy/v1/products/{product}/electricity-tariffs/{tarrifCode}/standard-unit-rates/?period_from={dateOffsetFormatted}T00:00Z&period_to={dateOffsetFormatted}T23:59Z'
    agileDataset = await of.apiCall(url)

    if agileDataset['count'] == 0:
        raise ValueError(f"Prices aren't available yet for {dateOffsetFormatted}")

    result = parsePrices(agileDataset)

    return result

if __name__ == '__main__':
    try:
        asyncio.run(mainReturnRates(1))
    except ValueError as e:
        print(e)