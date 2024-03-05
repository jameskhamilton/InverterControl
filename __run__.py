from libraries import inverter_control as ic
from libraries import inverter_dataset as id
from libraries import octopus_agile as oa
from libraries import database_control as dc
import asyncio

inverterValues = asyncio.run(id.datasetMain())
dc.inverterInsert(inverterValues)

prices = []
try:
    prices = asyncio.run(oa.mainReturnRates(0))
except ValueError as e:
    print(e)

dc.octopusInsert(prices)