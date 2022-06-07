from flask import Flask, redirect, url_for, render_template
from email.charset import BASE64
import requests
import json


#data for driver standings
url = "http://ergast.com/api/f1/current/driverStandings.json"
response = requests.get(url)

data = response.json()
data = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

#points/wins in list
standings_dict = {}
for i in range(len(data)):
    standings_dict.update({data[i]['Driver']['familyName'] : [data[i]['points'],data[i]['wins']]})

#data for most recent race
url2 = "http://ergast.com/api/f1/current/last/results.json"
response2 = requests.get(url2)

data2 = response2.json()
race_name = data2['MRData']['RaceTable']['Races'][0]['raceName']
data2 = data2['MRData']['RaceTable']['Races'][0]['Results']

race_dict = {}
for i in range(len(data2)):
    race_dict.update({data2[i]['position'] : [data2[i]['Driver']['familyName'], data2[i]['Constructor']['name'], data2[i]['status']]})


#data for constructors
url3 = "http://ergast.com/api/f1/current/constructorStandings.json"
response3 = requests.get(url3)

data3 = response3.json()
data3 = data3['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

constructor_dict = {}
for i in range(len(data3)):
    constructor_dict.update({data3[i]['Constructor']['name'] : data3[i]['points']})


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", content = race_dict)

if __name__ == "__main__":
    app.run(debug=True)