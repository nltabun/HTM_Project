
import mysql.connector

from flask import Flask
from flask_cors import CORS

#import game

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

@app.route('/airport/name/<location>')
def select_airport(location):
    sql = f'SELECT name FROM airport WHERE ident = "{location}"'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

@app.route('/airport/name/random/<count>')
def random_airports(count=2):
    sql = f'SELECT name FROM airport ORDER BY RAND() LIMIT {count}'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

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

@app.route('/movement/<player_id>/<location>')
def movement(player_id, location):
    try:
        player = player_id
        query = f'SELECT ident FROM airport WHERE name LIKE "{location}"'

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        #result = str(result).strip('[(\',)]')

        #if result == player.enemy_location:
        #    raise Exception
        
        return result
        #player.current_ap -= 1 #temp
        #player.fuel_consumption(distance=1) #temp

    except Exception:
        return 'Error'

def run_app():
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
