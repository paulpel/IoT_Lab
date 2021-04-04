from flask import Flask, request, abort, Response
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config["DEBUG"] = False

app.config['MQTT_BROKER_URL'] = "test.mosquitto.org"
mqtt = Mqtt(app)

with open('config_data', 'r') as f:
    data_config = json.load(f)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(data_config['overall']['topic_mqtt'])


@mqtt.on_message()
def mqtt_message(client, userdata, message):
    data = json.loads(message.payload)
    id = data['id']
    data = data['data']
    if id is None or data is None:
        abort(400)  # missing arguments
    stats(id, data)

def getAndReturn(dataOne,dataTwo):
    return dataOne/dataTwo


@app.route('/test', methods=['POST'])
def new_data():
    id = request.json.get('id')
    data = request.json.get('data')
    print(id,": ", data)
    if data is None:
        abort(400)  # missing arguments
    stats(id, data)
    return Response(status=201)


def stats(id, data):
    if id == 1:
        stat_data1.append((data))
    elif id == 2:
        stat_data2.append((data))
    elif id == 3:
        stat_data3.append(data)
        count_string.append(stat_data3[-1].count(data_config['overall']['char_chain']))
    elif id == 4:
        stat_data4.append(data)
    elif id == 5:
        stat_data5.append(data)



    print("\n" + "*"*50 + "STATYSTYKA START"+"*"*50)
    if stat_data1:
        print("Zagregowane dane z 1 aplikacji " + str(stat_data1))
        print("Liczba odebranych danych z 1 aplikacji: " + str(len(stat_data1)))
        print("Średnia zachorowań na malarie na 100 000 mieszkanców: " + str(sum(stat_data1) / len(stat_data1)))
    if stat_data2:
        print("\nZagregowane dane z 2 aplikacji" + str(stat_data2))
        print("Liczba odebranych danych z 2 aplikacji: " + str(len(stat_data2)))
        print(f"Średnia litrów trunku nr {data_config['overall']['drink_choice']} na osobę na swiecie przez rok: " + str(sum(stat_data2) / len(stat_data2)))
    if stat_data3:
        print("\nZagregowane dane z 3 aplikacji" + str(stat_data3))
        print("Liczba odebranych danych z 3 aplikacji: " + str(len(stat_data3)))
        print(f"Ciąg znaków \"{data_config['overall']['char_chain']}\" występuje:  " + str(sum(count_string)) + " razy.")
    if stat_data4:
        print("\nZagregowane dane z 4 aplikacji" + str(stat_data4))
        print("Liczba odebranych danych z 4 aplikacji: " + str(len(stat_data4)))
        print("Srednia liczba recenzji na jeden film według rottentomatoes: " + str(sum(stat_data4)/len(stat_data4)))
    if stat_data5:
        print("\nZagregowane dane z 5 aplikacji" + str(stat_data5))
        print("Liczba odebranych danych z 5 aplikacji: " + str(len(stat_data5)))
        print("Srednia liczba indyjskich studentów w jednym kraju: " + str(sum(stat_data5)/len(stat_data5)))

    print("*"*116+"\n")


count_string = []
stat_data1 = []
statystykaApki1 = 0
stat_data2 = []
statystykaApki2 = 0
stat_data3 = []
statystykaApki3 = 0
stat_data4 = []
statystykaApki4 = 0
stat_data5 = []
statystykaApki5 = 0


app.run(port=6000)