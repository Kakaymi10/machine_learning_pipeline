import mysql.connector
from db_connection import get_database_connection

def add_user(new_username, new_password):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute(f"CREATE USER '{new_username}'@'%' IDENTIFIED BY '{new_password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{new_username}'@'%' WITH GRANT OPTION")
            cursor.execute("FLUSH PRIVILEGES")
            db.commit()
            print(f"User '{new_username}' created and granted all privileges.")
        except mysql.connector.Error as err:
            print(f"Failed to add user: {err}")
        finally:
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")

add_user('jeanrobert', 'jeanrobert')