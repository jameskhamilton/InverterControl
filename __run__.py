from libraries import inverter_control as ic
from libraries import inverter_dataset as id
from libraries import octopus_agile as oa
from libraries import database_control as dc
from datetime import datetime, time
import asyncio

current = datetime.now().time()

def control():
    
    inverterValues = asyncio.run(id.datasetMain())
    dc.inverterInsert(inverterValues)

    # insert prices for the following day at 6pm - todo - review this!
    if time(18, 0) <= current <= time(18, 10):
        prices = []
        try:
            prices = asyncio.run(oa.mainReturnRates(0))
        except ValueError as e:
            print(e)

        dc.octopusInsert(prices)