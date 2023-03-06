import game_movement
import math
import random


def minigame(connection, player):
    correct_answer = ''

    # Fetching and printing a question from the database
    sql = (f"SELECT * FROM minigame WHERE completed = 0 ORDER BY RAND() LIMIT 1")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            correct_answer = row[6]
            difficulty = row[8]
            print(f"{row[1]} \n"
                  f"(1) {row[2]} \n"
                  f"(2) {row[3]} \n"
                  f"(3) {row[4]} \n"
                  f"(4) {row[5]}")

            # Assigning the letter for correct answer
            if row[6] == row[2]:
                correct_answer = '1'
            elif row[6] == row[3]:
                correct_answer = '2'
            elif row[6] == row[4]:
                correct_answer = '3'
            else:
                correct_answer = '4'
    else:
        print("You've gone through all of the questions, theres nothing left here")
        input('Press "Enter" to continue')
        return
    # Waiting for the correct answer format
    while True:
        answer = input('Answer: ')
        if answer in ('1', '2', '3', '4'):
            break
        else:
            print('Answer in wrong format')

    # Checking if answer was correct
    if answer == correct_answer:
        print("Correct, here's your money.")
        # Getting the value of the questions prize
        sql = f'SELECT value FROM prize WHERE id IN(SELECT difficulty FROM minigame WHERE difficulty = {difficulty})'
        cursor = connection.cursor()
        cursor.execute(sql)
        result_prize = cursor.fetchone()
        result_prize = int(str(result_prize).strip('(,)'))

        # update the amount of stonks for player
        if player.location == "'PHNL'":
            player.money = player.money + (result_prize * 3)  #triple the amount of money if in hawaii
        else:
            player.money = player.money + result_prize

        print(f'You now have {player.money} stocks')
        input('Press "Enter" to continue')
    else:
        print(f'Wrong answer')

        input('Press "Enter" to continue')

    player.current_ap -= 1
    player.done_minigame = 1

    if cursor.rowcount > 0:
        for row in result:
            update = f'UPDATE minigame SET completed = 1 WHERE id = {row[0]}'
            cursor.execute(update)


# Function for buying clues
def buy_clue(connection, player, musk):
    while True:
        you_sure = input(f'Currently you have {player.money} stonks, one clue costs 100 stonks, do you wish to proceed? (Y/N)\n').capitalize()
        choices = ('Y', 'N')
        if you_sure in choices:
            break
        else:
            print('Error in selection. Please use letters "Y" or "N".')

    if you_sure == 'Y':
        pass
    else:
        return

    # Check if player has enough stonks to buy a clue, the current clue price is just for testing purposes
    if player.money > 100:

        # Player has enough stonks, now we deduct the price
        player.money = player.money - 100

        # Finally give the clue to player
        random_clue = random.randint(1, 3)  # Randomize which clue we return

        # Gives the distance and bearing of musk compared to the player
        if random_clue == 1:
            print(f'{game_movement.clue_distance_to_musk(connection, player, musk)} to {get_bearing(game_movement.get_player_coordinates(connection, player.location), game_movement.get_player_coordinates(connection, musk.location))}')

        elif random_clue == 2:

            # Selects the zone where musk is located at
            sql = f'SELECT ident, zone FROM airport WHERE ident = {musk.location}'
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()

            if cursor.rowcount > 0:
                for row in result:
                    zone = row[1]
                    if zone == 1:
                        print("Musk is located in the east coast")

                    elif zone == 2:
                        print("Musk is located in the central US")

                    elif zone == 3:
                        print("Musk is located in the west coast")

                    elif zone == 4:
                        print("Outside of the United States Of America")

                    else:
                        print("Musk has escaped the matrix")

        elif random_clue == 3:
            airports = set()
            two_airports = game_movement.random_airports(connection)

            airports.update(two_airports)
            airports.update(game_movement.select_airport(connection, musk))

            print(f'Elon Musk is currently located in one of the following airports:')
            for i in airports:
                print(str(i).strip("('',)"))

        player.current_ap -= 1
        player.bought_clue = 1

        print(f'Your stonks have been deducted to the value of {player.money}')
        input('Press "Enter" to continue')
    else:
        # The player is too broke for us, show the door to him
        print(f'You do not have enough stocks, come back later')
        input('Press "Enter" to continue')


def get_bearing(player_coords, comp_coords):  # function found in https://www.programcreek.com/python/example/93521/geopy.Point
    """
    Calculates the bearing between two points.

    Parameters
    ----------
    player_coords: geopy.Point
    comp_coords: geopy.Point

    Returns
    -------
    point: int
        Bearing in degrees between the start and end points. <--- not anymore clown
    """

    direction = ''

    start_lat = math.radians(player_coords[0])
    start_lng = math.radians(player_coords[1])
    end_lat = math.radians(comp_coords[0])
    end_lng = math.radians(comp_coords[1])

    d_lng = end_lng - start_lng
    if abs(d_lng) > math.pi:
        if d_lng > 0.0:
            d_lng = -(2.0 * math.pi - d_lng)
        else:
            d_lng = (2.0 * math.pi + d_lng)

    tan_start = math.tan(start_lat / 2.0 + math.pi / 4.0)
    tan_end = math.tan(end_lat / 2.0 + math.pi / 4.0)
    d_phi = math.log(tan_end / tan_start)
    bearing = (math.degrees(math.atan2(d_lng, d_phi)) + 360.0) % 360.0

    if 0 < bearing < 22.5 or 337.5 < bearing < 360:
        direction = 'North'
    elif 22.5 < bearing < 67.5:
        direction = 'North East'
    elif 67.5 < bearing < 112.5:
        direction = 'East'
    elif 112.5 < bearing < 157.5:
        direction = 'South East'
    elif 157.5 < bearing < 202.5:
        direction = 'South'
    elif 202.5 < bearing < 247.5:
        direction = 'South West'
    elif 247.5 < bearing < 292.5:
        direction = 'West'
    elif 292.5 < bearing < 337.5:
        direction = 'North West'

    return direction
