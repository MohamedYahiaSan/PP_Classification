from joblib import load
import pandas as pd
import numpy as np 
import os

# Get the current working directory
here=os.getcwd()
# Define the path to the directory containing the model and scaler
path=os.path.join(here,'src')

# Load the trained SVM model
loaded_model = load(os.path.join(path,'svm_model.joblib'))

# Load the scaler used for normalization
scaler = load(os.path.join(path,'scaler.joblib'))

train=pd.read_excel(os.path.join(path,'train.xlsx'))


# Function to predict the price range for a single sample
def predict(user_data):
    # Define the columns of our input data
    df=train[:50].copy()

    # add the input to our mini DataFrame
    df.loc[50]=user_data
    # Create a new feature 'area' as the product of 'px_height' and 'px_width'
    df['area']=df.px_height * df.px_width
    # Drop the columns that are not useful for the model
    df.drop(['clock_speed','m_dep','px_height','px_width','sc_w','sc_h','touch_screen','mobile_wt','price_range'],axis=1,inplace=True)
    # Scale the data using the loaded scaler and reshape it
    x=scaler.fit_transform(df)   
    # Predict the price range using the loaded model
    return loaded_model.predict(x)[-1]
