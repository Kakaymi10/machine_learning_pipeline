from pymongo import MongoClient, ASCENDING

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to the MongoDB cluster
client = MongoClient(MONGODB_URI)
db = client.water_quality_db

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
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'profession': 'Researcher'
}).inserted_id

# Insert a location
location_id = locations.insert_one({
    "name": "Lakeview",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "address": "123 Lakeview Drive"
}).inserted_id

# Insert a water quality record
water_quality.insert_one({
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
})
