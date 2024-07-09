'''
This Script connects to a remote mysql server and 
'''
import mysql.connector
import os

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

def get_database_connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print(f'Succesfully connected to Database: {conn}')
        return  conn
    except Exception as err:
        print(f'An error occured: {err}')
        return None