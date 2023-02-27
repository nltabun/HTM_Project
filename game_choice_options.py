import random
import mysql.connector
import game_movement
from geopy import distance

conn = mysql.connector.connect(
       host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )
def minigame(connection):
    id = random.randint(1, 25) #randomizer for the random question
    correct_answer = ''

    # Fetching and printing a question from the database
    sql = (f"select * from minigame where id = {id}")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            correct_answer = row[6]
            difficulty = row[8]
            print(f"{row[1]} \n"
                  f"(A){row[2]} \n"
                  f"(B){row[3]} \n"
                  f"(C){row[4]} \n"
                  f"(D){row[5]}")

            # Assigning the letter for correct answer
            if row[6] == row[2]:
                correct_answer = 'a'
            elif row[6] == row[3]:
                correct_answer = 'b'
            elif row[6] == row[4]:
                correct_answer = 'c'
            else:
                correct_answer = 'd'

    # Waiting for the correct answer format
    while True:
        answer = input()
        if answer in ('a', 'b', 'c', 'd'):
            break
        else:
            print('Answer in wrong format')

    # Checking if answer was correct
    if answer == correct_answer:
        print("Correct, here's your money, now get out.")
        # Getting the value of the questions prize
        sql = f'SELECT value FROM prize WHERE id IN(SELECT difficulty FROM minigame WHERE difficulty = {difficulty})'
        cursor = connection.cursor()
        cursor.execute(sql)
        result_prize = cursor.fetchone()
        result_prize = int(str(result_prize).strip('(,)'))

        #Get players current amount of stonks
        sql = f'SELECT stonks  FROM game WHERE id = \'player\''
        cursor = connection.cursor()
        cursor.execute(sql)
        player_stonks = cursor.fetchall()
        player_stonks = int(str(player_stonks).strip('[(,)]'))

        #update the amount of stonks for player
        stonks = player_stonks + result_prize

        update = f'UPDATE game SET stonks = {stonks} WHERE id = \'player\''
        cursor.execute(update)

        print(f'Your stonks have reached the value of {stonks}')

    else:
        print('Wrong answer, now you lose your pension.')
        # penalty to be added in the near future

#minigame(conn)

################################################## Clue buying section below, be aware of eye cancer

#Get Elons location as it had not been done in game_movement(as in, the function was only made for players)
def musk_location(connection):
    sql = f'SELECT location FROM game WHERE id = \'Musk\''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

#Same comment as mentioned in row 83 but instead of location, its coordinates
def get_musk_coordinates(musk_location, connection):
    musk_location = str(musk_location).strip('[(,)]')
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = {musk_location}'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]

#Determine the distance between the player and Elon Musk, this was defined as one the clues for the game
def clue_distance_to_musk(connection):
    musk = get_musk_coordinates(musk_location(connection), connection)
    player = game_movement.get_player_coordinates(game_movement.player_location(connection), connection)

    return print(f'Your distance to musk is {int(distance.distance(musk, player).km)} kilometers')

#Function for buying clues
def buy_clue(connection):
    #Save players stonks to a variable
    sql = f'SELECT stonks  FROM game WHERE id = \'player\''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    result = int(str(result[0]).strip('[(,)]'))

    while True:
        you_sure = input(
            f'Currently you have {result} stonks, one clue costs 100 stonks, do you wish to proceed? (Y/N)\n').capitalize()
        choices = ('Y', 'N')
        if you_sure in choices:
            break
        else:
            print("Error in selection. Please use letters Y or N.")

    if you_sure == 'Y':
        pass
    else:
        return

    #Check if player has enough stonks to buy a clue, the current clue price is just for testing purposes
    if result > 100:

        #Player has enough stonks, now we deduct the price and update the new stonk total to database
        stonks = result - 100
        update = f'UPDATE game SET stonks = {stonks} WHERE id = \'player\''
        cursor.execute(update)

        #Finally give the clue to player
        clue_distance_to_musk(connection)
        print(f'Your stonks have been deducted to the value of {stonks}')
    else:

        #The player is too broke for us, show the door to him
        print(f'You do not have enough stonks, come back later')

#buy_clue(conn)