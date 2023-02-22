import mysql.connector
from geopy import distance


connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='HTM',
         user='root',
         password='',
         autocommit=True
         )



