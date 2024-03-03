import inverter_control as ic
import inverter_dataset as id
import octopus_agile as oa
import database_control as dc
import asyncio

inverterValues = asyncio.run(id.datasetMain())
dc.inverterInsert(inverterValues)

# prices = None
# try:
#     prices = asyncio.run(oa.mainReturnRates(1))
# except ValueError as e:
#     print(e)

# print(prices)