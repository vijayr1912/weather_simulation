import datetime
import pandas as pd

from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB


def get_prediction_models(df, feature):
    """ Trains and gets the regression models for weather prediction.
    Args:
        df: Pandas dataframe, with the learning data.
        feature: Location property which is to be modeled.
    Returns: sklearn ML model.
    """
    predictors_x = df[["latitude", "longitude", "elevation", "time"]].values
    prediction_y = df[[feature]].values

    if feature in ["temperature", "humidity", "pressure"]:
        return linear_model.LinearRegression().fit(predictors_x, prediction_y)
    else:
        return GaussianNB().fit(predictors_x, prediction_y.ravel())


def simulate_weather(
    location_info_list, temp_model, pres_model, hum_model, cond_model, start_date
):
    predicted_weather_data = {}

    for location_info in location_info_list:

        location = location_info["location"]
        latitude = location_info["latitude"]
        longitude = location_info["longitude"]
        elevation = location_info["elevation"]

        for date_offset in range(0, 365, 30):
            new_date = start_date + datetime.timedelta(date_offset)
            time = int((new_date).strftime("%s"))

            predicted_weather_data["Location"] = predicted_weather_data.get(
                "Location", []
            ) + [location]
            predicted_weather_data["Position"] = predicted_weather_data.get(
                "Position", []
            ) + [str(latitude) + "," + str(longitude) + "," + str(elevation)]
            predicted_weather_data["Local Time"] = predicted_weather_data.get(
                "Local Time", []
            ) + [new_date.isoformat()]

            cond = cond_model.predict([[latitude, longitude, elevation, time]])[
                0
            ].lower()
            if "clear" not in cond:
                predicted_weather_data["Conditions"] = predicted_weather_data.get(
                    "Conditions", []
                ) + ["Rain"]
            elif "snow" in cond:
                predicted_weather_data["Conditions"] = predicted_weather_data.get(
                    "Conditions", []
                ) + ["Snow"]
            else:
                predicted_weather_data["Conditions"] = predicted_weather_data.get(
                    "Conditions", []
                ) + ["Sunny"]

            temp = temp_model.predict([[latitude, longitude, elevation, time]])[0][0]
            temp_celsius = (temp - 32) * (5.0 / 9.0)
            predicted_weather_data["Temperature"] = predicted_weather_data.get(
                "Temperature", []
            ) + [temp_celsius]

            pressure = pres_model.predict([[latitude, longitude, elevation, time]])[0][
                0
            ]
            predicted_weather_data["Pressure"] = predicted_weather_data.get(
                "Pressure", []
            ) + [pressure]

            humidity = hum_model.predict([[latitude, longitude, elevation, time]])[0][0]
            predicted_weather_data["Humidity"] = predicted_weather_data.get(
                "Humidity", []
            ) + [int(humidity * 100)]

    df = pd.DataFrame(predicted_weather_data)
    df["Temperature"] = round(df["Temperature"], 1)
    df["Pressure"] = round(df["Pressure"], 1)

    return df
