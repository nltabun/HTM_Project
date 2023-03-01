#
import game_objects
from geopy import distance
import random



def select_airport(connection):
    sql = f'SELECT iso_country, ident, name, latitude_deg, longitude_deg FROM airport WHERE continent = \'NA\''
    cursor = connection.cursor(Dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def player_location(connection):
    sql = f'SELECT location FROM game WHERE id = \'Player\'' # TODO Get from object not database
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def player_location_name(connection):
    sql = f'SELECT name FROM airport WHERE ident IN(SELECT location FROM game WHERE id = \'Player\')' 
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def get_player_coordinates(player_location, connection):
    player_location = str(player_location).strip('[(,)]')
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = {player_location}'
    cursor = connection.cursor()
    cursor.execute(sql)
    tulos = cursor.fetchall()
    return tulos[0]


def get_all_airport_coordinates(connection):
    sql = f'SELECT name, latitude_deg, longitude_deg, ident FROM airport'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    airport_coordinates = []
    for row in result:
        airport_coordinates.append(row)
    return airport_coordinates


def calculate_distance(location_data, player_location):
    player_coordinates = (player_location[0], player_location[1])
    airport_location = (location_data[0], location_data[1])
    return float(distance.distance(airport_location, player_coordinates).km)


def calculate_all_airport_distance(airport_list, player_coordinates):
    distances = []
    for row in airport_list:
        location_data = (row[1], row[2])
        airport_distance = (row[0], calculate_distance(location_data, player_coordinates))
        distances.append(airport_distance)
    return distances


def airports_in_range(airport_list):
    in_range = []
    for row in airport_list:
        if row[1] <= 1000:
            in_range.append(row)
    return in_range


def player_movement(connection, player):
    player_loc = player_location(connection)
    airport_list = calculate_all_airport_distance(get_all_airport_coordinates(connection), get_player_coordinates(player_loc, connection))
    in_range = airports_in_range(airport_list) # TODO list shouldn't contain current airport
    i = 1
    airport_dic = dict()

    for row in in_range:
        print(f'({i}) {row[0]}')
        airport_dic.update({i:row[0]})
        i+=1
    answer = input(f'Choose your destination: ') # TODO Option to cancel?
    print(answer)
    print(len(in_range))
    try:
        if 0 < int(answer) <= len(in_range): 
            query = f'SELECT ident FROM airport WHERE name LIKE "{airport_dic.get(int(answer))}"'
    
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = str(result).strip('[(,)]')
            print(result)
            placeholder_id = 'Player'

            update = f'UPDATE game SET location = {result} WHERE id = \'{placeholder_id}\'' # TODO Update object not database
            print(update)
            cursor.execute(update)

            player.location = result
        else:
            raise Exception
    except:
        print('\nInvalid value\n')
        player_movement(connection)
    


def musk_location(connection): # TODO Duplicate/Unneeded
    sql = f'SELECT location FROM game WHERE id = \'Musk\'' # TODO Get from object not database
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

#Same comment as mentioned in row 83 but instead of location, its coordinates
def get_musk_coordinates(musk_location, connection): # TODO Duplicate/Unneeded
    musk_location = str(musk_location).strip('[(,)]')
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = {musk_location}'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]

#Determine the distance between the player and Elon Musk, this was defined as one the clues for the game
def clue_distance_to_musk(connection):
    musk = get_musk_coordinates(musk_location(connection), connection)
    player = get_player_coordinates(player_location(connection), connection)

    return print(f'Your distance to musk is {int(distance.distance(musk, player).km)} kilometers')

def musk_movement(connection):
    musk_loc = musk_location(connection)
    airport_list = calculate_all_airport_distance(get_all_airport_coordinates(connection), get_musk_coordinates(musk_loc, connection))
    in_range = airports_in_range(airport_list)

    airport_dict = dict()
    a = 1
    print(f'Number of airports in range: {len(in_range)}')
    for row in in_range:
        airport_dict.update({a: row[0]})
        a += 1
    print(f'Last airport number: {a}')
    rand = random.randint(1, a-1)

    sql = f'SELECT ident FROM airport WHERE name LIKE "{airport_dict.get(int(rand))}"'

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    result = str(result).strip('[(,)]')
    print(f'Musk has moved to {result}\n')
    musk_id = 'Musk'

    update = f'UPDATE game SET location = {result} WHERE id = \'{musk_id}\''  # TODO Update object not database
    print(update)
    cursor.execute(update)



#calculated = calculate_all_airport_distance(get_all_airport_coordinates(connection), get_player_coordinates('KIND', connection))

#player_movement(airports_in_range(calculated), connection)