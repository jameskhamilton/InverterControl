import inverter_control as ic
import inverter_dataset as id 
import octopus_agile as oa 
import asyncio
import json

inverterValues = asyncio.run(id.datasetMain())

print(inverterValues)