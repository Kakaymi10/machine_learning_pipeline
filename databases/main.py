# import modules

import mysql.connector
import os

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')


database = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

print(database)