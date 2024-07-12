import requests
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

def retrieve_latest_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()  # Automatically raises an error for bad status codes
    entries = response.json()
    
    if isinstance(entries, list) and entries:
        return entries[0]
    raise ValueError("Unexpected data format received from the API")

def transform_data_for_model(entry):
    dataframe = pd.DataFrame([entry]).drop(columns=['_id', 'created_at'])
    return dataframe.values

def predict_water_potability(model, data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    prediction = model.predict(scaled_data)
    return int(np.round(prediction)[0][0])

if __name__ == "__main__":
    API_URL = ""
    MODEL_FILE_PATH = "./water_potability_model.pkl"

    latest_data = retrieve_latest_data(API_URL)

    with open(MODEL_FILE_PATH, "rb") as model_file:
        water_model = pickle.load(model_file)

    prepared_data = transform_data_for_model(latest_data)
    potability_prediction = predict_water_potability(water_model, prepared_data)

    result = "Potable" if potability_prediction == 1 else "Not Potable"
    print(result)
