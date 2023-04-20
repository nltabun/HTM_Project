
import config
import json

from flask import Flask
from flask_cors import CORS

#import game
import game_data

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
def test():
    print(player)
    print(musk)

    return 'test'

@app.route('/load-game/<id>')
def load_game(id):
    player_obj, musk_obj = game_data.load_game_table_data(config.conn, int(id))
    global player
    player = player_obj
    global musk
    musk = musk_obj

    #test
    #print(player)
    #print(musk)

    save = []

    return [player.name, musk.name]


@app.route('/airport/name/<location>')
def select_airport(location):
    sql = f'SELECT name FROM airport WHERE ident = {location}'
    cursor = config.conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result


@app.route('/locate/<pid>')
def player_location_name(pid):
    
    if pid == '0':
        location = player.location
        print(location)
    elif pid == '1':
        location = musk.location
    else:
        pass

    airport = select_airport(location)
    print(airport)

    data = {
        "location": location,
        "name": airport[0]
    }

    return json.dumps(data)


@app.route('/airport/name/random/<count>')
def random_airports(count=2):
    sql = f'SELECT name FROM airport ORDER BY RAND() LIMIT {count}'
    cursor = config.conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

@app.route('/airport/coordinates/all')
# Fetches coordinates for all airports
def get_all_airport_coordinates():
    sql = f'SELECT name, latitude_deg, longitude_deg, ident FROM airport'
    
    cursor = config.conn.cursor()
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
        print(location)
        query = f'SELECT ident FROM airport WHERE name LIKE "{location}"'

        cursor = config.conn.cursor()
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

if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
