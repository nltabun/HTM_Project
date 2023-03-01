#

import game_objects


# Check if game table already contains data
def saved_game_data_exists(connection):
    query = f'SELECT * FROM game'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    if len(result) > 0:
        #print(result)
        exists = True
    else:
        exists = False

    return exists


# Create planes and return them in a list
def generate_airplanes():
    planes = []
    
    plane_musk = game_objects.Airplane('Air Force Musk', 50000, 0.9, 1000)
    plane1 = game_objects.Airplane('Cloudbus A69', 10000, 1.0, 850)
    plane2 = game_objects.Airplane('Boijong 420', 24000, 1.1, 900)
    
    planes.append(plane_musk)
    planes.append(plane1)
    planes.append(plane2)

    return planes


# Setup players when no data exists in 'game' table
def setup_game_table(connection, player_name, start_loc, planes, musk_start_loc):
    start_money = 250
    start_fuel = 1000
    start_plane = planes[1]
    musk_plane = planes[0]

    player = game_objects.Player('Player', player_name, start_money, start_fuel, start_loc, start_plane)
    musk = game_objects.Player('Musk', 'Elon Musk', 1000000, 9999999, musk_start_loc, musk_plane)

    insert_values = f'INSERT INTO game VALUES ({player.new_values()}), ({musk.new_values()})'
    cur = connection.cursor()
    cur.execute(insert_values)

    return


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
    print(player_loc, '|', musk_loc)

    player_name = input('Name: ')
    setup_game_table(connection, player_name, player_loc, generate_airplanes(), musk_loc)
    
    return
