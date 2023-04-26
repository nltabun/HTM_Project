import config
import json
import random
import math

from flask import Flask, request
from flask_cors import CORS
from geopy import distance

import game_init
import game_data
import game_movement
import game_fuel
import game_events

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

        return result
    else:

        result = ''

        return result


@app.route('/new-game/<name>&<game_length>')
def new_game(name, game_length):
    saves = int(check_for_save_data('max-id'))
    new_game_id = str(saves + 1)
    game_init.new_game(config.conn, name, game_length)

    print(f'New game created with id {new_game_id}')
    return new_game_id


@app.route('/load-game/<id>')
def load_game(id):
    player_obj, musk_obj = game_data.load_game_table_data(config.conn, int(id))
    global player
    player = player_obj
    global musk
    musk = musk_obj

    return refresh_player_data()


@app.route('/refresh-player-data')
def refresh_player_data():
    data = {
        "id": player.id,
        "name": player.name,
        "location": player.location,
        "money": player.money,
        "fuelReserve": player.fuel_reserve,
        "ap": player.current_ap,
        "minigameDone": player.done_minigame,
        "clueBought": player.bought_clue,
        "turns": player.turns_left,
        "plane": player.plane.name,
        "fuelCurrent": player.plane.current_fuel,
        "fuelCapacity": player.plane.fuel_capacity,
        "fuelEfficiency": player.plane.fuel_efficiency,
        "speed": player.plane.speed,
        "range": player.range()
    }

    return json.dumps(data)


@app.route('/airport-in-range/')
def airports_in_range(current_player=1, return_format=1):
    if current_player == 1:  # If default then use globally defined player
        current_player = player

    airport_list = game_movement.get_all_airport_coordinates(config.conn)
    start_loc = game_movement.get_player_coordinates(config.conn, current_player.location)
    airports = game_movement.calculate_all_airport_distance(airport_list, start_loc)
    airport_name = game_movement.airports_in_range(airports, current_player.travel_speed, current_player.range())

    if return_format != 1:
        return json.dumps(airport_name)
    else:
        return airport_name


@app.route('/save-game')
def save_game():
    game_data.save_to_game_table()

    return 'saved'


@app.route('/airport/name/<ident>')
def select_airport(ident):
    airport = game_movement.select_airport(config.conn, ident)

    data = {
        "icao": ident,
        "name": str(airport[0]).strip("(),'")
    }

    return json.dumps(data)


@app.route('/locate/<pid>')
def start_location_name(pid):
    if pid == '0':
        ident = player.location
    elif pid == '1':
        ident = musk.location
    else:
        pass

    airport = select_airport(ident)

    return airport


@app.route('/airport/name/random/<count>')
def random_airports(count=2):
    sql = f'SELECT name FROM airport ORDER BY RAND() LIMIT {count}'
    cursor = config.conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return json.dumps(result)


@app.route('/airport/coordinates/all')
# Fetches coordinates for all airports
def get_all_airport_coordinates():
    sql = f'SELECT name, latitude_deg, longitude_deg, ident FROM airport'

    cursor = config.conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    airport_coordinates = []
    for row in result:
        airport_coordinates.append({
            "name": row[0],
            "latitude_deg": row[1],
            "longitude_deg": row[2],
            "ident": row[3]
        })

    return json.dumps(airport_coordinates)


@app.route('/movement/<location>')
def movement(location):
    try:
        in_range = airports_in_range()

        legal_move = False
        for airport in in_range:
            if airport[5] == location:
                legal_move = True
                target = airport
                break
        if legal_move == False:
            raise Exception('Illegal move')

        print(target)
        move = game_movement.player_movement(player, target)

        if move:
            if player.location == musk.location:  # Player wins the game
                status = 0
            else:  # Game continues
                status = 1
            data = {
                "location": player.location,
                "status": status
            }
            return json.dumps(data)
        else:
            raise Exception('Failed to move')
    except Exception:
        return 'No move made'


@app.route('/fuel-management/<action>=<amount>')
def fuel_management(action, amount):
    try:
        if action == 'buy':
            return json.dumps(game_fuel.buy_fuel(player, int(amount)))
        elif action == 'load':
            return game_fuel.load_fuel(player, int(amount))
        else:
            raise Exception('Invalid action')
    except Exception:
        return 'Error'


@app.route('/event')
def events(player):
    try:
        if player.location == 'KDTW' or player.location == 'KSTL' or player.location == 'KORD':
            message = game_events.event1(player)
            return message

        elif player.location == 'MHPR' or player.location == 'MMMX' or player.location == 'MMGL':
            message = game_events.event2(player)
            return message
        else:
            raise Exception('XD')
    except Exception:
        return 'Error'



# Ends the players turn and plays out Musks turn.
@app.route('/end-turn')
def end_turn():
    player.decrease_turns()

    musk_status = musk_actions()

    if musk_status == 0:  # Musk wins the game
        return json.dumps({"status": 0})  # Display lost game screen
    else:  # Game continues
        # Reset player ap
        player.current_ap = player.max_ap
        # Reset minigame and clue checks
        player.done_minigame = 0
        player.bought_clue = 0

        return json.dumps({"status": 1})  # Refresh player data and continue game normally


# Defines the actions Musk takes during his turn. Returns whether or not he has won the game: 0 = win, 1 = game continues
def musk_actions():
    if musk.turns_left <= 1:  # Player can't catch Musk anymore so he wins.
        return 0

    musk.current_ap = musk.max_ap  # Reset Musk ap
    musk.epitaph(player.location)  # Refresh Musks future sight

    # Fuel up if currently low
    if musk.plane.current_fuel <= 10000:
        game_fuel.load_fuel(musk)

    # Musk Movement
    try:
        in_range = airports_in_range(musk)

        # Randomize an airport from the list
        if len(in_range) != 0:
            n = random.randint(0, len(in_range) - 1)
            print(str(n) + '/' + str(len(in_range) - 1))
        else:
            raise Exception('No airports in range')

        target = in_range[n]  # Target airport info

        game_movement.player_movement(config.conn, musk, target)
    except Exception:
        print('Musk encountered issues while trying to move.')

    musk.decrease_turns()  # Turn over

    return 1


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
