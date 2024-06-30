# DSC 510
# Week 10
# Programming Final Project
# Author Jackson Lyons
# 08/12/2023
import json
import requests

# Function to obtain the geocode data for a given zip code
# Returns a dictionary given by the api
def get_geocode_zip(zip_code):
    url_geo = 'http://api.openweathermap.org/geo/1.0/zip?'
    query_string_geo = {"zip": zip_code,
                        "appid": "5744b75256c2234ee31e1b9517e76410"}
    try:
        response_geo = json.loads(requests.request("GET", url_geo, params=query_string_geo).text)
    except requests.exceptions.ConnectionError:
        return "FAILED"
    except requests.exceptions.HTTPError:
        return "FAILED"
    return response_geo


# Function to obtain the geocode data for a given city
# Returns a dictionary given by the api
def get_geocode_city(city):
    # Ask the user for the state to differentiate between same city names
    state = input('Please enter the state: ')
    city_state = city + ',' + state
    url_geo = 'http://api.openweathermap.org/geo/1.0/direct?'
    query_string_geo = {"q": city_state,
                        "appid": "5744b75256c2234ee31e1b9517e76410"}
    # Checking if our response data is correct, if no city is found then the API returns an empty list
    # so we check for an index error if this is the case. Also check for connection errors and HTTP Errors
    try:
        response_geo = json.loads(requests.request("GET", url_geo, params=query_string_geo).text)[0]
    except IndexError:
        return "FAILED"
    except requests.exceptions.ConnectionError:
        return "FAILED"
    except requests.exceptions.HTTPError:
        return "FAILED"
    return response_geo


# Function to obtain the weather for a given geocode based on the lat, lon
# Input: Dictionary containing the lat, lon as keys
# Return: Dictionary given by the api
def get_weather(geocode):
    lat = geocode['lat']
    lon = geocode['lon']
    url = "https://api.openweathermap.org/data/2.5/weather"
    query_string = {"lat": lat,
                    "lon": lon,
                    "appid": "5744b75256c2234ee31e1b9517e76410"}
    # Trying to connect to the server, if the connection fails then we return
    # FAILED which is handeled in main
    try:
        response = requests.request("GET", url, params=query_string)
    except requests.exceptions.ConnectionError:
        return "FAILED"
    except requests.exceptions.HTTPError:
        return "FAILED"
    else:
        return json.loads(response.text)


# Function to convert the temperature from Kelvin given by the returned data
# to either Celsius, Fahrenheit, or Kelvin based on user preference
# Returns an integer
def convert_temp(temp, pref):
    # Conversion will default to Fahrenheit if choice is not entered correctly
    if pref == "c":
        return int(temp - 273.15)
    elif pref == 'k':
        return temp
    else:
        return int((temp - 273.15) * (9/5) + 32)


# Helper function to process the weather section
# Has no return value, just prints the information to the command line
def process_weather(d):
    t = d[0]
    for key in t:
        if key in ['main', 'description']:
            print(f"{key :>12}{t[key] :>12}")


# Helper function to process the main section of the weather data
# This function uses convert_temp to convert the temperatures from Kelvin to
# the specified user preference
# Has no return, just prints the information to command line
def process_main(d, temp_pref):
    for key in d:
        if key in ['temp', 'feels_like', 'temp_min', 'temp_max']:
            print(f"{key.replace('_', ' ') :>12}{convert_temp(d[key], temp_pref) :>12}")
        else:
            print(f"{key :>12}{d[key] :>12}")


# Print to screen all items contained in dictionary where each key
# value pair is the weather related information
def pretty_print(dictionaries, temp_pref):
    city_name = "Current Weather for " + dictionaries['name']
    print('-' * len(city_name))
    print(city_name)
    print('-' * len(city_name))

    for dictionary in dictionaries:
        d = dictionaries[dictionary]
        if dictionary == "weather":
            process_weather(d)
        elif dictionary == "main":
            process_main(d, temp_pref)
        elif dictionary == "visibility":
            print(f"{dictionary :>12}{int(d / 1609) :>12}")


def main():
    cont = 'y'
    while cont == 'y':
        city = input("Please enter a city: ")

        # Check to see if input value is an integer for a zip code or string for city, if input value can
        # be converted to an int then we treat it as a zip code in the try block,
        # if not then we treat it as a city in the except block
        try:
            val = int(city)
            geocode = get_geocode_zip(val)
        except ValueError:
            val = city
            geocode = get_geocode_city(val)

        # Here were checking if the result sent from the get_geocode functions is correct
        # if we get an error then we handle it here, if not then we continue with getting the weather
        if 'cod' in geocode:
            print("Error Code: ", geocode['cod'], geocode['message'])
        elif geocode == 'FAILED':
            print("Sorry, there was an error in your city name")
        else:
            weather_data = get_weather(geocode)

            # Checking if we were able to be connected to the server
            if weather_data == "FAILED":
                print("Sorry, the server could not be reached. Please try again shortly")

            # Checking for any server response errors, if none then we proceed to printing
            if weather_data['cod'] != 200:
                print("Error", response['cod'], response['message'])
            else:
                # Get the input and just take the first char if a word is entered
                temp_pref = input("Would you like Celsius (c), Fahrenheit (f), or Kelvin (k): ")[0].lower()
                pretty_print(weather_data, temp_pref.lower())

        # Ask user if they would like to continue, take the first character in case
        # they enter a string instead of a char
        cont = input("Would you like weather for another city [Y/N]: ")[0].lower()


if __name__ == "__main__":
    main()
