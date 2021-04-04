import time, json, csv, random, requests
import paho.mqtt.client as mqtt

with open("config_data", "r") as jsonFile:
    config_data = json.load(jsonFile)


avgOfAppTwo = 0
config_data['app_two']['stop'] = "online"
config_data['app_two']['avg'] = "0"

with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)

def http_send(address, freq, source):
    counter = 0
    with open(source, 'r') as csv_file:
        data = list(csv.reader(csv_file))
        rows = sum(1 for _ in data)



    while True:
        with open('config_data', 'r') as f:
            data_config = json.load(f)

        temp = data[random.randint(1, rows-1)][2].split('"')[0].replace(",", ".")
        temp = str(temp) * int(data_config['app_three']['multiplier'])
        payload = {'id': 3, 'data': str(temp)}
        print(payload)

        counter += 1
        avgOfAppTwo = round(counter, 1)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        config_data['app_three']['avg'] = str(avgOfAppTwo)
        config_data['app_three']['stop'] = "online"

        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)
        requests.post(address,headers = {'Content-Type': 'application/json'}, data=json.dumps(payload))
        time.sleep(float(data_config['app_three']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_three']['stop'] == "offline":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_three']['stop'] = "offline"
            with open("config_data", "w") as jsonFile:
                json.dump(config_data, jsonFile)
            exit()

def mqtt_send(address, topic, freq, source):
    counter = 0


    def send(content, client, address):
        client.publish(address, content)


    with open(source, 'r') as csv_file:
        data = list(csv.reader(csv_file))
        rows = sum(1 for _ in data)



    broker_adress = address
    client = mqtt.Client("APP1")
    client.connect(broker_adress)
    client.loop_start()

    while True:
        with open('config_data', 'r') as f:
            data_config = json.load(f)

        temp = data[random.randint(1, rows - 1)][2].split('"')[0].replace(",", ".")
        temp = str(temp) * int(data_config['app_three']['multiplier'])
        payload = json.dumps({'id': 3, 'data': str(temp)})
        print(payload)

        counter += 1

        avgOfAppTwo = round(counter, 1)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        config_data['app_three']['avg'] = str(avgOfAppTwo)
        config_data['app_three']['stop'] = "online"

        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)

        send(payload, client, topic)
        time.sleep(float(data_config['app_three']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_three']['stop'] != "offline":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_three']['stop'] = "offline"
            with open("config_data", "w") as jsonFile:
                json.dump(config_data, jsonFile)
            exit()

with open('config_data', 'r') as f:
    data_config = json.load(f)

if data_config['app_three']['send_type'] == "http":
    http_send(f"http://127.0.0.1:{data_config['overall']['port']}/{data_config['overall']['adress_http']}", data_config['app_three']['freq'], f"{data_config['app_three']['path_csv']}")
elif data_config['app_three']['send_type']:
    mqtt_send(f"{data_config['overall']['adress_mqtt']}",f"{data_config['overall']['topic_mqtt']}", data_config['app_three']['freq'], f"{data_config['app_three']['path_csv']}")