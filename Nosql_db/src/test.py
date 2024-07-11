import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to the MongoDB cluster
client = MongoClient(MONGODB_URI)
db = client.water_quality_db

# Collections
users = db.users
locations = db.locations
water_quality = db.water_quality

# Create unique index on email for users
users.create_index([('email', ASCENDING)], unique=True)
# Create unique index on name for locations
locations.create_index([('name', ASCENDING)], unique=True)

# Insert a user
user_id = users.insert_one({
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'profession': 'Researcher'
}).inserted_id
print(f"Inserted User ID: {user_id}")

# Insert a location, handle duplicate key error
location_name = 'Lakeview'
try:
    location_id = locations.insert_one({
        'name': location_name,
        'latitude': -1.2921,
        'longitude': 36.8219,
        'address': '123 Lakeview St.'
    }).inserted_id
    print(f"Inserted Location ID: {location_id}")
except DuplicateKeyError:
    location_id = locations.find_one({'name': location_name})['_id']
    print(f"Location already exists. Using existing Location ID: {location_id}")

# Insert a water quality record
water_quality_id = water_quality.insert_one({
    'location_id': location_id,
    'user_id': user_id,
    'ph': 7.0,
    'Hardness': 150,
    'Solids': 1000,
    'Chloramines': 4.0,
    'Sulfate': 200,
    'Conductivity': 450,
    'Organic_carbon': 20.0,
    'Trihalomethanes': 80.0,
    'Turbidity': 1.0,
    'Potability': None  # Initially set to NULL
}).inserted_id
print(f"Inserted Water Quality Record ID: {water_quality_id}")

# Update the water quality record with potability
result = water_quality.update_one(
    {'_id': water_quality_id},
    {'$set': {'Potability': 1}}
)
print(f"Matched Count: {result.matched_count}, Modified Count: {result.modified_count}")

# Retrieve and print the updated record
updated_record = water_quality.find_one({'_id': water_quality_id})
print(f"Updated Water Quality Record: {updated_record}")
