# This program Get Weather data
# Version1
# TODO: modify data format and combine with apparent_temp

import requests
import json

r = requests.get('https://www.tianqiapi.com/api/?version=v1&cityid=101280701')
r.encoding = 'utf-8'

parsed_json = json.loads(r.text)
# print(parsed_json)

for i in range(len(parsed_json['data'])):
    for j in range(len(parsed_json['data'][i]['hours'])):
        print(parsed_json['data'][i]['hours'][j])

# relative_humidity = parsed_json['data'][0]['humidity']
# use hash-table to get value
 
