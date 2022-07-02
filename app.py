import requests
import json
from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()

weather_api = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
city_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + \
           weather_api + '&id='


def timestamp_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)


def timestamp_to_time(epoch):
    date_time = datetime.fromtimestamp(epoch)
    return date_time.strftime("%H:%M:%S")


def kelvin_to_celsius(kelvin_temp):
    return round(kelvin_temp - 273.15)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<city_id>')
def weather(city_id):
    response = requests.get(city_url + city_id)
    weather_data = json.loads(response.text)

    city_name = weather_data["name"]
    coordinates = str(weather_data["coord"]["lat"]) + ', ' + str(weather_data["coord"]["lon"])
    last_updated = timestamp_to_datetime(weather_data["dt"])
    sunrise = timestamp_to_time(weather_data["sys"]["sunrise"])
    sunset = timestamp_to_time(weather_data["sys"]["sunset"])

    current_temp = kelvin_to_celsius(weather_data["main"]["temp"])
    current_conditions = weather_data["weather"][0]["description"].title()
    current_icon = 'http://openweathermap.org/img/wn/' + weather_data["weather"][0]["icon"] + '@2x.png'
    feels_like = kelvin_to_celsius(weather_data["main"]["feels_like"])

    return render_template("weather.html",
                           city_name=city_name,
                           coordinates=coordinates,
                           last_updated=last_updated,
                           sunrise=sunrise,
                           sunset=sunset,
                           current_temp=current_temp,
                           current_conditions=current_conditions,
                           current_icon=current_icon,
                           feels_like=feels_like)


if __name__ == '__main__':
    app.run()
