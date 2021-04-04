import time, json, csv, random, requests
import paho.mqtt.client as mqtt
from datetime import datetime

with open("config_data", "r") as jsonFile:
    config_data = json.load(jsonFile)

avgOfAppTwo = 0
config_data['app_two']['stop'] = "online"
config_data['app_two']['avg'] = "0"

with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)



def http_send(address, freq, source):
    counter = 0
    dataCout = 0
    with open(source, 'r') as csv_file:
        data = list(csv.reader(csv_file))
        rows = sum(1 for _ in data)


    while True:
        with open('config_data', 'r') as f:
            data_config = json.load(f)
        temp = data[random.randint(1, rows-1)][2].split('"')[0].replace(",", ".")
        temp = float(temp) * float(data_config['app_two']['multiplier'])
        payload = {'id': 2, 'data': float(temp)}
        print(payload)

        counter += 1
        dataCout += payload['data']
        avgOfAppTwo = round(dataCout/counter, 1)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        config_data['app_two']['avg'] = str(avgOfAppTwo)
        config_data['app_two']['stop'] = "online"

        # ToDo: Wykonanie zapisu danych do sobengo pliku + godzina zapisu - LISTA 5
        with open("templates/dataStructuredOfApp2", "a") as DataFile:
            nowInTime = datetime.now().strftime('%d/%m/20%y %H:%M')
            DataFile.write( "id: " + str(payload["id"]) + " data: " + str(payload["data"]) + " time: " + str(nowInTime) + "\n")

        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)
        requests.post(address,headers = {'Content-Type': 'application/json'}, data=json.dumps(payload))
        time.sleep(float(data_config['app_two']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_two']['stop'] == "offline":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_two']['stop'] = "offline"
            with open("config_data", "w") as jsonFile:
                json.dump(config_data, jsonFile)
            exit()

def mqtt_send(address, topic, freq, source):
    counter = 0
    dataCout = 0

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
        temp = float(temp) * float(data_config['app_two']['multiplier'])
        payload = {'id': 2, 'data': float(temp)}
        counter += 1
        dataCout += payload['data']
        avgOfAppTwo = round(dataCout / counter, 1)
        print(payload)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        config_data['app_two']['avg'] = str(avgOfAppTwo)
        config_data['app_two']['stop'] = "online"

        # ToDo: Wykonanie zapisu danych do sobengo pliku + godzina zapisu - LISTA 5
        with open("templates/dataStructuredOfApp2", "a") as DataFile:
            nowInTime = datetime.now().strftime('%H:%M:%S')
            DataFile.write(str(payload["id"]) + " " + str(payload["data"]) + " " + str(nowInTime) + "\n")


        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)
        payload = json.dumps(payload)
        send(payload, client, topic)
        time.sleep(float(data_config['app_two']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_two']['stop'] == "offline":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_two']['stop'] = "offline"
            with open("config_data", "w") as jsonFile:
                json.dump(config_data, jsonFile)
            exit()

with open('config_data', 'r') as f:
    data_config = json.load(f)

if data_config['app_two']['send_type'] == "http":
    http_send(f"http://127.0.0.1:{data_config['overall']['port']}/{data_config['overall']['adress_http']}", data_config['app_two']['freq'], f"{data_config['app_two']['path_csv']}")
elif data_config['app_two']['send_type']:
    mqtt_send(f"{data_config['overall']['adress_mqtt']}",f"{data_config['overall']['topic_mqtt']}", data_config['app_two']['freq'], f"{data_config['app_two']['path_csv']}")