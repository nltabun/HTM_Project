# Game

import mysql.connector
import game_fuel
import game_init
import game_movement
import game_actions
import game_data
# import game_objects

# Start game
def play_game(connection):
    # A little variable to keep the game going for testing purposes
    game_on = True

    player, musk = game_data.load_game_table_data(connection) # Loads player and Musk as "Player" objects from the game table

    print(f'{player}') # Test print loaded player
    print(f'{musk}\n') # Test print loaded musk

    # A loop made for testing purposes
    while game_on == True:
        game_actions.airport_visit(connection, player)

    print(f'{player}')


def main_menu(connection): # TODO
    pass


def main():
    # Establish connection to database using predetermined login details
    conn = mysql.connector.connect(
        host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )
    
    # Check if save data can be found. (= is there something in the game table)
    save_data = game_init.saved_game_data_exists(conn)

    if save_data:
        print('\nSave data found.\n')
    else:
        print('\nNo save data found.\n')
    
    # Test "main menu" # TODO func main menu
    option = 1
    if option == 1: # New game
        game_init.new_game(conn)
        play_game(conn)
    elif option == 2: # Continue game (TODO Hide if no save to load maybe?)
        if save_data: 
            play_game(conn)
        else: # No save
            pass
    elif option == 4: # Quit game
        pass
    
    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()
