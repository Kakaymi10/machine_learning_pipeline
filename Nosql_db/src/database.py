from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority")
    return client['water_quality_db']

def create_collections(db):
    db.create_collection("users")
    db.create_collection("locations")
    db.create_collection("water_quality")

if __name__ == "__main__":
    db = get_database()
    create_collections(db)
