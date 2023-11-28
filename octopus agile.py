import requests 
import pandas as pd
import json

filePath = 'C:\\test\\octopusSecurity.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

apiKey = securityData['apiKey']
accountNumber = securityData['accountNumber']

url = f'https://api.octopus.energy/v1/accounts/{accountNumber}/'
r = requests.get(url, auth=(apiKey,''))
output_dict = r.json()

print(json.dumps(output_dict, indent=2, sort_keys=True))


url = ('https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/' + 
         'electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-N/standard-unit-rates/' + 
         '?period_from=2023-11-28T15:00Z&period_to=2023-11-28T15:30Z')
r = requests.get(url)
output_dict = r.json()

print(json.dumps(output_dict, indent=2, sort_keys=True))

# url = 'https://api.octopus.energy/v1/products'
# r = requests.get(url)
# output_dict = r.json()

# print(json.dumps(output_dict, indent=2, sort_keys=True))