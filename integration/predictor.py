# predictor.py

from tensorflow.keras.models import load_model
import pandas as pd
import tensorflow as tf

class Predictor:
    def __init__(self, model_path, csv_path):
        self.model = self.load_model(model_path)
        self.data = self.load_data(csv_path)
    
    def load_model(self, model_path):
        return load_model(model_path)

    def load_data(self, csv_path):
        return pd.read_csv(csv_path)
    
    def get_sample(self, sample_id):
        if 0 <= sample_id < len(self.data):
            return self.data.iloc[sample_id]
        else:
            raise ValueError(f"Sample ID {sample_id} is out of range. It should be between 0 and {len(self.data) - 1}.")
    
    def preprocess_sample(self, sample):
        # Implement any necessary preprocessing steps here
        return sample.values.reshape(1, -1)  # Example reshape for prediction
    
    def predict(self, sample_tensor):
        # Convert the sample to a TensorFlow tensor with appropriate dtype
        prediction = self.model.predict(sample_tensor)
        return float(prediction[0][0])  # Convert numpy.float32 to native float
    
    def interpret_prediction(self, prediction):
        # Assuming a binary classification model
        class_label = "Positive" if prediction > 0.5 else "Negative"
        return {"class": class_label, "prediction": prediction}


    