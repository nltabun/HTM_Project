#
#import mysql.connector
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
def load_game_table_data(connection):
    query = f'SELECT * FROM game ORDER BY id DESC'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    player = result[0]
    musk = result[1]

    player_plane = load_plane(player[5], player[6])
    musk_plane = load_plane(musk[5], musk[6])

    player_object = game_objects.Player(player[0], player[4], player[2], player[1], player[3], player_plane)
    musk_object = game_objects.Player(musk[0], musk[4], musk[2], musk[1], musk[3], musk_plane)

    return player_object, musk_object


# Save game data to the database
def save_to_game_table(connection, player, musk):
    player_update = f'UPDATE game SET {player.update_values()} WHERE id = \'{player.id}\''
    musk_update = f'UPDATE game SET {musk.update_values()} WHERE id = \'{musk.id}\''

    cur = connection.cursor()
    cur.execute(player_update)
    cur.execute(musk_update)

# Testing
#if __name__ == "__main__":
#    conn = mysql.connector.connect(
#        host='localhost',
#        database='htm_database',
#        user='htm',
#        password='play',
#        autocommit=True
#    )
#
#    player, musk = load_game_table_data(conn)
#    print(player)
#    print(musk)
#    player.fuel = player.fuel + 1500
#    if player.location == 'KLIT':
#        player.location = 'KBOS'
#    else:
#        player.location = 'KLIT'
#    musk.money = musk.money - 10000
#    musk.fuel = musk.fuel - 1000
#    player.plane = load_plane('Boijong 420', 7900)    
#    print(player)
#    print(musk)
#    save_to_game_table(conn, player, musk)
