import requests
import datetime
import forecastio

import pandas as pd

def get_location_details(location, key=None):
    """
    Uses Google map REST API with credentials to get geolocation info of a place.
    Keyword arguments:
        location: Python String, with loction  name and country. E.g. Paris, France.
    Returns:
       A Python dict mapping for position attributes for a location.
    Raises:
        Response library exception: Error from the Response library when
                                        getting data using Google Server.
    """
    base_geolocation_url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    base_elevation_url = 'https://maps.googleapis.com/maps/api/elevation/json?locations='
    location_info = {'location': location}

    geolocation_url = base_geolocation_url + location + 'CA&key=' + key
    response_position = requests.get(geolocation_url)
    response_position.raise_for_status()

    position_data = response_position.json()
    if position_data.get('results'):
        for rgc_results in position_data.get('results'):
            # print(rgc_results)
            latlong = rgc_results.get('geometry', '').get('location', '')
            location_info['latitude'] = latlong.get('lat', '')
            location_info['longitude'] = latlong.get('lng', '')

            elevation_url = base_elevation_url + str(location_info['latitude']) + ',' + str(location_info['longitude']) + '&key=' + key
            response_elevation = requests.get(elevation_url)
            response_elevation.raise_for_status()

            elevation_data = response_elevation.json()
            # print(elevation_data)
            if elevation_data.get('results'):
                for elevation_data_results in elevation_data.get('results'):
                    location_info['elevation'] = elevation_data_results.get('elevation', '')
                    break

            break

    return location_info

def download_weather_data(location_info_list, start_date, api_key):
    """
    Uses forecastio Python module REST API to get weather data.
    Keyword arguments:
        location_info_list: Python list of dict, location with properties mapped as key value pairs.
        start_date: Python datetime structure, start date to download data from.
        api_key: Python string, forecast API access key.
    Returns:
       A Python dict mapping for position attributes for a location.
    Raises:
        Response library exception: Error from the fForecast.io weather API.
    """
    weather_data = {}
    for location_info in location_info_list:
        for date_offset in range(0, 365, 7):
            forecast = forecastio.load_forecast(
                api_key,
                location_info['latitude'],
                location_info['longitude'],
                time=start_date+datetime.timedelta(date_offset),
                units="us"
            )

            for hour in forecast.hourly().data:
                weather_data['location'] = weather_data.get('location', []) + [location_info['location']]
                weather_data['latitude'] = weather_data.get('latitude', []) + [location_info['lat']]
                weather_data['longitude'] = weather_data.get('longitude', []) + [location_info['lng']]
                weather_data['elevation'] = weather_data.get('elevation', []) + [location_info['elev']]
                weather_data['condition'] = weather_data.get('condition', []) + [hour.d.get('summary', '')]
                weather_data['temperature'] = weather_data.get('temperature', []) + [hour.d.get('temperature', 50)]
                weather_data['humidity'] = weather_data.get('humidity', []) + [hour.d.get('humidity', 0.5)]
                weather_data['pressure'] = weather_data.get('pressure', []) + [hour.d.get('pressure', 1000)]
                weather_data['time'] = weather_data.get('time', []) + [hour.d['time']]

    return pd.DataFrame(weather_data)
