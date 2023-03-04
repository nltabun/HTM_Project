# Game

import mysql.connector
import game_fuel
import game_init
import game_movement
import game_actions
import game_data
import game_events


def airport_visit(connection, musk=None, player=None):
    global game_on

    if player.current_ap <= 0:
        return

    print(f'\nCurrent {player}\n')

    location_name = str(game_movement.player_location_name(connection, player)).strip("[('',)]")
    print(f'Welcome to {location_name}. Select what you want to do.\n'
          '\n'
          '(1) Play Minigame\n'
          '(2) Fuel management\n'
          '(3) Buy a clue\n'
          '(4) Fly to another location\n')

    while True:
        selection = input('Selection: ').capitalize()
        choices = ('1', '2', '3', '4', 'F11', 'C')
        if selection in choices:
            break
        else:
            print('Error in selection. Please use numbers 1, 2, 3 or 4.')
            continue

    if selection == '1':
        game_actions.minigame(connection, player)
    elif selection == '2':
        game_fuel.fuel_management(player)
    elif selection == '3':
        game_actions.buy_clue(connection, player, musk)
    elif selection == '4':
        game_movement.player_movement(connection, player)
        game_events.event(player)
                
        # Disabled for testing loop
        '''if musk.turns_left != 0:
            print('\nElon Musk is moving.\n')
            game_movement.player_movement(connection, musk)
            game_movement.decrease_turns(musk)
        else:
            print("Elon Musk found his Tesla and escaped, you lost the game...")
            game_on = False'''

    # Return to main menu
    elif selection == 'F11' or 'C':
        print('Returning to main menu.')
        game_on = False
    
# Start game
def play_game(connection):
    # Loads player and Musk as "Player" objects from the game table
    player, musk = game_data.load_game_table_data(connection)

    global game_on

    # Game loop
    while game_on:
        # Win condition
        if player.location == musk.location:
            print("Congratulations! You found Elon Musk!")
            game_on = False
        # Both player and Musk are out of AP. Turn ends and a new one starts.
        elif player.current_ap <= 0 and musk.current_ap <= 0:
            player.current_ap = player.max_ap
            musk.current_ap = musk.max_ap
            airport_visit(connection, musk, player)
        # Player takes their turn first, so it's their turn until they are out of AP.
        elif player.current_ap > 0:
            airport_visit(connection, musk, player)
        # Otherwise Musk takes his turn.
        else:
            airport_visit(connection, player=musk)

    # Save game data back to the database
    game_data.save_to_game_table(connection, player, musk)


def main_menu(connection):
    global game_on

    while True:
        # Check if save data exists
        save_data = game_init.saved_game_data_exists(connection)
        # Valid options
        options = {'1', '4'}
        # Add continue game option if save data exists
        if save_data:
            options.add('2')

        # Print options and the player which one they choose
        print('\n(1) NEW GAME')
        if '2' in options:
            print('(2) CONTINUE GAME')
        print('(4) QUIT GAME')
        option = input('\n> ')

        # Verify the option exists
        if option in options:
            if option == '1': # New game
                print('\nStarting new game\n')
                # Create new game
                game_init.new_game(connection) 
                # Make sure the game is on
                game_on = True 
                # Start game
                play_game(connection)
            elif option == '2': # Continue game
                print('\nContinuing Game\n')
                # Make sure the game is on
                game_on = True
                # Start game
                play_game(connection)                
            elif option == '4': # Quit game
                print('\nQuitting Game\n')
                break
        # Go back and ask again if the option doesn't exist
        else:
            print('\nOption doen\'t exist.\n')
            continue  


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
    
    # A little variable to keep the game going for testing purposes
    global game_on
    game_on = True

    # Start main menu
    main_menu(conn)
    
    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()
