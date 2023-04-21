
import config
import json

from flask import Flask
from flask_cors import CORS

import game_init
import game_data
import game_movement
import game_fuel


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
def test():
    print(player)
    print(musk)

    return 'test'


@app.route('/save-data/<param>')
def check_for_save_data(param):
    if param == 'info':
        query = f'SELECT screen_name, id FROM game WHERE NOT screen_name = "Elon Musk"'

        cursor = config.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        return result
    elif param == 'max-id':
        query = f'SELECT MAX(id) FROM game'

        cursor = config.conn.cursor()
        cursor.execute(query)
        result = str(cursor.fetchone()).strip('(,)')

        if result == 'None':
            result = '0'
        
        return result
    else:

        result = ''

        return result
    

@app.route('/new-game/<name>&<game_length>')
def new_game(name, game_length):
    saves = int(check_for_save_data('max-id'))
    new_game_id = saves + 1
    game_init.new_game(config.conn, name, game_length, new_game_id)
    
    print(f'New game created with id {new_game_id}')
    return str(new_game_id)


@app.route('/load-game/<id>')
def load_game(id):
    player_obj, musk_obj = game_data.load_game_table_data(config.conn, int(id))
    global player
    player = player_obj
    global musk
    musk = musk_obj

    return [player.name, musk.name]


@app.route('/airport-in-range/')
def airports_in_range():
    airport_list = game_movement.get_all_airport_coordinates(config.conn)
    player_loc = game_movement.get_player_coordinates(config.conn, player.location)
    airports = game_movement.calculate_all_airport_distance(airport_list, player_loc)

    return game_movement.airports_in_range(airports, player.travel_speed, player.range())


@app.route('/save-game')
def save_game():
    game_data.save_to_game_table()

    return 'saved'


@app.route('/airport/name/<ident>')
def select_airport(ident):
    return game_movement.select_airport(config.conn, ident)


@app.route('/locate/<pid>')
def player_location_name(pid):
    
    if pid == '0':
        ident = player.location
    elif pid == '1':
        ident = musk.location
    else:
        pass

    airport = select_airport(ident)
    print(airport)

    data = {
        "location": ident,
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
def all_airport_coordinates():
    return game_movement.get_all_airport_coordinates(config.conn)


@app.route('/movement/<location>')
def movement(location):
    try:
        in_range = airports_in_range()

        legal_move = False
        for airport in in_range:
            if airport[0] == location:
                legal_move = True
                target = airport
                break
        if legal_move == False:
            raise Exception('Illegal move')
        
        print(target)
        move = game_movement.player_movement(config.conn, player, target)
        if move:
            return 'New location ' + player.location
        else:
            raise Exception('Failed to move')
    except Exception:
        return 'No move made'
    

@app.route('/fuel-management/<action>=<amount>')
def fuel_management(action, amount):
    try:
        if action == 'buy':
            return game_fuel.buy_fuel(player, int(amount))
        elif action == 'load':
            return game_fuel.load_fuel(player, int(amount))
        else:
            raise Exception('Invalid action')
    except Exception:
        return 'Error with fuel management system'


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
