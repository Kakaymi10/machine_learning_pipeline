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
    
def get_user(user_id):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            cursor.execute("""
                SELECT * FROM user WHERE user_id = %s
            """, (user_id,))
            result = cursor.fetchone()
            if result:
                return {
                    'user_id': result[0],
                    'name': result[1],
                    'email': result[2],
                    'profession': result[3]
                }
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Failed to get user: {err}")
        finally:
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")

def update_user(user_id, name=None, email=None, profession=None):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            query = "UPDATE user SET "
            params = []
            if name:
                query += "name = %s, "
                params.append(name)
            if email:
                query += "email = %s, "
                params.append(email)
            if profession:
                query += "profession = %s, "
                params.append(profession)
            query = query.rstrip(", ")
            query += " WHERE user_id = %s"
            params.append(user_id)
            cursor.execute(query, params)
            db.commit()
            print(f"User '{name}' updated successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to update user: {err}")
        finally:
            db.commit()
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")

def delete_user(user_id):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            cursor.execute("""
                DELETE FROM user WHERE user_id = %s
            """, (user_id,))
            db.commit()
            print(f"User '{user_id}' deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to delete user: {err}")
        finally:
            db.commit()
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")