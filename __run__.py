import inverter_control as ic
import inverter_dataset as id 
import octopus_agile as oa 
import asyncio

inverterValues = asyncio.run(id.datasetMain())

print(inverterValues)

prices = None
try:
    prices = asyncio.run(oa.mainReturnRates(1))
except ValueError as e:
    print(e)

print(prices)