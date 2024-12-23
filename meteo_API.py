# -- EI4 • IoT - TP 2 - Exercice 3
# ANDRIATSILAVO Matteo - TP A
# /!\ Utilisation d'un environnement virtuel nommé `TP1`

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def retreive_weather_data(starting_row: int = 1, ending_row: int = -1):
	"""Récupère les données de l'API météo sur 7 jours de prévisions, sous forme de dataframe Pandas.
	Paramètres: starting_row: ligne (heure) à laquelle il faut commencer à insérer les données,
				ending_row: ligne (heure) à laquelle il faut arrêter d'insérer les données.
	Sortie: une dataframe type Pandas"""
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 48.8534,
		"longitude": 2.3488,
		"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "is_day"],
		"timezone": "auto"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	# print(f"Elevation {response.Elevation()} m asl")
	# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
	hourly_is_day = hourly.Variables(3).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["is_day"] = hourly_is_day

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	if (starting_row == 1 and ending_row == -1):
		return hourly_dataframe
	return hourly_dataframe.loc[starting_row: ending_row]
	# print(hourly_dataframe)
	# retreive certain rows (row x to row y) from a Pandas dataframe `some_df`: 
	# some_df.loc[x:y]      # method 1
	# some_df.iloc[x:y+1]   # method 2

def formatting_weather_api_data(data):
    """Effectue un pré-traitement sur les données `data` provenant de l'API météo pour une meilleure compréhension 
    pour Jinja2 et un meilleur rendu à l'affichage.
    Entrées: `data`, dataframe type Pandas 
    Sorties: `data_dict`, les données sous formes de tableau Python"""
    # Conversion en dictionnaire pour Jinja2
    data_dict = data.to_dict(orient='records')
    #Pré-traitement pour un meilleur affichage (données compréhensibles)
    index = 0
    for _ in data_dict:
        data_dict[index]['date'] = _['date'].hour												# récupérer uniquement l'heure
        data_dict[index]['temperature_2m'] = round(_['temperature_2m'])							# arrondir la température
        data_dict[index]['apparent_temperature'] = round(_['apparent_temperature'])				# arrondir la température ressentie
        data_dict[index]['precipitation_probability'] = int(_['precipitation_probability'])		# arrondir la probabilité de précipitations
        data_dict[index]['is_day'] = "☀️" if (_['is_day'] > 0) else "🌙"					  
        index += 1
    return data_dict
