# test_predict.py

from predictor import Predictor
import tensorflow as tf

def test_predict():
    model_path = "./model/my_model.h5"
    csv_path = "./data/samples.csv"
    sample_id = 0  # Change this to the sample ID you want to predict

    try:
        predictor = Predictor(model_path, csv_path)
        sample = predictor.get_sample(sample_id)  # Use the instance to access the method
        sample_tensor = tf.convert_to_tensor(predictor.preprocess_sample(sample), dtype=tf.float32)  # Ensure the sample is correctly shaped
        print(f"Sample ID {sample_id}: {sample_tensor}")
        prediction = predictor.predict(sample_tensor)
        print(f"Prediction for sample ID {sample_id}: {prediction}")
    except (ValueError, FileNotFoundError) as e:
        print(e)

if __name__ == "__main__":
    test_predict()
