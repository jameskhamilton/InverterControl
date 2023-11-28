import requests 
import pandas as pd
import json
import http.client
import base64

filePath = 'C:\\test\\octopusSecurity.json'

with open(filePath, 'r') as file:
    securityData = json.load(file)

apiKey = securityData['apiKey']
accountNumber = securityData['accountNumber']

def apiCall(url, apiKey):
    authHeader = 'Basic ' + base64.b64encode(apiKey.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': authHeader,}

    # Parse the URL to extract the hostname and path
    urlParts = http.client.urlsplit(url)
    hostname = urlParts.hostname
    path = urlParts.path

    conn = http.client.HTTPSConnection(hostname)

    try:
        conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        if response.status >= 400:
            print(f'Error: {response.status} - {data}')
        else:
            return data
    except http.client.HTTPException as e:
        print(f'Error: {e}')
    finally:
        conn.close()

url = f'https://api.octopus.energy/v1/accounts/{accountNumber}/'
result = apiCall(url, apiKey)

resultJSON = json.loads(result)

print(json.dumps(resultJSON, indent=2, sort_keys=True))


# url = ('https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/' + 
#          'electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-N/standard-unit-rates/' + 
#          '?period_from=2023-11-28T15:00Z&period_to=2023-11-28T15:30Z')
# r = requests.get(url)
# output_dict = r.json()

#print(json.dumps(output_dict, indent=2, sort_keys=True))

# url = 'https://api.octopus.energy/v1/products'
# r = requests.get(url)
# output_dict = r.json()

# print(json.dumps(output_dict, indent=2, sort_keys=True))