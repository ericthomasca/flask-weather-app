import requests
import json
from flask import Flask, render_template

app = Flask(__name__)

open_weather_map_api = '38eaed335d3085d2ca20fa104799a742'
city_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + \
            open_weather_map_api + '&id='


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/<city_id>')
def weather(city_id):
    response = requests.get(city_url + city_id)
    weather_data = json.loads(response.text)

    return render_template("weather.html", weather=weather_data)


if __name__ == '__main__':
    app.run()
