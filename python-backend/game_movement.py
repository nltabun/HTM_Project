#

from geopy import distance
import math


# Fetches airport name with an ICAO code
def select_airport(connection, location):
    sql = f'SELECT name FROM airport WHERE ident = \'{location}\''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def airport_municipality(connection, location):
    sql = f'SELECT municipality FROM airport WHERE ident = \'{location}\''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    return result


# Fetch a defined number of random airports from airport database. Default 2
# Optionally get coordinates for airports aswell
def random_airports(connection, count=2, coords=0):
    if coords == 0:
        sql = f'SELECT name, ident FROM airport ORDER BY RAND() LIMIT {count}'
    else:
        sql = f'SELECT name, ident, latitude_deg, longitude_deg FROM airport ORDER BY RAND() LIMIT {count}'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
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
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = \'{player_loc}\''

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    
    return result


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
        airport_distance = (row[0], calculate_distance(location_data, player_coordinates), row[1], row[2], row[3])
        if airport_distance[1] != 0:
            distances.append(airport_distance)
    
    return distances


# Makes a list of airports that are in range
def airports_in_range(airport_list, player_movement_per_ap, player_range=0):
    in_range = []

    for row in airport_list:
        if row[1] <= player_range:
            ap_cost = math.ceil(row[1] / player_movement_per_ap)
            row_with_ap = (row[0], row[1], ap_cost, row[2], row[3], row[4])

            in_range.append(row_with_ap)

    return in_range


# Moves player to the desired location
# location_info contains: [0] = airport name, [1] = distance, [2] = ap cost (and currently unused [3]&[4] = airport coordinates), [5] = icao code
def player_movement(player, location_info):  
    try:
        if location_info[5] == player.enemy_location: # For Musk
            raise Exception('Premonition triggered')

        # Update player location, ap and fuel
        player.location = location_info[5]
        player.current_ap -= int(location_info[2])
        player.fuel_consumption(int(location_info[1]))

        return True # Moved succesfully
    except Exception:
        return False # Issues moving


# Determine the distance between the player and Elon Musk, this was defined as one the clues for the game
def clue_distance_to_musk(connection, player, musk):
    musk = get_player_coordinates(connection, musk.location)
    player = get_player_coordinates(connection, player.location)

    return f'Your distance to musk is {int(distance.distance(musk, player).km)} kilometers'

