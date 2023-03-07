#

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
def generate_airplanes():
    planes = []

    plane_musk = game_objects.Airplane('Air Force Musk', 50000, 0.9, 1000, 50000, 999999)
    plane1 = game_objects.Airplane('MickyD CD-01', 48000, 1.0, 850, 0, 150)
    plane2 = game_objects.Airplane('Boijong 420', 100000, 1.1, 900, 0, 1050)
    plane3 = game_objects.Airplane('Cloudbus A69', 88000, 0.9, 1000, 0, 1400)
    plane4 = game_objects.Airplane('Specific Statics F-61 "Tussling Caracara"', 7000, 0.1, 2500, 0, 3000)
    plane5 = game_objects.Airplane('Sockweed F-66 "Rapture"', 7500, 0.09, 2800, 0, 3500)
    
    planes.append(plane_musk)
    planes.append(plane1)
    planes.append(plane2)
    planes.append(plane3)
    planes.append(plane4)
    planes.append(plane5)

    return planes


# Setup players when no data exists in 'game' table
def setup_game_table(connection, player_name, start_loc, planes, musk_start_loc):
    start_money = 250
    start_fuel = 20000
    start_plane = planes[1]
    musk_plane = planes[0]

    while True:
        game_len = input('Short or long game? (S/L): ')
        if game_len.capitalize() == 'Short' or game_len.capitalize() == 'S':
            turns = random.randint(10, 15)
            break
        elif game_len.capitalize() == 'Long' or game_len.capitalize() == 'L':
            turns = random.randint(30, 40)
            break
        else:
            print('Invalid value')

    player = game_objects.Player('Player', player_name, start_money, start_fuel, start_loc, turns, start_plane)
    musk = game_objects.Player('Musk', 'Elon Musk', 1000000, 9999999, musk_start_loc, turns, musk_plane)

    insert_values = f'INSERT INTO game VALUES ({player.new_values()}), ({musk.new_values()})'
    cur = connection.cursor()
    cur.execute(insert_values)

    return


# Resets minigame completion status
def reset_minigames(connection):
    cur = connection.cursor()
    update = f'UPDATE minigame SET completed = 0'
    cur.execute(update)


# Setup new game (currently also deletes old game)
def new_game(connection):
    cur = connection.cursor()
    if saved_game_data_exists(connection):
        delete_save = f'DELETE FROM game'
        cur.execute(delete_save)

    query_ident = f'SELECT ident FROM airport ORDER BY RAND() LIMIT 2'
    cur.execute(query_ident)
    result = cur.fetchall()
    
    player_loc = str(result[0]).strip('(,)')
    musk_loc = str(result[1]).strip('(,)')

    player_name = input('\nName: ')
    setup_game_table(connection, player_name, player_loc, generate_airplanes(), musk_loc)
    reset_minigames(connection)

    return

