from threading import Thread
import requests
import time
import pandas as pd
from src import app

# Function to run Flask app
def run_flask_app():
    app.app.run(debug=True, use_reloader=False)


# Functions to perform API requests

# Function to retrieve whole list as a Pandas DataFrame
def all_data(BASE_URL):
    response= requests.post(BASE_URL+'/devices/')
    if response.status_code==500:
        print(f'Failed to retrive code:{response.status_code}')
    else:
        df=pd.DataFrame(response.json())
        print(df)



# Function to add a device data
def add_device(BASE_URL,data:dict):
    response= requests.post(BASE_URL+'/devices' , json=data )

    # Check if the request was successful
    if response.status_code == 201:
        print("Device added successfully!")
        print("Response:", response.json())
    else:
        print("Failed to add device.")
        print("Error:", response.text)



# Function to retrieve data of a specific device ID
def find_device(BASE_URL, id):
    #Make a GET request to retrieve device details by ID
    response = requests.get(BASE_URL+f'/devices/{id}')

    # Check if the request was successful
    if response.status_code == 200:
        device_details = pd.Series(response.json())
        print("Device details:")
        print(device_details)
    else:
        print("Failed to retrieve device details.")
        print("Error:", response.text)



# Function to predict price of a specific device and save it into the database
def predict_update(BASE_URL,id):
    # Make a POST request to predict the price for the device ID
    response = requests.post(BASE_URL+f'/predict/{id}')

    # Check if the request was successful
    if response.status_code == 200:
        predicted_price = response.json()
        print(f"Predicted price for device ID {id}: {predicted_price}")
    else:
        print("Failed to predict price.")
        print("Error:", response.text)






# Start the Flask app in a separate thread
thread = Thread(target=run_flask_app)
thread.start()

# Give the server a moment to ensure it's fully started
time.sleep(2)


# Initializing the URL of our service
BASE_URL = "http://localhost:5000/api"


# Reading test file to test 10 samples 
test=pd.read_excel('Machine_Learning/PP_Classification/src/test.xlsx')

# Checking our data
all_data(BASE_URL)

# Adding 10 devices and predicting their price
for i in range(10):
    device_data=test.iloc[i,:].to_dict()
    add_device(BASE_URL,device_data)
    predict_update(BASE_URL,i+1)

# Taking a look at device 5
find_device(BASE_URL,id=10)

# Checking our data
all_data(BASE_URL)