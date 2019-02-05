from chatbot import app
import requests
import json
from chatbot import config
from flask import request


@app.route('/')
@app.route('/index')    # A decorator modifies the function that follows it.
def index():
    return("How ya doin")


@app.route("/get_weather",methods=["POST"])
def get_weather():
    data = request.get_json()
    # print("Parsed post_body",requestjson)
    city = data["queryResult"]["parameters"]["geo-city"]

    if city:
        # print(city)
        apiKey = config.open_weather_map_api_key
        weatherUrl = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}".format(city = city,key = apiKey);

        res = requests.get(weatherUrl)

        try:
            res.raise_for_status()
        except Exception as exc:
            print("There was a problem:",(exc))

        weatherDetails = res.json()

        temp = weatherDetails["main"]["temp"]
        weatherDescription = weatherDetails["weather"][0]["description"]

        response = "It is {temp} degrees with {desc}".format(temp=temp,desc=weatherDescription)

        res = {"fulfillmentText":response}

        return json.dumps(res)
