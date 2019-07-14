# Weather Simulator Assessement

Software Pre-requisites

Python version 3.7.1 or higher
Pipenv packing tool version 2018.11.26
To install Pipenv in your Mac machine use the command - brew install pipenv
For other OS, refer to the relevant instructions in https://pipenv.readthedocs.io/en/latest/

Place holder for CBA assessement - generate a weather simulation tool.

1. Clone the repo master branch - https://github.com/vijayr1912/weather_simulation.git


2. Go to the path- environment_simulation_assessement/

3. Run the command
`pipenv install -r requirements.txt`
This should install the necessary libraries for running the simulator tool.

4. Go to the config folder and open the file weathersimulator.ini. Change the Google API Key and Working directory sections with your Google API key and working directory on your local environment.
```python
[Google API Key]
key  = replacewithyourkey

[Working directory]
working_directory = ~/CBA_assessement
```

6. Activate the Virtual environment by running the command
`pipenv shell`

Running the code

1. The train and test data are located in the weathersimulator.ini
``` python
[Training Data]
locations = Tokyo Japan, New York USA, Sao Paulo Brazil, Manila Philippines,
 Mumbai India, Jakarta Indonesia, Lagos Nigeria, Cairo Egypt, Los Angeles USA,
 Buenos Aires Argentina, Moscow Russia, Shanghai China, Sydney Australia,
 Kabul Afghanistan, Johannesburg South Africa, Toronto Canada, Dresden Germany,
 San Francisco,USA

[Test Data]
locations = Miami United States, Oslo Norway, Adelaide Australia, Berlin Germany,
 Cardiff England, Srinagar India
```

You can add to the train or test data and the simulator will generate a model using the train data set and predict the weather for the test data.
The prediction are saved in the working directory specified in the config file.

To generate only predictions run the following command from the virtual environment shell - 
``` python
pipenv run python main.py --ini config/weathersimulator.ini --train True
```

To generate a new regression models and from them to predict for test data run from the virtual environment shell - 
``` python
pipenv run python main.py --ini config/weathersimulator.ini
```
