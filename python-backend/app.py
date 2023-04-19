import json
import mysql.connector

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Database connection
conn = mysql.connector.connect(
    user="rikuhel",
    password="1234",
    host="mysql.metropolia.fi",
    port=3306,
    database="rikuhel",
    autocommit=True
)

@app.route('/airport/coordinates/all')
# Fetches coordinates for all airports
def get_all_airport_coordinates():
    sql = f'SELECT name, latitude_deg, longitude_deg, ident FROM airport'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    
    airport_coordinates = []
    for row in result:
        airport_coordinates.append(row)
    
    return airport_coordinates


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
