from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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
    temp_k_value = list_element.get('main', {}).get('temp')  # Température en Kelvin
    temp_c_value = temp_k_value - 273.15 if temp_k_value is not None else None  # Conversion en °C
    weather_description = list_element.get('weather', [{}])[0].get('description', 'No description')  # Description météo

    results.append({
        'Timestamp': dt_value,
        'Temperature (°C)': temp_c_value,
        'Weather': weather_description
    })
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
  
if __name__ == "__main__":
  app.run(debug=True)
