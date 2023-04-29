import config
import json
import random
import requests

from flask import Flask
from flask_cors import CORS

import game_init
import game_data
import game_movement
import game_fuel
import game_events
import game_actions
import game_events
import game_planes


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
def test():
    print(player)
    print(musk)

    return 'test'


# For getting active saves or current highest game id # TODO: Maybe reformat returns
@app.route('/save-data/<param>')
def check_for_save_data(param):
    # Return info for all active games
    if param == 'info': 
        query = f'SELECT screen_name, id FROM game WHERE NOT screen_name = "Elon Musk"'

        cursor = config.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result
    # Get current highest game id
    elif param == 'max-id':
        query = f'SELECT MAX(id) FROM game'

        cursor = config.conn.cursor()
        cursor.execute(query)
        result = str(cursor.fetchone()).strip('(,)')

        return result
    else:

        result = ''

        return result


# Create a new game
# Parameters: player name and desired game length
# Returns new game id
@app.route('/new-game/<name>&<game_length>')
def new_game(name, game_length):
    saves = int(check_for_save_data('max-id'))
    new_game_id = saves + 1
    
    game_init.new_game(config.conn, name, game_length, new_game_id)

    print(f'New game created with id {new_game_id}')
    return json.dumps({"id" : new_game_id})


# Loads game data from the database using game id and initializes player, musk and plane list globally
# Also calls and returns player data in JSON using refresh_player_data function
@app.route('/load-game/<id>')
def load_game(id):
    player_obj, musk_obj = game_data.load_game_table_data(config.conn, int(id))
    global player
    player = player_obj
    global musk
    musk = musk_obj

    global plane_list
    plane_list = game_init.generate_airplanes()

    return refresh_player_data()


# Return player data in JSON
@app.route('/refresh-player-data')
def refresh_player_data():
    try:
        data = player.stats()
        data.update({"status" : 1})

        return json.dumps(data)
    except:
        return json.dumps({"status" : 0})


# Returns a list of all the airports in range (default: Player)
# If parameter return_format=0 then return in JSON (default)
@app.route('/airport-in-range/')
def airports_in_range(current_player=1, return_format=0):
    if current_player == 1: # If default then use globally defined player
        current_player = player

    airport_list = game_movement.get_all_airport_coordinates(config.conn)
    start_loc = game_movement.get_player_coordinates(config.conn, current_player.location)
    airports = game_movement.calculate_all_airport_distance(airport_list, start_loc)
    in_range_list = game_movement.airports_in_range(airports, current_player.travel_speed, current_player.range())

    if return_format == 0:
        formatted_list = []
        for airport in in_range_list:
            data = {
                "name" : airport[0],
                "icao" : airport[5],
                "distance" : airport[1],
                "apCost" : airport[2],
                "latitude_deg" : airport[3],
                "longitude_deg" : airport[4]
            }
            formatted_list.append(data)

        return json.dumps(formatted_list)
    else:
        return in_range_list


# Save game data back to the database
# Return status = 1 if no issues, otherwise 0
@app.route('/save-game')
def save_game():
    save = game_data.save_to_game_table()

    return json.dumps(save)


# Get airport name from airport database with icao-code
# Return icao-code and airport name in JSON
@app.route('/airport/name/<ident>')
def select_airport(ident):
    airport = game_movement.select_airport(config.conn, ident)

    data = {
        "icao": ident,
        "name": str(airport[0]).strip("(),'")
    }

    return json.dumps(data)


# Locate a player. Pid: 0=Player; 1=Musk
# Return icao-code and airport name in JSON
@app.route('/locate/<pid>')
def start_location_name(pid):
    if pid == '0': # Player
        ident = player.location
    elif pid == '1': # Musk
        ident = musk.location
    else: # Invalid pid
        return json.dumps({"status" : 0})
    
    return select_airport(ident)


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


@app.route('/weather/<location>')
def get_weather_data(location):
    api_key = 'f08355556ae585e753c3498c6cc4756c'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        visibility = weather_data['visibility']
        weather_data = {
            'temperature': temp,
            'weather_desc': weather_desc,
            'wind_speed': wind_speed,
            'visibility': visibility
        }
        return json.dumps(weather_data)

    else:
        return json.dumps('PERKELE ei tänne!')


