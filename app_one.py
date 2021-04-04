import time, json, csv, random, requests
import paho.mqtt.client as mqtt
from datetime import datetime

# Wszystko co najnowsze odbywa się własnie w tej aplikacji !!!

with open("config_data", "r") as jsonFile:
    config_data = json.load(jsonFile)

avgOfAppOne = 0
config_data['app_one']['stop'] = "online"
config_data['app_one']['avg'] = "0"
config_data['overall']['heater'] = "Off"
config_data['app_one']['kom'] = ""

with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)

#open("templates/dataStructuredOfApp1", 'w').close()

def http_send(address, freq, source, avgOfAppOne):
    counter = 0
    dataCout = 0

    with open(source, 'r') as csv_file:
        data = list(csv.reader(csv_file))
        rows = sum(1 for _ in data)

    while True:
        with open('config_data', 'r') as f:
            data_config = json.load(f)

        temp = data[random.randint(1, rows-1)][2].split('"')[0].replace(",", ".")
        temp = float(temp)*float(data_config['app_one']['multiplier'])
        payload = {'id': 1, 'data': float(temp)}

        counter += 1
        dataCout += payload['data']
        avgOfAppOne = round(dataCout / counter, 1)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        print(avgOfAppOne)
        if avgOfAppOne > 20 and config_data['overall']['heater'] == "Off":
            print("za wysoki poziom komarow - włącz lampę!!!")
            config_data['app_one']['kom'] = "za wysoki poziom komarow - włącz lampę!!!"
            config_data['overall']['heater'] = "On"

            with open("templates/dataStructuredOfApp1", "a") as DataFile:
                nowInTime = datetime.now().strftime('%d/%m/20%y %H:%M')
                DataFile.write("id: " + str(payload["id"]) + " heater: " + config_data['overall']['heater'] + " time: " + str(nowInTime) + "\n")

            if avgOfAppOne - 10 <= 0:
                avgOfAppOne = 0
            else:
                avgOfAppOne -= 10
        elif avgOfAppOne > 20 and config_data['overall']['heater'] == "On":
            print("Za wysoki poziom komarow - Lampa On")
            config_data['app_one']['kom'] = "Za wysoki poziom komarow - Lampa On"
            if avgOfAppOne - 10 <= 0:
                avgOfAppOne = 0
            else:
                avgOfAppOne -= 10
        elif avgOfAppOne < 20:
            print("poziom komarow w normie :)")
            config_data['app_one']['kom'] = "poziom komarow w normie :)"
            config_data['overall']['heater'] = "Off"
            with open("templates/dataStructuredOfApp1", "a") as DataFile:
                nowInTime = datetime.now().strftime('%d/%m/20%y %H:%M')
                DataFile.write("id: " + str(payload["id"]) + " heater: " + config_data['overall']['heater'] + " time: " + str(nowInTime) +  "\n")
        print(config_data['overall']['heater'])

        print(avgOfAppOne)
        config_data['app_one']['avg'] = str(round(avgOfAppOne,2))
        config_data['app_one']['stop'] = "online"

        # ToDo: Wykonanie zapisu danych do sobengo pliku + godzina zapisu - LISTA 5
        with open("templates/dataStructuredOfApp1", "a") as DataFile:
            nowInTime = datetime.now().strftime('%d/%m/20%y %H:%M')
            DataFile.write("id: " + str(payload["id"]) + " data: " + str(payload["data"]) + " time: " + str(nowInTime) + "\n")


        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)
        requests.post(address, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        time.sleep(float(data_config['app_one']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_one']['stop'] == "offline":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_one']['stop'] = "offline"
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
        temp = float(temp) * float(data_config['app_one']['multiplier'])
        payload = {'id': 1, 'data': float(temp)}
        print(payload)

        counter += 1
        dataFor = payload['data']
        dataCout += int(dataFor)
        avgOfAppOne = round(dataCout / counter, 1)

        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)

        print(avgOfAppOne)
        if avgOfAppOne > 20 and config_data['overall']['heater'] == "Off":
            print("za wysoki poziom komarow - włącz lampę!!!")
            config_data['app_one']['kom'] = "za wysoki poziom komarow - włącz lampę!!!"
            config_data['overall']['heater'] = "On"
            if avgOfAppOne - 10 <= 0:
                avgOfAppOne = 0
            else:
                avgOfAppOne -= 10
        elif avgOfAppOne > 20 and config_data['overall']['heater'] == "On":
            print("Za wysoki poziom komarow - Lampa On")
            config_data['app_one']['kom'] = "Za wysoki poziom komarow - Lampa On"
            if avgOfAppOne - 10 <= 0:
                avgOfAppOne = 0
            else:
                avgOfAppOne -= 10
        elif avgOfAppOne < 20:
            print("poziom komarow w normie :)")
            config_data['app_one']['kom'] = "poziom komarow w normie :)"
            config_data['overall']['heater'] = "Off"
        print(config_data['overall']['heater'])

        config_data['app_one']['avg'] = str(avgOfAppOne)
        config_data['app_one']['stop'] = "online"

        # ToDo: Wykonanie zapisu danych do sobengo pliku + godzina zapisu - LISTA 5
        with open("templates/dataStructuredOfApp1", "a") as DataFile:
            nowInTime = datetime.now().strftime('%y/%m/%d %H:%M:%S')
            DataFile.write("id: " + str(payload["id"]) + " data: " + str(payload["data"]) + " time: " + str(nowInTime) + "\n")

        with open("config_data", "w") as jsonFile:
            json.dump(config_data, jsonFile)
        payload = json.dumps(payload)
        send(payload, client, topic)
        time.sleep(float(data_config['app_one']['freq']))
        with open("config_data", "r") as jsonFile:
            config_data = json.load(jsonFile)
        if config_data['app_one']['stop'] == "stop":
            with open("config_data", "r") as jsonFile:
                config_data = json.load(jsonFile)
            config_data['app_one']['stop'] = "offline"
            with open("config_data", "w") as jsonFile:
                json.dump(config_data, jsonFile)
            exit()


with open('config_data', 'r') as f:
    data_config = json.load(f)

if data_config['app_one']['send_type'] == "http":
    http_send(f"http://127.0.0.1:{data_config['overall']['port']}/{data_config['overall']['adress_http']}", data_config['app_one']['freq'], f"{data_config['app_one']['path_csv']}",avgOfAppOne)
elif data_config['app_one']['send_type']:
    mqtt_send(f"{data_config['overall']['adress_mqtt']}",f"{data_config['overall']['topic_mqtt']}", data_config['app_one']['freq'], f"{data_config['app_one']['path_csv']}")