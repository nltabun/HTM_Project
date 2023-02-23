# Game

import mysql.connector
import game_init
#import game_objects


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
    
    conn.close()


if __name__ == "__main__":
    main()
