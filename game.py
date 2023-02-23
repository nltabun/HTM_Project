import mysql.connector
from geopy import distance


connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='HTM_Database',
         user='root',
         password='Salasana1!',
         autocommit=True
         )



def select_airports():
    sql = "SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE continent = NA"
    cursor = conn.cursor(Dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result
