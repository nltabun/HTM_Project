# Game

import mysql.connector
import game_fuel
import game_init
import game_movement
import game_actions
import game_data
import game_events
import game_planes


def airport_visit(connection, musk=None, player=None):
    global game_on

    if player.current_ap <= 0:
        return

    if player.name != 'Elon Musk':
        print(f'\nCurrent {player}\n')

        location_name = str(game_movement.player_location_name(connection, player)).strip("[('',)]")
        print(f'Welcome to {location_name}. Select what you want to do.\n'
            '\n'
            '(1) Play Minigame\n'
            '(2) Fuel management\n'
            '(3) Buy a clue\n'
            '(4) Fly to another location\n'
            '(5) Plane Market\n'
            '(6) End turn\n'
            '(C) Quit to main menu\n')

        while True:
            selection = input('Selection: ').capitalize()
            choices = ('1', '2', '3', '4', '5', '6', 'F11', 'C')
            if selection in choices:
                break
            else:
                print('\nError in selection. Please use numbers 1, 2, 3, 4, 5, 6 or letter "C" to return to main menu')
                continue

        if selection == '1':
            if player.done_minigame == 1:
                print("\nYou've already played a minigame, try again next round")
                input('\nPress "Enter" to continue')
            else:
                mgame = game_actions.minigame(connection, player)
                if mgame == -1:
                    game_init.reset_minigames()
        elif selection == '2':
            game_fuel.fuel_management(player)
        elif selection == '3':
            if player.bought_clue == 1:
                print("\nYou've already bought 1 clue, try again next round")
                input('\nPress "Enter" to continue')
            else:
                game_actions.buy_clue(connection, player, musk)
        elif selection == '4':
            game_movement.player_movement(connection, player)
            game_events.event(player)
        elif selection == '5':
            game_planes.plane_market(player)
        elif selection == '6':
            player.end_turn()
        # Return to main menu
        elif selection == 'F11' or 'C':
            print('\nReturning to main menu.\n')
            game_on = False
    
    elif player.name == 'Elon Musk':
        if player.plane.current_fuel < 25000:
            print('\nMusk is managing fuel.')
            game_fuel.fuel_management(player)
        else:
            print('\nMusk is moving.')
            game_movement.player_movement(connection, player)

            if player.current_ap == player.max_ap:
                print('\nMusk is apparently having troubles.')
                game_fuel.fuel_management(player)
            print('\nMusk is going to sleep.')
            player.end_turn()

    else:
        print('\nInvalid Player ID\n')      

     
# Start game
def play_game(connection, save_slot):
    # Loads player and Musk as "Player" objects from the game table
    player, musk = game_data.load_game_table_data(connection, save_slot)

    global game_on

    # Game loop
    while game_on:
        # Player win condition
        if player.location == musk.location:
            print('\nCongratulations! You found Elon Musk!\n')
            game_on = False
            input('Press "Enter" to return to the main menu\n')
            game_data.save_to_game_table(connection, player, musk)
            return
        # Musk win condition
        elif musk.turns_left <= 0:
            print('\nElon Musk found his Tesla and escaped, you lost the game...\n')
            game_on = False
            input('Press "Enter" to return to the main menu\n')
            game_data.save_to_game_table(connection, player, musk)
            return

        # Both player and Musk are out of AP, which means both have fully taken their turns.
        if player.current_ap <= 0 and musk.current_ap <= 0:
            # Save game data back to the database after both players have taken their turns.
            game_data.save_to_game_table(connection, player, musk)
            player.current_ap = player.max_ap
            musk.current_ap = musk.max_ap
            player.bought_clue = 0
            player.done_minigame = 0
            airport_visit(connection, musk, player)
        # Player takes their turn first, so it's their turn until they are out of AP.
        elif player.current_ap > 0:
            airport_visit(connection, musk, player)
            if player.current_ap <= 0:
                player.decrease_turns()
                print('\nYour turn has ended.\n')
                musk.epitaph(player.location)
                input('Press "Enter" to continue\n')
        # Otherwise Musk takes his turn.
        else:
            if musk.current_ap == musk.max_ap:
                print('Musk will make his moves now.\n')
            
            airport_visit(connection, player=musk)
            if musk.current_ap <= 0:
                musk.decrease_turns()

    
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
                #
                saves = game_data.saved_games(connection)
                # Make sure the game is on
                game_on = True
                # Start game
                # print(saves[len(saves)-1]) # Correct
                play_game(connection, saves[len(saves)-1])
            elif option == '2': # Continue game
                print('\nSaved Games\n')
                saves = game_data.saved_games(connection)

                i = 1
                for save in saves:
                    print(f'({i}) {save[1]}')
                    i += 1
                while True:
                    choice = input('Select the save you want to load. (Use numbers) ("C" to cancel)')
                    if choice.capitalize() == 'C':
                        print('f')
                        break
                    elif 0 < int(choice) < len(saves):
                        print('elif')
                        saved_game = saves[int(choice)-1]
                        # Make sure the game is on
                        game_on = True
                        # Start game
                        play_game(connection, saved_game)
                        break
                    else:
                        print('Invalid input. Try again')
                          
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
    
    # A little variable to keep the game going
    global game_on
    game_on = True

    # Start main menu
    main_menu(conn)
    
    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()
