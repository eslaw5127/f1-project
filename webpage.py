from flask import Flask, redirect, url_for, render_template
from email.charset import BASE64
import requests
import json


#data for driver standings
url = "http://ergast.com/api/f1/current/driverStandings.json"
response = requests.get(url)

data = response.json()
season_year = data['MRData']['StandingsTable']['season']
data = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

#points/wins in list
standings_dict = {}
for i in range(len(data)):
    name = str(data[i]['Driver']['givenName'] + " " + data[i]['Driver']['familyName'])
    standings_dict.update({str(i+1) :[ name,data[i]['Constructors'][0]['name'],data[i]['points'],data[i]['wins']]})

#data for most recent race
url2 = "http://ergast.com/api/f1/current/last/results.json"
response2 = requests.get(url2)

data2 = response2.json()

season = data2['MRData']['RaceTable']['season']
round = data2['MRData']['RaceTable']['round']

race_name = data2['MRData']['RaceTable']['Races'][0]['raceName']
race_country = data2['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']

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
    constructor_dict.update({str(i+1) : [data3[i]['Constructor']['name'], data3[i]['points']]})

#data for qualifying round
url4 = f'http://ergast.com/api/f1/{season}/{round}/qualifying.json'
response4 = requests.get(url4)

data4 = response4.json()
data4 = data4['MRData']['RaceTable']['Races'][0]['QualifyingResults']

qual = {}

q1 = []
q2 = []
q3 = []


for i in range(len(data4)):
    q1.append(data4[i]['Q1'])

for i in range(0,15):
    q2.append(data4[i]['Q2'])

for i in range(0,10):
    q3.append(data4[i]['Q3'])

for i in range(len(data4)):
    q_list = []
    q_list.append(data4[i]['Driver']['familyName'])
    q_list.append(data4[i]['Constructor']['name'])
    q_list.append(q1[i])
    if(i < 15):
        q_list.append(q2[i])
    else:
        q_list.append(0)
    if(i < 10):
        q_list.append(q3[i])
    else:
        q_list.append(0)
    
    qual.update({str(i+1) : q_list})

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/race")
def race():
    return render_template("race.html", content = race_dict, race = race_name, country = race_country)

@app.route("/qualifying")
def qualifying():
    return render_template("qualifying.html", content = qual)

@app.route("/drivers")
def drivers():
    return render_template("drivers.html", content = standings_dict, year = season_year)

@app.route("/constructors")
def constructors():
    return render_template("constructors.html", content = constructor_dict, year = season_year )

if __name__ == "__main__":
    app.run(debug=True)