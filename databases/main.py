'''
This Script connects to a remote mysql server and 
'''
import mysql.connector
import os

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

try:
    database = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print(f'Succesfully connected to Database: {database}')
except Exception as err:
    print(f'An error occured: {err}')