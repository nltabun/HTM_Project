# Game

import mysql.connector
import game_fuel
import game_init
import game_movement
import game_actions
import game_data
# import game_objects

# A little variable to keep the game going for testing purposes
game_on = True


def airport_visit(connection, musk, player=None):
    location_name = str(game_movement.player_location_name(connection, player)).strip("[('',)]")
    print(f'Welcome to {location_name}. Select what you want to do.\n'
          '\n'
          '(A) Play Minigame\n'
          '(B) Buy Fuel\n'
          '(C) Buy a clue\n'
          '(D) Select another airport\n')

    while True:
        selection = input('Selection: ').capitalize()
        choices = ('A', 'B', 'C', 'D', 'F11')
        if selection in choices:
            break
        else:
            print('Error in selection. Please use letters A, B, C or D.')
            continue

    if selection == 'A':
        game_actions.minigame(connection, player)
    elif selection == 'B':
        game_fuel.buying_fuel(player)
    elif selection == 'C':
        game_actions.buy_clue(connection, player, musk)
    elif selection == 'D':
        game_movement.player_movement(connection, player)
        print(player.location)
        print('\nElon Musk is moving.\n')
        game_movement.musk_movement(connection)
        # game_movement.player_movement(connection)

    # A way to end the while loop/program
    elif selection == 'F11':
        global game_on
        game_on = False


# Start game
def play_game(connection):
    player, musk = game_data.load_game_table_data(connection) # Loads player and Musk as "Player" objects from the game table

    print(f'{player}') # Test print loaded player
    print(f'{musk}\n') # Test print loaded musk

    # A loop made for testing purposes
    while game_on == True:
        airport_visit(connection, musk, player)
        print(f'{player}')
        print(f'{musk}')

    game_data.save_to_game_table(connection, player, musk)


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
