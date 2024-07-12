from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from databases.db_manager import DatabaseManager
from integration.predictor import Predictor
import tensorflow as tf

app = FastAPI()
db_manager = DatabaseManager()
predictor = Predictor(model_path="./integration/model/my_model.h5", csv_path="./integration/data/samples.csv")

class DataModel(BaseModel):
    id: int
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

class UpdateDataModel(BaseModel):
    data: dict
    condition: str

@app.post("/add_data/{table_name}")
async def add_data(table_name: str, data: DataModel):
    try:
        db_manager.add_data(table_name, data.dict())
        return {"message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete_data/{table_name}")
async def delete_data(table_name: str, condition: str):
    try:
        db_manager.delete_data(table_name, condition)
        return {"message": "Data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/add_column/{table_name}")
async def add_column(table_name: str, column_name: str, column_type: str):
    try:
        db_manager.add_column(table_name, column_name, column_type)
        return {"message": "Column added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/drop_column/{table_name}")
async def drop_column(table_name: str, column_name: str):
    try:
        db_manager.drop_column(table_name, column_name)
        return {"message": "Column dropped successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_potability_table")
async def create_potability_table():
    try:
        db_manager.create_potability_table()
        return {"message": "Table 'potability' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/update_data/{table_name}")
async def update_data(table_name: str, update_data: UpdateDataModel):
    try:
        db_manager.update_data(table_name, update_data.data, update_data.condition)
        return {"message": "Data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_all_tables")
async def get_all_tables():
    try:
        tables = db_manager.get_all_tables()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_specific_table/{table_name}")
async def get_specific_table(table_name: str):
    try:
        data = db_manager.get_specific_table(table_name)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_all_ids_from_water_quality")
async def get_all_ids_from_water_quality():
    try:
        ids = db_manager.get_all_ids_from_water_quality()
        return {"ids": ids}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sample/{sample_id}")
async def get_sample(sample_id: int):
    try:
        sample = predictor.get_sample(sample_id)
        return sample.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predict/{sample_id}")
async def predict_sample(sample_id: int):
    try:
        sample = predictor.get_sample(sample_id)
        sample_tensor = predictor.preprocess_sample(sample)
        prediction = predictor.predict(sample_tensor)
        interpreted_prediction = predictor.interpret_prediction(prediction)
        return interpreted_prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/last_water_quality")
async def get_last_water_quality_and_potability():
    # Fetch the last water quality data
    last_data = db_manager.get_last_water_quality_and_potability()
    if last_data:
        # Extract id and features
        id = last_data['id']
        features = last_data['features']
        
        # Convert features list to a TensorFlow tensor
        features_tensor = tf.convert_to_tensor(features, dtype=tf.float32)
        
        # Reshape tensor for prediction
        features_tensor = tf.reshape(features_tensor, (1, -1))
        
        # Make prediction using the loaded model
        prediction = predictor.predict(features_tensor)
        
        # Interpret the prediction
        interpreted_prediction = predictor.interpret_prediction(prediction)
        
        # Check if a prediction entry for this ID already exists
        existing_row = db_manager.get_row_by_id('potability', id)
        if existing_row:
            # If it exists, you might want to update it or handle it differently
            print(f"Existing prediction for ID {id}: {existing_row}")
        else:
            # Add the prediction result to the potability table
            db_manager.add_prediction(id, interpreted_prediction['class_name'], interpreted_prediction['prediction'])
        
        # Return the prediction result and last data
        return {
            'Last data from water Quality': last_data,
            'prediction': interpreted_prediction  # Ensure it is JSON serializable
        }
    else:
        raise HTTPException(status_code=404, detail="No data found.")

@app.get("/get_row/{table_name}/{row_id}")
async def get_row(table_name: str, row_id: int):
    try:
        row = db_manager.get_row_by_id(table_name, row_id)
        if row:
            return {"row": row}
        else:
            raise HTTPException(status_code=404, detail="Row not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

