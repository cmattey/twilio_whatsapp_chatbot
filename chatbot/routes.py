from chatbot import app
import requests
import json
from chatbot import config
from flask import request


@app.route('/')
@app.route('/index')    # A decorator modifies the function that follows it.
def index():
    return("How ya doin")


@app.route("/get_info",methods=["POST"])
def get_info():
    data = request.get_json()
    # print("Parsed post_body",requestjson)

    intent_name = data["queryResult"]["intent"]["displayName"]
    json_response = ""

    if intent_name == "weather info":
        json_response = get_weather_info(data)
    elif intent_name == "pokemon":
        json_response = get_pokemon_info(data)

    return json_response

def get_weather_info(data):

    city = data["queryResult"]["parameters"]["geo-city"]

    if city:
        # print(city)
        apiKey = config.open_weather_map_api_key
        weather_url = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}".format(city = city,key = apiKey)

        res = requests.get(weather_url)

        try:
            res.raise_for_status()
        except Exception as exc:
            print("There was a problem with weather API:",(exc))

        weatherDetails = res.json()

        temp = weatherDetails["main"]["temp"]
        weatherDescription = weatherDetails["weather"][0]["description"]

        response = "It is {temp} degrees with {desc}".format(temp=temp,desc=weatherDescription)

        res = {"fulfillmentText":response}

        return json.dumps(res)

def get_pokemon_info(data):

    pokemon_name = data["queryResult"]["parameters"]["pokemon_name"]

    if pokemon_name:
        pokemon_name_lower = pokemon_name.lower()
        print(pokemon_name)

        poke_url= "https://pokeapi.co/api/v2/pokemon/{poke_name}".format(poke_name = pokemon_name_lower)

        res = requests.get(poke_url)

        try:
            res.raise_for_status()
        except Exception as exc:
            print("There was a problem with PokeAPI:",(exc))

        pokemon_details = res.json()

        types = []
        abilities = []

        for ability in pokemon_details["abilities"]:
            print(ability)
            abilities.append(ability["ability"]["name"])

        for type in pokemon_details["types"]:
            types.append(type["type"]["name"])

        response = "{poke_name} is a {poke_type} type pokemon and has the abilities: {poke_abil}".format(poke_name=pokemon_name,
        poke_abil = ", ".join(abilities), poke_type = ", ".join(types))

        res = {"fulfillmentText":response}

        return json.dumps(res)
