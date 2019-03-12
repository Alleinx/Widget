# This program Get Weather data
# Version1
# TODO: modify data format and combine with apparent_temp

import requests
import json

r = requests.get('https://www.tianqiapi.com/api/?version=v1&cityid=101280701')
r.encoding = 'utf-8'

parsed_json = json.loads(r.text)
# print(parsed_json)


relative_humidity = parsed_json['data'][0]['humidity']
print('relative humidity: ' + str(relative_humidity))

for i in range(len(parsed_json['data'])):
    for j in range(len(parsed_json['data'][i]['hours'])):
        print(parsed_json['data'][i]['hours'][j])
# use hash-table to get value
 
#wind_level_to_speed_per_sec = dict({'<0级': 0.1},
#                                {'<1级': 0.8},
#                                {'<2级': 2.45}, 
#                                {'<3级': 4.4},
#                                {'<4级': 6.7},
#                                {'<5级': 9.35},
#                                {'<6级': 12.35},
#                                {'<7级': 15.5},
#                                {'<8级': 18.95},
#                                {'<9级': 22.6}, 
#                                {'<10级': 26.3})
