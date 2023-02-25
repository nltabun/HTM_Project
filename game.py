# Game

import mysql.connector
import game_init
import game_movement
import minigame
#import game_objects

def airport_visit(connection):
    print(f"Welcome to {str(game_movement.player_location_name(connection)).strip('[(,)]')}. Select what you want to do.\n"
          "\n"
          "(A) Play Minigame\n"
          "(B) Buy Fuel\n"
          "(C) Buy a clue\n"
          "(D) Select another airport\n")

    while True:
        selection = input("Selection: ").capitalize()
        choices = ('A', 'B', 'C', 'D')
        if selection in choices:
            break
        else:
            print("Error in selection. Please use letters A, B, C or D.")
            continue
    if selection == 'A':
        minigame.minigame(connection)
    elif selection == 'B':
        print("BUYING FUEL")
    elif selection == 'C':
        print("BUY A CLUE")
    elif selection == 'D':
        game_movement.player_movement(connection)

def play_game(connection):
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
        # TODO Start game
    elif option == 2: # Continue game (TODO Hide if no save to load maybe?)
        if save_data: 
            pass # TODO Start game
        else: # No save
            pass
    elif option == 4: # Quit game
        pass

    play_game(conn)
    conn.close()


if __name__ == "__main__":
    main()

