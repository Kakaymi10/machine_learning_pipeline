import mysql.connector
from db_connection import get_database_connection

try:
    conn = get_database_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS water_quality")
        cursor.execute("USE water_quality")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE,
                profession VARCHAR(50)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS location (
                location_id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                latitude VARCHAR(255),
                longitude VARCHAR(255),
                address VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS water_quality (
                id INT NOT NULL PRIMARY KEY,
                user_id INT NOT NULL,
                location_id INT NOT NULL,
                ph FLOAT,
                hardness FLOAT,
                solids FLOAT,
                chloromines FLOAT,
                sulfate FLOAT,
                conductivity FLOAT,
                organic_carbon FLOAT,
                trihalomethanes FLOAT,
                turbidity FLOAT,
                portability FLOAT,
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (location_id) REFERENCES location(location_id)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created successfully.")
except mysql.connector.Error as err:
    print(f"There was an error: {err}")
