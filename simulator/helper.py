"""
Helper function for
1. Getting weather simulator training data
2.
Formatting output data in desired format
"""

import configparser

# helper function to swith on/off print statement
def log_debug(msg):
    print(msg)
    pass


def get_configuration_parameters(filename, section, data):
    """ Returns configuration parameters from weathersimulator.ini file.
    Args:
        filename: Python string, name of the configuration file.
        section: Python string, name of the section in which the property is located.
        data: Python dict, with default values for the section in configuration file.
    Returns:
        The return value. Python dict, values read from configuration file for a section.
    """
    config = configparser.ConfigParser()
    config.read(filename)

    if section in config.sections():
        for key in config[section]:
            data[key] = config[section][key]
        for key in data:
            if key in config[section]:
                data[key] = config[section][key]
            else:
                data[key] = "Key not found in configuration file"
    return data


def check_configuration_values(data):
    """ Checks if parameters needed for creating a weather simulator are present in the configuration file.
    Args:
        data: Python dict, with values read from configuration file for a section.
    Returns: Boolean, True if all needed parameters are present in configuration file,
                False if not found.
    """
    is_valid = True
    for key in data:
        if data[key] == "Key not found in configuration file" or data[key] == "":
            is_valid = False
            break
    return is_valid


def get_locations_in_canonized_form(filename, section):
    """ Gets the location names in a standardized format to be recognized as valid locations by Google API.
    Args:
        filename: Python string, name of the configuration file.
    Returns: Python list, all valid locations.
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return [e.strip() for e in config.get(section, "locations").split(",")]


def format_weather_data(df):
    df[
        [
            "Location",
            "Position",
            "Local Time",
            "Conditions",
            "Temperature",
            "Pressure",
            "Humidity",
        ]
    ].to_csv("data/generated_weather_data.psv", header=0, index=0, sep="|")
