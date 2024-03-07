from libraries import inverter_control as ic
from libraries import inverter_dataset as id
from libraries import octopus_agile as oa
from libraries import database_control as dc
from datetime import datetime, time
import asyncio
import logging

def octopusControl(timeFrom: list, timeTo: list, dayOffset: int) -> None:
    # insert prices for the following day at around 4pm - todo: review this!
    current = datetime.now().time()
    if time(timeFrom[0], timeFrom[1]) <= current <= time(timeTo[0], timeTo[1]):
        prices = []
        try:
            prices = asyncio.run(oa.mainReturnRates(dayOffset))
        except ValueError as e:
            print(e)

        dc.octopusInsert(prices)

def control():
    
    inverterValues = asyncio.run(id.datasetMain())
    try:
        dc.inverterInsert(inverterValues)
        logging.info('Inverter Insert Finished.')
    except Exception as e:
        logging.error(f'Inverter Insert Failed. {e}')

    #get tomorrow prices
    octopusControl([4,0],[4,30],1)
    #get today prices to catch 23:30 - 00:00
    octopusControl([0,0],[0,10],0)

    return inverterValues

if __name__ == '__main__':
    control()