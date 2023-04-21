#

from geopy import distance
import random
import math
import game_actions

# Fetches airport name with an ICAO code
def select_airport(connection, location):
    sql = f'SELECT name FROM airport WHERE ident = \'{location}\''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def random_airports(connection, count=2):
    sql = f'SELECT name FROM airport ORDER BY RAND() LIMIT {count}'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    result = set(result)
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
        airport_distance = (row[0], calculate_distance(location_data, player_coordinates), row[1], row[2])
        if airport_distance[1] != 0:
            distances.append(airport_distance)
    
    return distances

# Makes a list of airports that are in range
def airports_in_range(airport_list, player_movement_per_ap, player_range=0):
    in_range = []

    for row in airport_list:
        if row[1] <= player_range:
            ap_cost = math.ceil(row[1] / player_movement_per_ap)
            row_with_ap = (row[0], row[1], ap_cost, row[2], row[3])
            
            in_range.append(row_with_ap)
    
    return in_range

# Defines the players movement
def player_movement(connection, player):
    airport_list = calculate_all_airport_distance(get_all_airport_coordinates(connection), get_player_coordinates(connection, player.location))
    in_range = airports_in_range(airport_list, player.travel_speed, player.range())

    airport_dic = dict()
    i = 0
    # Prints a list of airports that are in range of the player
    if player.name != 'Elon Musk':
        for row in in_range:
            i += 1
            airport_coords = (row[3], row[4])
            print(f'({i}) {row[0]} | Distance: {int(row[1])} | AP Cost: {row[2]} | Direction: {game_actions.get_bearing(get_player_coordinates(connection, player.location), airport_coords)}')

            airport_dic.update({i: (row[0], row[2], row[1])})
        # Asks for the players input on where they want to go
        answer = input(f'Choose your destination (Type "C" to cancel): ')
        # Returns if the player wants to cancel the search
        if answer.capitalize() == 'C':
            return
    # Randomly chooses an airport for musk to move to.
    else:
        for row in in_range:
            i += 1
            airport_dic.update({i: (row[0], row[2], row[1])})

        if i != 0:
            answer = random.randint(1, i)
        else:
            answer = i
    
    try:
        if 0 < int(answer) <= len(in_range): 
            query = f'SELECT ident FROM airport WHERE name LIKE "{airport_dic.get(int(answer))[0]}"'
    
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = str(result).strip('[('',)]')

            if result == player.enemy_location:
                raise Exception

            player.location = result
            player.current_ap -= airport_dic.get(int(answer))[1]
            player.fuel_consumption(airport_dic.get(int(answer))[2])

        else:
            raise Exception
    except:
        if player.name != 'Elon Musk':
            print('\nInvalid value\n')
            player_movement(connection, player)
        else:
            return


# Determine the distance between the player and Elon Musk, this was defined as one the clues for the game
def clue_distance_to_musk(connection, player, musk):
    musk = get_player_coordinates(connection, musk.location)
    player = get_player_coordinates(connection, player.location)

    return f'Your distance to musk is {int(distance.distance(musk, player).km)} kilometers'

