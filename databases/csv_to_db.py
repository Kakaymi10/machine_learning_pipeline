import pandas as pd
import random
import mysql.connector
from db_connection import get_database_connection

def add_water_quality_record(data):
    db = get_database_connection()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute('USE water_quality')
            cursor.execute("""
                INSERT INTO water_quality (id, user_id, location_id, ph, hardness, solids, chloromines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, portability)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            db.commit()
            print(f"Water quality record {data[0]} added successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to add water quality record {data[0]}: {err}")
        finally:
            db.commit()
            cursor.close()
            db.close()
    else:
        print("Failed to connect to the database.")

def main():
    df = pd.read_csv('datapoints.csv')

    user_ids = [1, 2, 3, 4, 5]
    location_ids = [1, 2, 3, 4, 5]
    
    df['id'] = range(1, len(df) + 1)
    
    for index, row in df.iterrows():
        data = (
            row['id'],
            random.choice(user_ids),
            random.choice(location_ids),
            row['ph'],
            row['Hardness'],
            row['Solids'],
            row['Chloramines'],
            row.get('Sulfate', None),
            row['Conductivity'],
            row['Organic_carbon'],
            row['Trihalomethanes'],
            row['Turbidity'],
            row['Potability']
        )
        add_water_quality_record(data)

if __name__ == "__main__":
    main()
