#

import game_init
import game_objects


# Return a plane from list of planes using plane name as the search term. Can also set its current fuel with the optional parameter.
def load_plane(plane_name, current_fuel=0):
    planes = game_init.generate_airplanes()
    
    for p in planes:
        if p.name == plane_name:
            plane = p
            break
    
    plane.current_fuel = current_fuel
    
    return plane


# Load currently present saved game data from game table in the database and return player and Musk as "Player" objects
def load_game_table_data(connection, save_slot):
    query = f'SELECT * FROM game WHERE id = {save_slot} OR id = {save_slot+1} ORDER BY id ASC'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    print(result)

    player = result[0]
    musk = result[1]

    player_id = player[0]
    player_name = player[4]
    player_money = player[2]
    player_fuel = player[1]
    player_location = f'\'{player[3]}\''
    player_turns = player[7]
    musk_id = musk[0]
    musk_name = musk[4]
    musk_money = musk[2]
    musk_fuel = musk[1]
    musk_location = f'\'{musk[3]}\''
    musk_turns = musk[7]

    player_plane = load_plane(player[5], player[6])
    musk_plane = load_plane(musk[5], musk[6])

    player_object = game_objects.Player(player_id, player_name, player_money, player_fuel, player_location, player_turns, player_plane)
    musk_object = game_objects.Player(musk_id, musk_name, musk_money, musk_fuel, musk_location, musk_turns, musk_plane)

    return player_object, musk_object


# Save game data to the database
# Return 1 if no issues, 0 if errors
def save_to_game_table(connection, player, musk):
    try:
        player_update = f'UPDATE game SET {player.update_values()} WHERE id = {player.id}'
        musk_update = f'UPDATE game SET {musk.update_values()} WHERE id = {musk.id}'

        cur = connection.cursor()
        cur.execute(player_update)
        cur.execute(musk_update)

        return {"status" : 1}
    except Exception:
        return {"status" : 0}


# List of saved games present in the database
def saved_games(connection):
    query = f'SELECT id, screen_name FROM game WHERE id mod 2 = 1'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    print(result)

    return result


# Delete game from database
def delete_save(connection, id):
    try:
        sql = f'DELETE FROM game WHERE id = {id} OR id = {id+1}'
        cur = connection.cursor()
        cur.execute(sql)

        return {"status" : 1}
    except:
        return {"status" : 0}
