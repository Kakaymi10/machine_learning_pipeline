import mysql.connector
from dotenv import load_dotenv
import os

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT')
        self.database_name = os.getenv('DB_NAME')
        self.connection = None

    def get_database_connection(self):
        if self.connection and self.connection.is_connected():
            return self.connection
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database_name
            )
            print(f'Successfully connected to Server {self.connection}')
            return self.connection
        except Exception as err:
            print(f'An error occurred: {err}')
            return None

    def add_data(self, table_name, data):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(sql, tuple(data.values()))
                db.commit()
                print(f"Data added successfully to table '{table_name}'.")
            except mysql.connector.Error as err:
                print(f"Failed to add data to table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def delete_data(self, table_name, condition):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                sql = f"DELETE FROM {table_name} WHERE {condition}"
                cursor.execute(sql)
                db.commit()
                print(f"Data deleted successfully from table '{table_name}' where {condition}.")
            except mysql.connector.Error as err:
                print(f"Failed to delete data from table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def drop_column(self, table_name, column_name):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
                cursor.execute(sql)
                db.commit()
                print(f"Column '{column_name}' dropped successfully from table '{table_name}'.")
            except mysql.connector.Error as err:
                print(f"Failed to drop column '{column_name}' from table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")
            
    def add_column(self, table_name, column_name, column_type):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                cursor.execute(sql)
                db.commit()
                print(f"Column '{column_name}' added successfully to table '{table_name}'.")
            except mysql.connector.Error as err:
                print(f"Failed to add column '{column_name}' to table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def create_potability_table(self):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                sql = """
                    CREATE TABLE IF NOT EXISTS potability (
                        id INT PRIMARY KEY,
                        result VARCHAR(255) NOT NULL,
                        FOREIGN KEY (id) REFERENCES water_quality(id)
                    )
                """
                cursor.execute(sql)
                db.commit()
                print("Table 'potability' created successfully.")
            except mysql.connector.Error as err:
                print(f"Failed to create table 'potability': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def update_data(self, table_name, data, condition):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                query = f"UPDATE {table_name} SET "
                params = []
                for key, value in data.items():
                    query += f"{key} = %s, "
                    params.append(value)
                query = query.rstrip(", ")
                query += f" WHERE {condition}"
                cursor.execute(query, params)
                db.commit()
                print(f"Data in table '{table_name}' updated successfully where {condition}.")
            except mysql.connector.Error as err:
                print(f"Failed to update data in table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def get_all_tables(self):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                return [table[0] for table in tables]
            except mysql.connector.Error as err:
                print(f"Failed to retrieve tables: {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def get_specific_table(self, table_name):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute(f"SELECT * FROM {table_name}")
                result = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]
                return [dict(zip(column_names, row)) for row in result]
            except mysql.connector.Error as err:
                print(f"Failed to retrieve data from table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def get_all_ids_from_water_quality():
        db = self.get_database_connection()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute("SELECT id FROM water_quality")
                ids = cursor.fetchall()
                return [id[0] for id in ids]
            except mysql.connector.Error as err:
                print(f"Failed to retrieve IDs from water_quality: {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")

    def get_last_water_quality_and_potability(self):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor(dictionary=True)
            try:
                # Fetch the last row from water_quality
                cursor.execute("""
                    SELECT id, ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity
                    FROM water_quality
                    ORDER BY id DESC
                    LIMIT 1
                """)
                last_water_quality = cursor.fetchone()

                # Fetch the result from potability
                if last_water_quality:
                    id = last_water_quality['id']
                    cursor.execute("""
                        SELECT result
                        FROM potability
                        WHERE id = %s
                    """, (id,))
                    result = cursor.fetchone()

                    # Add result to the last_water_quality data
                    last_water_quality['result'] = result['result'] if result else None

                    # Convert features to TensorFlow tensor
                    features = [
                        last_water_quality['ph'],
                        last_water_quality['Hardness'],
                        last_water_quality['Solids'],
                        last_water_quality['Chloramines'],
                        last_water_quality['Sulfate'],
                        last_water_quality['Conductivity'],
                        last_water_quality['Organic_carbon'],
                        last_water_quality['Trihalomethanes'],
                        last_water_quality['Turbidity']
                    ]
                    
                    
                    # Add tensor data to the response
                    last_water_quality['features'] = features  # Convert tensor to list for JSON serialization
                    
                    return last_water_quality
                else:
                    return None

            except mysql.connector.Error as err:
                print(f"Failed to retrieve last water quality and potability data: {err}")
                return None
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")
            return None
    
    def get_row_by_id(self, table_name, row_id):
        db = self.get_database_connection()
        if db:
            cursor = db.cursor(dictionary=True)
            try:
                sql = f"SELECT * FROM {table_name} WHERE id = %s"
                cursor.execute(sql, (row_id,))
                result = cursor.fetchone()
                return result
            except mysql.connector.Error as err:
                print(f"Failed to retrieve row from table '{table_name}': {err}")
            finally:
                cursor.close()
                db.close()
        else:
            print("Failed to connect to the database.")
            return None