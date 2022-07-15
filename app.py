import requests
import json
from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_wtf import FlaskForm

app = Flask(__name__)

load_dotenv()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/city/<city>')
def weather(city):
    city_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + \
               os.environ.get("OPEN_WEATHER_MAP_API_KEY") + \
               '&q=' + city
    response = requests.get(city_url + city)
    weather_data = json.loads(response.text)

    def timestamp_to_datetime(epoch):
        raw_datetime = datetime.fromtimestamp(epoch)
        return raw_datetime.strftime("%A, %B %d %I:%M:%S %p")

    def timestamp_to_time(epoch):
        date_time = datetime.fromtimestamp(epoch)
        return date_time.strftime("%I:%M %p")

    def kelvin_to_celsius(kelvin_temp):
        return round(kelvin_temp - 273.15)

    def deg_to_cardinal(deg):
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        ix = int((deg + 11.25) / 22.5)
        return dirs[ix % 16]

    def mps_to_kmph(mps):
        return round(3.6 * mps)

    city = weather_data["name"]
    coordinates = str(weather_data["coord"]["lat"]) + ', ' + str(weather_data["coord"]["lon"])
    last_updated = timestamp_to_datetime(weather_data["dt"])
    sunrise = timestamp_to_time(weather_data["sys"]["sunrise"])
    sunset = timestamp_to_time(weather_data["sys"]["sunset"])

    current_temp = kelvin_to_celsius(weather_data["main"]["temp"])
    current_conditions = weather_data["weather"][0]["description"].title()
    current_icon = 'http://openweathermap.org/img/wn/' + weather_data["weather"][0]["icon"] + '@2x.png'
    feels_like = kelvin_to_celsius(weather_data["main"]["feels_like"])
    wind_speed = mps_to_kmph(weather_data["wind"]["speed"])
    wind_direction = deg_to_cardinal(weather_data["wind"]["deg"])
    humidity = weather_data["main"]["humidity"]

    return render_template("weather.html",
                           city_name=city,
                           coordinates=coordinates,
                           last_updated=last_updated,
                           sunrise=sunrise,
                           sunset=sunset,
                           current_temp=current_temp,
                           current_conditions=current_conditions,
                           current_icon=current_icon,
                           feels_like=feels_like,
                           wind_speed=wind_speed,
                           wind_direction=wind_direction,
                           humidity=humidity)


if __name__ == '__main__':
    app.run()
