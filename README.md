# Devices Price Classification System

## Project Description

The Devices Price Classification System is an AI-based application that predicts the price range of mobile devices based on their specifications. The system comprises a Python project that includes data exploration, model training, and a Flask API to serve predictions.

## Features

- Predict the price range of a mobile device based on its specifications.
- RESTful API endpoints to handle device information.
- Stores device information and predicted price ranges in a SQLite database.

## Project Structure

```plaintext
PP_Classification/
├── src/
│   ├── EDA_DataProcessing_ModelCreation.ipynb  # Data exploration, cleaning, processing, model training
│   ├── pipe.py                                # Pipeline for predicting device prices
│   ├── app.py                                 # Flask app to create the API endpoints
│   ├── train.xlsx                             # Training data
│   ├── test.xlsx                              # Testing data
│   ├── devices.db                             # SQLite database for storing devices
│   ├── scaler.joblib                          # Saved scaler for normalization
│   └── svm_model.joblib                       # Saved SVM model
├── device_price_api.py                        # Script to test and run 10 test samples
├── README.md                                  # Readme file of the project 
└── requirements.txt                           # Required libs
```

## Installation

### Python Project

1. Clone the repository:
    ```sh
    git clone https://github.com/MohamedYahiaSan/PP_Classification.git
    ```
2. Navigate to the project directory (Make sure to adjust the line):
    ```sh
    cd ../PP_Classification
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Flask API

1. Navigate to the `src` directory:
    ```sh
    cd src
    ```

2. Start the Flask API:
    ```sh
    python app.py
    ```

3. The following endpoints are available:

- **Retrieve a list of all devices**:
    Endpoint: `POST /api/devices/`
    Expected Return: Returns a JSON array containing details of all devices stored in the database.

    ```sh
    curl -X POST http://localhost:5000/api/devices/
    ```

- **Retrieve details of a specific device by ID**:
    Endpoint: `GET /api/devices/{id}`
    Expected Return: Returns details of the device with the specified ID in JSON format. If the device is not found, returns a 404 error.

    ```sh
    curl http://localhost:5000/api/devices/{id}
    ```

- **Add a new device**:
    Endpoint: `POST /api/devices`
    Expected Return: Returns a success message in JSON format if the device is added successfully. If any required fields are missing in the request body, returns a 400 error.

    ```sh
    curl -X POST -H "Content-Type: application/json" -d '{
        "battery_power": 500,
        "blue": 1,
        "clock_speed": 2.5,
        "dual_sim": 1,
        "fc": 5,
        "four_g": 1,
        "int_memory": 64,
        "m_dep": 0.5,
        "mobile_wt": 150,
        "n_cores": 4,
        "pc": 12,
        "px_height": 1080,
        "px_width": 1920,
        "ram": 4000,
        "sc_h": 15,
        "sc_w": 7,
        "talk_time": 20,
        "three_g": 1,
        "touch_screen": 1,
        "wifi": 1
    }' http://localhost:5000/api/devices
    ```

- **Predict the price for a device by ID and update the database**:
    Endpoint: `POST /api/predict/{id}`
    Expected Return: Returns the predicted price for the device with the specified ID in JSON format. If the device is not found, returns a 404 error
    ```sh
    curl -X POST http://localhost:5000/api/predict/{id}
    ```

### Testing with `device_price_api.py`

1. Runs 10 test samples from test.xlsx:
    ```sh
    python device_price_api.py
    ```

## Data Exploration and Model Training

The `EDA_DataProcessing_ModelCreation.ipynb` notebook contains steps for exploring the data, processing it, training multiple models, and selecting the optimal model.

### Insights and Visualization

- **Strong correlations**:
  - Price x RAM
  - Screen dimensions x Pixel dimensions
  - 3G x 4G
  
  We will make full use of such strong features.

- **Feature engineering**:
  - Use pixel area instead of dimensions as a feature.
  
  We will drop features with bad correlation and almost no effect, such as touch screen, screen height/width, mobile weight, mobile depth, and clock speed.

### Model Evaluation

We evaluated several models, including Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, and Support Vector Machine (SVM). The best-performing model was selected based on metrics such as accuracy, precision, recall, and F1 score.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
