from flask import Flask, request, render_template,redirect
import json
from flask import Flask
from flask import send_file
import downloadDataFile


with open("config_data", "r") as jsonFile:
    config_data = json.load(jsonFile)

apki = ['app_one', 'app_two', 'app_three', 'app_four', 'app_five']

for index in range(5):
    config_data[apki[index]]['stop'] = "offline"

with open("config_data", "w") as jsonFile:
    json.dump(config_data, jsonFile)

app = Flask(__name__)

@app.route('/setPara' , methods =["GET", "POST"])
def download_form():
    if request.method == "POST":
        day = request.form.get("day0")
        month = request.form.get("month0")
        year = request.form.get("year0")
        start = request.form.get("start0")
        end = request.form.get("end0")
        whichApp = request.form.get("appToDownload")
    ovverriteDownload(day, month, year, start, end, whichApp)
    return render_template("getData.html")


@app.route('/fetchData')
def fetch_form():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('getData.html', variable=data)

@app.route('/info')
def another_form():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/')
def starter_form():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('config.html', variable=data)


@app.route('/Heater')
def heat():
    with open("config_data", "r") as jsonFile:
        config_data = json.load(jsonFile)

    if config_data['overall']['heater'] == "Off":
        config_data['overall']['heater'] = "On"

    else:
        config_data['overall']['heater'] = "Off"

    with open("config_data", "w") as jsonFile:
        json.dump(config_data, jsonFile)
    return render_template('info.html', variable=config_data)


@app.route('/settings')
def go_back():
    with open("config_data", "r") as jsonFile:
        config_data = json.load(jsonFile)
    with open("config_data", "w") as jsonFile:
        json.dump(config_data, jsonFile)
    return render_template('config.html')


@app.route('/getDataOne')
def getDataOne():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/getDataTwo')
def getDataTwo():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/getDataThree')
def getDataThree():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/getDataFour')
def getDataFour():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/getDataFive')
def getDataFive():
    with open("config_data", "r") as jsonFile:
        data = json.load(jsonFile)
    return render_template('info.html', variable=data)


@app.route('/app0', methods=["GET", "POST"])
def appOne():
    if request.method == "POST":
        freq = request.form.get("freq0")
        multi = request.form.get("multi0")
        start = request.form.get("start0")
        source = request.form.get("source0")
        NEWoverwrite(freq, source, multi, start, 0)
    return render_template("config.html")


@app.route('/app1', methods =["GET", "POST"])
def appTwo():
    if request.method == "POST":
        freq = request.form.get("freq1")
        multi = request.form.get("multi1")
        start = request.form.get("start1")
        source = request.form.get("source1")
        NEWoverwrite(freq, source, multi, start, 1)
    return render_template("config.html")


@app.route('/app2', methods =["GET", "POST"])
def appThree():
    if request.method == "POST":
        freq = request.form.get("freq2")
        multi = request.form.get("multi2")
        start = request.form.get("start2")
        source = request.form.get("source2")
        NEWoverwrite(freq, source, multi, start, 2)
    return render_template("config.html")


@app.route('/app3', methods =["GET", "POST"])
def appFour():
    if request.method == "POST":
        freq = request.form.get("freq3")
        multi = request.form.get("multi3")
        start = request.form.get("start3")
        source = request.form.get("source3")
        NEWoverwrite(freq, source, multi, start, 3)
    return render_template("config.html")


@app.route('/app4', methods =["GET", "POST"])
def appFive():
    if request.method == "POST":
        freq = request.form.get("freq4")
        multi = request.form.get("multi4")
        start = request.form.get("start4")
        source = request.form.get("source4")
        NEWoverwrite(freq, source, multi, start, 4)
    return render_template("config.html")

def ovverriteDownload(day, month, year, start, end, whichApp):
    with open("config_download", "r") as jsonFile:
        config_data = json.load(jsonFile)

        if whichApp != "":
            config_data['app_one_download']['whichApp'] = whichApp
        else:
            config_data['app_one_download']['whichApp'] = "1"

        if day != "":
            config_data['app_one_download']['day'] = day
        else:
            config_data['app_one_download']['day'] = "1"

        if month != "":
            config_data['app_one_download']['month'] = month
        else:
            config_data['app_one_download']['month'] = "01"

        if year != "":
            config_data['app_one_download']['year'] = year
        else:
            config_data['app_one_download']['year'] = "2021"

        if start != "":
            config_data['app_one_download']['start'] = start
        else:
            config_data['app_one_download']['start'] = "10:10"

        if end != "":
            config_data['app_one_download']['end'] = end
        else:
            config_data['app_one_download']['end'] = "22:10"

    with open("config_download", "w") as jsonFile:
        json.dump(config_data, jsonFile)



def NEWoverwrite(freq, send_type, multiplier, stop, whichApp):
    apki = ['app_one', 'app_two', 'app_three', 'app_four','app_five']
   # online = [0,0,0,0,0]
    with open("config_data", "r") as jsonFile:
        config_data = json.load(jsonFile)

        if freq != "":
            config_data[apki[whichApp]]['freq'] = freq
            config_data[apki[whichApp]]['stop'] = "online"
        else:
            config_data[apki[whichApp]]['freq'] = 1
            config_data[apki[whichApp]]['stop'] = "online"

        if send_type != "":
            config_data[apki[whichApp]]['send_type'] = send_type
            config_data[apki[whichApp]]['stop'] = "online"
        else:
            config_data[apki[whichApp]]['send_type'] = "http"
            config_data[apki[whichApp]]['stop'] = "online"

        if multiplier != "":
            config_data[apki[whichApp]]['multiplier'] = multiplier
            config_data[apki[whichApp]]['stop'] = "online"
        else:
            config_data[apki[whichApp]]['multiplier'] = 1
            config_data[apki[whichApp]]['stop'] = "online"

        if stop == "stop":
            config_data[apki[whichApp]]['stop'] = "offline"

    with open("config_data", "w") as jsonFile:
        json.dump(config_data, jsonFile)


app.run(port=9000, debug=False)