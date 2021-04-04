import json
import os

with open("config_data", "r") as jsonFile:
    config_data = json.load(jsonFile)


config_data['app_three']['freq'] = 1

with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)

print('hello')

# apki= ['app_one', 'app_two', 'app_three', 'app_four','app_five']
# with open("config_data", "r") as jsonFile:
#     config_data = json.load(jsonFile)
#
# for index in range(5):
#     config_data[apki[index]]['stop'] = 'offline'
#
with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)
