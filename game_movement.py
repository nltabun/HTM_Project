#

from geopy import distance
import random

# Fetches all airports that are located in the Northen america
def select_airport(connection):
    sql = f'SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE continent = "NA"'
    cursor = connection.cursor(Dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

# Fetches players ICAO code
def player_location_name(connection, player):
    location = str(player.location).strip("''")
    sql = f'SELECT name FROM airport WHERE ident = "{location}"'

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    return result

# Fetches players coordinates
def get_player_coordinates(connection, player_loc):
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = {player_loc}'

    cursor = connection.cursor()
    cursor.execute(sql)
    tulos = cursor.fetchone()
    #  print(f'Get player coord: {tulos}\n')
    
    return tulos

# Fetches coordinates for all airports
def get_all_airport_coordinates(connection):
    sql = f'SELECT name, latitude_deg, longitude_deg, ident FROM airport'
    
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    airport_coordinates = []
    for row in result:
        airport_coordinates.append(row)
    
    return airport_coordinates

# Does the calculation between the player and an airport.
def calculate_distance(location_data, player_location):
    player_coordinates = (player_location[0], player_location[1])
    airport_location = (location_data[0], location_data[1])
    
    return float(distance.distance(airport_location, player_coordinates).km)

# Calculates the distance between the player and all airports
def calculate_all_airport_distance(airport_list, player_coordinates):
    distances = []
    
    for row in airport_list:
        location_data = (row[1], row[2])
        airport_distance = (row[0], calculate_distance(location_data, player_coordinates))
        distances.append(airport_distance)
    
    return distances

# Makes a list of airports that are in a 1000km radius of the player
def airports_in_range(airport_list):
    in_range = []
    
    for row in airport_list:
        if row[1] <= 1000:
            in_range.append(row)
    
    return in_range

# Defines the players movement
def player_movement(connection, player):
    airport_list = calculate_all_airport_distance(get_all_airport_coordinates(connection), get_player_coordinates(connection, player.location))
    in_range = airports_in_range(airport_list) # TODO list shouldn't contain current airport

    airport_dic = dict()
    i = 1
    # Prints a list of airports that are in range of the player
    if player.id == 'Player':
        for row in in_range:
            print(f'({i}) {row[0]}')
            airport_dic.update({i: row[0]})
            i += 1
        # Asks for the players input on where they want to go
        answer = input(f'Choose your destination (Type "C" to cancel): ')
        # Returns if the player wants to cancel the search
        if answer.capitalize() == 'C':
            return
    # Randomly chooses an airport for musk to move to.
    elif player.id == 'Musk':
        for row in in_range:
            airport_dic.update({i: row[0]})
            i += 1

        answer = random.randint(1, i-1)
    else:
        print('Invalid player id')
    
    try:
        if 0 < int(answer) <= len(in_range): 
            query = f'SELECT ident FROM airport WHERE name LIKE "{airport_dic.get(int(answer))}"'
    
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = str(result).strip('[('',)]')

            player.location = result
        else:
            raise Exception
    except:
        print('\nInvalid value\n')
        player_movement(connection, player)

    if player.id == 'Musk':
        print(f'Musk has moved to {result}\n')
 

# Determine the distance between the player and Elon Musk, this was defined as one the clues for the game
def clue_distance_to_musk(connection, player, musk):
    musk = get_player_coordinates(connection, musk.location)
    player = get_player_coordinates(connection, player.location)

    return f'Your distance to musk is {int(distance.distance(musk, player).km)} kilometers'


def decrease_turns(player):
    player.turns_left = player.turns_left - 1



