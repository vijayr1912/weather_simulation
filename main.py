#!/usr/bin/env python
"""
Main function for simulating a weather pattern for major cities.
Executes a data pipeline -
    1 First download and gets the training data for the machine learning algorithm.
    2. Develop the sklearn regression and classification models on train data.
    3. use the models to generate simulation for test data.
    4. Formats and saves the predictions of test data to a csv file in desired format.
    5. The train and test files are saved in a working directory, that is specified in the config file
"""

# Generic/Built-in
import os
import argparse
import traceback
import datetime

import pandas as pd

# Project specific files
from simulator.helper import get_configuration_parameters
from simulator.helper import check_configuration_values
from simulator.helper import get_locations_in_canonized_form
from simulator.helper import log_debug
from simulator.training_data import get_location_details
from simulator.training_data import download_weather_data
from simulator.models import get_prediction_models
from simulator.models import simulate_weather

# Owned
__author__ = "Vijay Raghunath"
__copyright__ = "MIT License"
__credits__ = ["Vijay Raghunath"]
__license__ = "MPL 2.0"
__version__ = "1.0.0"
__email__ = "vrag7458@uni.sydney,edu.au"
__status__ = "dev"

"""
Command-Line commands:
1. To create a simulator for the test data
    pipenv run python main.py --ini config/weathersimulator.ini
    
2. To get new train data
    pipenv run python main.py --ini config/weathersimulator.ini --train True
"""

# Code
def main():
    create_simulator = True
    parser = argparse.ArgumentParser()
    os.environ["TZ"] = "UTC"

    parser.add_argument(
        "-i",
        "--ini",
        action="store",
        dest="ini_filename",
        help=".ini file name having configuration parameters for weather simulator",
    )

    parser.add_argument(
        "--train",
        action="store",
        dest="train",
        help="new train data for the ML regression algorithm",
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    input_arguments = parser.parse_args()

    google_api_key = get_configuration_parameters(
        input_arguments.ini_filename, "Google API Key", {}
    )

    dark_sky_api_key = get_configuration_parameters(
        input_arguments.ini_filename, "Dark Sky API Key", {}
    )
    if not check_configuration_values(dark_sky_api_key):
        create_simulator = False

    if not check_configuration_values(google_api_key):
        create_simulator = False
        # TODO : log it a file to tell the user it is a critical failure if a Google API key is absent.

    working_directory = get_configuration_parameters(
        input_arguments.ini_filename, "Working directory", {}
    )
    if not check_configuration_values(working_directory):
        create_simulator = False

    if create_simulator:
        try:
            if input_arguments.train:
                train_locations = get_locations_in_canonized_form(
                    input_arguments.ini_filename, "Training Data"
                )

                location_info = []
                for location in train_locations:
                    location_info.append(
                        get_location_details(location, google_api_key["key"])
                    )

                log_debug(location_info)

                weather_data = download_weather_data(
                    location_info,
                    datetime.datetime(2018, 1, 1),
                    dark_sky_api_key["key"],
                )

                train_data_path = os.path.join(
                    working_directory["working_directory"], "train_data.csv"
                )
                weather_data.to_csv(train_data_path)

            train_data_path = os.path.join(
                working_directory["working_directory"], "train_data.csv"
            )
            train_df = pd.read_csv(train_data_path)

            temperature_model = get_prediction_models(train_df, "temperature")
            pressure_model = get_prediction_models(train_df, "pressure")
            humidity_model = get_prediction_models(train_df, "humidity")
            condition_model = get_prediction_models(train_df, "condition")

            test_location = get_locations_in_canonized_form(
                input_arguments.ini_filename, "Test Data"
            )

            test_location_info = []
            for location in test_location:
                test_location_info.append(
                    get_location_details(location, google_api_key["key"])
                )

            generated_weather_data = simulate_weather(
                test_location_info,
                temperature_model,
                pressure_model,
                humidity_model,
                condition_model,
                datetime.datetime(2018, 1, 1),
            )

            test_data_path = os.path.join(
                working_directory["working_directory"], "test_data_predictions.csv"
            )
            generated_weather_data[
                [
                    "Location",
                    "Position",
                    "Local Time",
                    "Conditions",
                    "Temperature",
                    "Pressure",
                    "Humidity",
                ]
            ].to_csv(test_data_path, header=0, index=0, sep="|")

        except Exception as exc:
            log_debug(traceback.format_exc())


if __name__ == "__main__":
    main()
