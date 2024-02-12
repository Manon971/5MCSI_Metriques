from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                        
app = Flask(__name__)  #commentaire 
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
 
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits():
    # Récupération des données des commits
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits = response.json()

    # Extraction des minutes de chaque commit
    minutes = [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').minute for commit in commits]

    # Création du graphique
    plt.hist(minutes, bins=60, range=(0, 59))
    plt.title('Commits par minute')
    plt.xlabel('Minutes')
    plt.ylabel('Nombre de commits')

    # Conversion du graphique en image pour l'incorporer dans la réponse HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)

if __name__ == "__main__":
  app.run(debug=True)
