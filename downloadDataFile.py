from flask import Flask
from flask import send_file
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
plt.switch_backend('agg')

app = Flask(__name__)
@app.route('/download')
def downloadFile ():
    apki = ['dataStructuredOfApp1', 'dataStructuredOfApp2', 'dataStructuredOfApp3', 'dataStructuredOfApp4','dataStructuredOfApp5']
    apkiDownload = ["dataStructuredOfApp1toDownloadReady.txt","dataStructuredOfApp2toDownloadReady.txt","dataStructuredOfApp3toDownloadReady.txt","dataStructuredOfApp4toDownloadReady.txt","dataStructuredOfApp5toDownloadReady.txt"]
    with open("config_download", "r") as jsonFile:
        config_data = json.load(jsonFile)
    choosenAppNumber = int(config_data['app_one_download']['whichApp'])
    chossenAppName = apki[choosenAppNumber-1]
    chossenAppDownloadPath = apkiDownload[choosenAppNumber-1]
    ArrayOfDataForPlot = []
    path = "filesToDownload/" + chossenAppDownloadPath
    open("filesToDownload/" + chossenAppDownloadPath, 'w').close()
    # 5 indeks to data
    # 6 indeks to czas
    # app.run(port=5005, debug=True)
    with open('templates/' + chossenAppName) as f:
        matrix = [line.split() for line in f]
    # Wyciąganie danych które określą zakres
    with open("config_download", "r") as jsonFile:
        config_data = json.load(jsonFile)
        dataGivenByUser = config_data["app_one_download"]['day'] + "/" + config_data["app_one_download"][
            'month'] + "/" + config_data["app_one_download"]['year']
        print(dataGivenByUser)
        # Określanie czasu
        startTimeGivenByUser = config_data["app_one_download"]['start']
        print(startTimeGivenByUser)
        endTimeGivenByUser = config_data["app_one_download"]['end']
        print(endTimeGivenByUser)
    for items in range(len(matrix)):
        dane = matrix[items][3]
        data = matrix[items][5]
        czas = matrix[items][6]
        if data == dataGivenByUser:
            if czas >= startTimeGivenByUser and czas <= endTimeGivenByUser:
                output = ""
                for elem in range(7):
                    output += matrix[items][elem] + " "
                # tworzenie wykresu z danych
                ArrayOfDataForPlot += dane
                with open("filesToDownload/" + chossenAppDownloadPath, "a") as DataFile:
                    DataFile.write(output + "\n")
                print(output)
                output = ""
    return send_file(path, as_attachment=True)



@app.route('/downloadPlot')
def downloadPlot():
    apki = ['dataStructuredOfApp1', 'dataStructuredOfApp2', 'dataStructuredOfApp3', 'dataStructuredOfApp4',
            'dataStructuredOfApp5']
    apkiPlot = ['plotOfApp1.png', 'plotOfApp2.png', 'plotOfApp3.png', 'plotOfApp4.png',
            'plotOfApp5.png']
    with open("config_download", "r") as jsonFile:
        config_data = json.load(jsonFile)
    choosenAppNumber = int(config_data['app_one_download']['whichApp'])
    chossenAppName = apkiPlot[choosenAppNumber - 1]
    longPath =  apki[choosenAppNumber - 1]
    ArrayOfDataForPlot = []
    path = "filesToDownload/" + chossenAppName
    # 5 indeks to data
    # 6 indeks to czas
    # app.run(port=5005, debug=True)
    with open('templates/' + longPath) as f:
        matrix = [line.split() for line in f]
    # Wyciąganie danych które określą zakres
    with open("config_download", "r") as jsonFile:
        config_data = json.load(jsonFile)
        dataGivenByUser = config_data["app_one_download"]['day'] + "/" + config_data["app_one_download"][
            'month'] + "/" + config_data["app_one_download"]['year']
        print(dataGivenByUser)
        # Określanie czasu
        startTimeGivenByUser = config_data["app_one_download"]['start']
        print(startTimeGivenByUser)
        endTimeGivenByUser = config_data["app_one_download"]['end']
        print(endTimeGivenByUser)
    for items in range(len(matrix)):
        if matrix[items][2] == "data:":
            dane = matrix[items][3]
            data = matrix[items][5]
            czas = matrix[items][6]
            if data == dataGivenByUser:
                if czas >= startTimeGivenByUser and czas <= endTimeGivenByUser:
                    # tworzenie wykresu z danych
                    ArrayOfDataForPlot += dane
                    output = ""
        else:
            continue
    print(ArrayOfDataForPlot)
    plt.plot(ArrayOfDataForPlot, color='green', linestyle='dashed', linewidth=3)
    plt.xlabel('Data')
    plt.axis([0, 150, 0, 20])
    plt.savefig('filesToDownload/' + chossenAppName)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5005, debug=True)






