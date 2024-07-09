import mysql.connector
from db_connection import get_database_connection

def add_user(user_id, name, email, profession=None):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            cursor.execute("""
                INSERT INTO user (user_id, name, email, profession)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, profession))
            db.commit()
            print(f"User '{name}' added successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to add user '{name}': {err}")
        finally:
            db.commit()
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")


def add_location(location_id, name, latitude, longitude, address):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            cursor.execute("""
                INSERT INTO location (location_id, name, latitude, longitude, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (location_id, name, latitude, longitude, address))
            db.commit()
            print(f"Location '{name}' added successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to add location '{name}': {err}")
        finally:
            db.commit()
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")

users = [
    (1, 'Robert', 'robert@email.com'),
    (2, 'Elsie', 'elsie@email.com'),
    (3, 'Kingsley', 'kingsley@email.com'),
    (4, 'David', 'david@email.com'),
    (5, 'Moussa', 'moussa@email.com')
]

for user in users:
    add_user(*user)
    
locations = [
    (1, 'Location1', '12.9715987', '77.594566', 'Address 1'),
    (2, 'Location2', '28.7040592', '77.1024902', 'Address 2'),
    (3, 'Location3', '19.0760', '72.8777', 'Address 3'),
    (4, 'Location4', '51.5074', '-0.1278', 'Address 4'),
    (5, 'Location5', '40.7128', '-74.0060', 'Address 5')
]

for location in locations:
    add_location(*location)