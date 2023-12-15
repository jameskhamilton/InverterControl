import inverter_control as ic
import inverter_dataset as id
import inverter_functions as inf
import octopus_agile as oa 
import octopus_functions as of
import user_input as ui
import asyncio

if not inf.credentialFile('credentials', 'inverter_config.json'):
    print('No file')

inverterValues = asyncio.run(id.datasetMain())

print(inverterValues)

prices = None
try:
    prices = asyncio.run(oa.mainReturnRates(1))
except ValueError as e:
    print(e)

print(prices)