# Moves player to <location>
# Returns new player location and if the player won with their move.
# status = 2 for win, 1 to continue game, 0 if failed to move
@app.route('/movement/<location>')
def movement(location):
    try:
        # Get non-formatted version of the list with airports in range
        in_range = airports_in_range(return_format=1)

        # Check that the attempted move is legal
        legal_move = False
        for airport in in_range:
            if airport[5] == location: # Location is in range
                legal_move = True
                target = airport
                break
        if legal_move == False:
            raise Exception('Illegal move')

        # Make the actual move. Returns if successful
        move = game_movement.player_movement(player, target)
        
        events(player)

        if move: # If the move was successful
            if player.location == musk.location: # Player found Musk and wins the game
                status = 2
            else: # Otherwise continue game
                status = 1
            
            data = {
                "location": player.location,
                "status": status
            }

            return json.dumps(data)
        else:
            raise Exception('Failed to move')
    except Exception:
        return json.dumps({"status" : 0})
        

# For buying and loading fuel
# Parameters: action = whether to buy or load
# amount = how much to buy or load
@app.route('/fuel-management/<action>=<amount>')
def fuel_management(action, amount):
    try:
        if action == 'buy': # Returns if successful and both old and new fuel & money values
            return json.dumps(game_fuel.buy_fuel(player, int(amount)))
        elif action == 'load': # Returns if successful and both old and new fuel values
            return json.dumps(game_fuel.load_fuel(player, int(amount)))
        else:
            raise Exception('Invalid action')
    except Exception:
        return json.dumps({"status" : "burger"})
    

# Start a minigame. Returns an id, question and four possible answers
@app.route('/minigame/play')
def play_minigame():
    result = game_actions.play_minigame(config.conn)

    # Reset minigames if all have been previously completed
    if result[1] == -1:
        game_init.reset_minigames(config.conn)

    return json.dumps(result[0])
    

# For answering questions from the minigames. Parameters: question id, inputted answer
# Returns whether or not answer is correct and reward if correct
@app.route('/minigame/answer/<qid>=<answer>')
def answer_minigame(qid, answer):
    return json.dumps(game_actions.answer_minigame(config.conn, player, qid, answer))


# Buy clues. Return status (1=successful, 0=not), clue type and the clue itself
@app.route('/clues')
def buy_clue():
    # Make sure the player has enough money and return status 0 (fail) if not so.
    if player.money < 100:
        return json.dumps({"status" : 0})
    if player.bought_clue == 1:
        return json.dumps({"status": 0})
    
    clue = game_actions.buy_clue(config.conn, player, musk)

    return json.dumps(clue)


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
    

# For browsing all available planes
# Returns all planes
@app.route('/planes/browse')
def browse_planes():
    planes = game_planes.get_plane_data(player)
    return json.dumps(planes)


# Compare current plane vs selected plane
# Parameters: current plane index, selected plane index
# Returns stats for both planes and cost to upgrade
@app.route('/planes/compare/<current_idx>=<selected_idx>')
def compare_planes(current_idx, selected_idx):
    current_plane = plane_list[int(current_idx)]
    selected_plane = plane_list[int(selected_idx)]
    planes = game_planes.compare_planes(current_plane, selected_plane)
    
    return json.dumps(planes)


# Buy the selected plane using plane index
# Return status = 1 if successful, 0 if not
@app.route('/planes/buy=<index>')
def buy_plane(index):
    selected_plane = plane_list[int(index)]
    purchase = game_planes.buy_plane(player, selected_plane)
    
    return json.dumps(purchase)


# Ends the players turn and plays out Musks turn.
@app.route('/end-turn')
def end_turn():
    player.decrease_turns() # Player turns_left -1

    musk_status = musk_actions() # Musk plays his turn

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
        return 0 # End game

    musk.current_ap = musk.max_ap  # Reset Musk ap
    musk.epitaph(player.location)  # Refresh Musks future sight

    # Fuel up if currently low
    if musk.plane.current_fuel <= 10000:
        game_fuel.load_fuel(musk)

    # Musk Movement
    try:
        in_range = airports_in_range(musk, 1)

        # Randomize an airport from the list
        if len(in_range) != 0:
            n = random.randint(0, len(in_range) - 1)
            print(str(n) + '/' + str(len(in_range) - 1))
        else:
            raise Exception('No airports in range')

        target = in_range[n]  # Target airport info

        game_movement.player_movement(musk, target)
    except Exception:
        print('Musk encountered issues while trying to move.')

    musk.decrease_turns()  # Turn over

    return 1 # Continue game


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
