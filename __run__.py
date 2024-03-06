from libraries import inverter_control as ic
from libraries import inverter_dataset as id
from libraries import octopus_agile as oa
from libraries import database_control as dc
from datetime import datetime, time
import asyncio
import logging

def control():
    
    inverterValues = asyncio.run(id.datasetMain())
    try:
        dc.inverterInsert(inverterValues)
        logging.info('Inverter Insert Finished.')
    except Exception as e:
        logging.error(f'Inverter Insert Failed. {e}')

    # insert prices for the following day at around 4pm - todo: review this!
    current = datetime.now().time()
    if time(16, 0) <= current <= time(16, 30):
        prices = []
        try:
            prices = asyncio.run(oa.mainReturnRates(1))
        except ValueError as e:
            print(e)

        dc.octopusInsert(prices)

    return inverterValues

if __name__ == '__main__':
    control()