from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

# Replace 'your_connection_string' with your actual MongoDB connection string
client = MongoClient('mongodb+srv://gatwaza:rGi31HknO0g3OXrt@cluster0.pa5u5ln.mongodb.net/')
db = client['water_quality_db']

# Create collections
users = db['users']
locations = db['locations']
water_quality = db['water_quality']

# Create indexes for fast lookup
users.create_index([('email', ASCENDING)], unique=True)
locations.create_index([('name', ASCENDING)], unique=True)

# Sample data insertion
# Insert a user
user_id = users.insert_one({
    "name": "John Doe",
    "email": "johndoe@example.com",
    "profession": "Hydrologist"
}).inserted_id
print(f'Inserted User ID: {user_id}')

# Insert a location
location_id = locations.insert_one({
    "name": "Lakeview",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "address": "123 Lakeview Drive"
}).inserted_id
print(f'Inserted Location ID: {location_id}')

# Insert a water quality record
water_quality_id = water_quality.insert_one({
    "location_id": location_id,
    "user_id": user_id,
    "ph": 7.0,
    "Hardness": 150,
    "Solids": 1000,
    "Chloramines": 4.0,
    "Sulfate": 200,
    "Conductivity": 450,
    "Organic_carbon": 20.0,
    "Trihalomethanes": 80.0,
    "Turbidity": 1.0,
    "Potability": None
}).inserted_id
print(f'Inserted Water Quality Record ID: {water_quality_id}')

# Assuming `prediction` is the result from your ML model
prediction = 1  # Example prediction

# Update the water quality record with the prediction
update_result = water_quality.update_one(
    {"_id": water_quality_id},
    {"$set": {"Potability": prediction}}
)
print(f'Matched Count: {update_result.matched_count}, Modified Count: {update_result.modified_count}')

# Fetch and print the updated water quality record
updated_record = water_quality.find_one({"_id": water_quality_id})
print('Updated Water Quality Record:', updated_record)
