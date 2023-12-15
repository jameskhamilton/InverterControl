import asyncio
import json
import octopus_functions as of
from datetime import datetime, timezone, timedelta

apiKey, accountNumber = of.secrets()
now = datetime.now(timezone.utc)

async def mainReturnRates() -> json:
    tomorrow = now + timedelta(days=1)
    tomorrowFormatted = tomorrow.strftime('%Y-%m-%d')

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

    url = f'https://api.octopus.energy/v1/products/{product}/electricity-tariffs/{tarrifCode}/standard-unit-rates/?period_from={tomorrowFormatted}T00:00Z&period_to={tomorrowFormatted}T23:59Z'
    agileDataset = await of.apiCall(url)

    print(json.dumps(agileDataset, indent=2, sort_keys=True))
    return agileDataset

if __name__ == '__main__':
    asyncio.run(mainReturnRates())