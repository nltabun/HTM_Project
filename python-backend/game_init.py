#
import config
import game_objects
import random

# Check if game table already contains data
def saved_game_data_exists(connection):
    query = f'SELECT * FROM game'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    if len(result) > 0:
        exists = True
    else:
        exists = False

    return exists


# Create planes and return them in a list
def generate_airplanes(format=0):
    planes = []

    plane_musk = game_objects.Airplane('Air Force Musk', 50000, 0.9, 1000, 50000, 999999)
    plane1 = game_objects.Airplane('MickyD CD-01', 50000, 1.0, 850, 0, 150)
    plane2 = game_objects.Airplane('Boijong 420', 100000, 1.1, 900, 0, 1050)
    plane3 = game_objects.Airplane('Cloudbus A69', 88000, 0.9, 1000, 0, 1400)
    plane4 = game_objects.Airplane('Specific Statics F-61', 7000, 0.1, 2500, 0, 3000)
    plane5 = game_objects.Airplane('Sockweed F-66', 7500, 0.09, 2800, 0, 3500)

    planes.append(plane_musk)
    planes.append(plane1)
    planes.append(plane2)
    planes.append(plane3)
    planes.append(plane4)
    planes.append(plane5)

    if format == 1:
        formatted = []
        i = 0
        for plane in planes:
            if i == 0:
                i += 1
                continue

            formatted.append(plane.stats(1, i))
            i += 1

        return formatted
    else:
        return planes


# Setup players and save game data to database
def setup_game_table(connection, player_name, start_loc, planes, musk_start_loc, game_len, id_key):
    if game_len.capitalize() == 'Short' or game_len.capitalize() == 'S':
        turns = random.randint(config.short_min, config.short_max)
        start_money = config.player_money * 2
        start_fuel = config.player_fuel * 3
        start_plane = planes[config.player_plane]
    elif game_len.capitalize() == 'Long' or game_len.capitalize() == 'L':
        turns = random.randint(config.long_min, config.long_max)
        start_money = config.player_money
        start_fuel = config.player_fuel
        start_plane = planes[config.player_plane]
    else:
        print('Invalid game length value.')

    musk_money = config.musk_money
    musk_fuel = config.musk_fuel
    musk_plane = planes[config.musk_plane]
    
    player = f'{id_key}, {start_fuel}, {start_money}, \'{start_loc}\', \'{player_name}\', \'{start_plane.name}\', {start_plane.current_fuel} , {turns}'
    musk = f'{id_key+1}, {musk_fuel}, {musk_money}, \'{musk_start_loc}\', \'Elon Musk\', \'{musk_plane.name}\', {musk_plane.current_fuel}, {turns}'

    insert_values = f'INSERT INTO game(id, fuel, stonks, location, screen_name, plane, plane_fuel, turns_left) VALUES ({player}), ({musk})'

    cur = connection.cursor()
    cur.execute(insert_values)

    return


# Resets minigame completion status
def reset_minigames(connection):
    cur = connection.cursor()
    update = f'UPDATE minigame SET completed = 0'
    cur.execute(update)


# Setup new game
def new_game(connection, name, game_len, id_key):
    cur = connection.cursor()
    query_ident = f'SELECT ident FROM airport ORDER BY RAND() LIMIT 2'
    cur.execute(query_ident)
    result = cur.fetchall()
    
    player_loc = str(result[0]).strip('(\',)')
    musk_loc = str(result[1]).strip('(\',)')

    setup_game_table(connection, name, player_loc, generate_airplanes(), musk_loc, game_len, id_key)
    reset_minigames(connection)

    return

