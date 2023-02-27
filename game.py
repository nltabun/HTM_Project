# Game

import mysql.connector

import game_fuel
import game_init
import game_movement
import game_choice_options
import game_data
#import game_objects

#A little variable to keep the game going for testing purposes
game_on = True
def airport_visit(connection):
    print(f"Welcome to {str(game_movement.player_location_name(connection)).strip('[(,)]')}. Select what you want to do.\n"
          "\n"
          "(A) Play Minigame\n"
          "(B) Buy Fuel\n"
          "(C) Buy a clue\n"
          "(D) Select another airport\n")

    while True:
        selection = input("Selection: ").capitalize()
        choices = ('A', 'B', 'C', 'D', 'F11')
        if selection in choices:
            break
        else:
            print("Error in selection. Please use letters A, B, C or D.")
            continue
    if selection == 'A':
        game_choice_options.minigame(connection)
    elif selection == 'B':
        game_fuel.buying_fuel(connection)
    elif selection == 'C':
        game_choice_options.buy_clue(connection)
    elif selection == 'D':
        game_movement.player_movement(connection)
    #A way to end the while loop/program
    elif selection == 'F11':
        global game_on
        game_on = False


def play_game(connection):
    players = game_data.load_player_data(connection)

    #A loop made for testing purposes
    while game_on == True:
        airport_visit(connection)

def main():
    conn = mysql.connector.connect(
        host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )
    
    save_data = game_init.saved_game_data_exists(conn)

    if save_data:
        print('True')
    else:
        print('False')
    
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

    conn.close()


if __name__ == "__main__":
    main()

