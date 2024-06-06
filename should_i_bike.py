import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import numpy as np
from geopy import Nominatim

"""
class location:
    def __init__(self, name):
        self.name
        # self.lat
        # self.lon

    # def get_name(self):
    def print_name(self):
        print(self.name)
"""


def auto_input(location_name):

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/gfs"

    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(location_name)
    print(getLoc.address)
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)
    lat = getLoc.latitude
    lon = getLoc.longitude

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m",
                   "precipitation_probability", "visibility",
                   "wind_speed_10m", "uv_index"],
        # "minutely_15": ["temperature_2m", "relative_humidity_2m",
        # "apparent_temperature", "precipitation", "wind_speed_10m",
        # "visibility"],
        "wind_speed_unit": "ms",
        "timezone": "America/New_York",
        "forecast_days": 1,
        "forecast_hours": 12,
        # "forecast_minutely_15": 96
    }
    responses = openmeteo.weather_api(url, params=params)

    return responses


def inputs(lat, lon):

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/gfs"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m",
                   "precipitation_probability", "visibility",
                   "wind_speed_10m", "uv_index"],
        # "minutely_15": ["temperature_2m", "relative_humidity_2m",
        # "apparent_temperature", "precipitation", "wind_speed_10m",
        # "visibility"],
        "wind_speed_unit": "ms",
        "timezone": "America/New_York",
        "forecast_days": 1,
        "forecast_hours": 12,
        # "forecast_minutely_15": 96
    }
    responses = openmeteo.weather_api(url, params=params)

    return responses

# def minutely_15_process():


def hourly_process(response):

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["visibility"] = hourly_visibility
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["uv_index"] = hourly_uv_index

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe)

    return hourly_dataframe


def data_analysis():

    


    return



def main():
    resp = auto_input("coventry ct")
    hourly_process(resp[0])
    # cov_resp = cov_resp[0]
    # hourly_process(cov_resp)
    # location("coventry ct")






if __name__ == "__main__":
    main()
