import asyncio
import json
import octopus_functions as of
from datetime import datetime, timezone, timedelta

apiKey, accountNumber = of.secrets()

async def mainReturnRates(dateOffsetValue: int) -> json:
    """
    Parameters:
    - int value to offset the date when getting price values
    - pass 1 to look at tomorrow
    - pass 0 to look at today
    """
    now = datetime.now(timezone.utc)
    hour = now.hour
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

    print(json.dumps(agileDataset, indent=2, sort_keys=True))
    return agileDataset

if __name__ == '__main__':
    try:
        asyncio.run(mainReturnRates(1))
    except ValueError as e:
        print(e)