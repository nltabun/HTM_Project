import random
import mysql.connector
import game_movement

conn = mysql.connector.connect(
        host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )


def minigame(connection, player):
    correct_answer = ''

    # Fetching and printing a question from the database
    sql = (f"SELECT * FROM minigame WHERE completed = 0 ORDER BY RAND() LIMIT 1")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            completed = row[7]
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
    else:
        print("You've gone through all of the questions, theres nothing left here")
        return
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

        # update the amount of stonks for player
        player.money = player.money + result_prize 

        print(f'Your stonks have reached the value of {player.money}')

    else:
        print('Wrong answer, now you lose your pension.')
        # penalty to be added in the near future

    if cursor.rowcount > 0:
        for row in result:
            update = f'UPDATE minigame SET completed = 1 WHERE id = {row[0]}'
            cursor.execute(update)

# minigame(conn, player)

################################################## Clue buying section below, be aware of eye cancer

# Function for buying clues


def buy_clue(connection, player, musk):
    while True:
        you_sure = input(f'Currently you have {player.money} stonks, one clue costs 100 stonks, do you wish to proceed? (Y/N)\n').capitalize()
        choices = ('Y', 'N')
        if you_sure in choices:
            break
        else:
            print("Error in selection. Please use letters Y or N.")

    if you_sure == 'Y':
        pass
    else:
        return

    # Check if player has enough stonks to buy a clue, the current clue price is just for testing purposes
    if player.money > 100:

        # Player has enough stonks, now we deduct the price
        player.money = player.money - 100

        # Finally give the clue to player
        game_movement.clue_distance_to_musk(connection, player, musk)
        print(f'Your stonks have been deducted to the value of {player.money}')
    else:

        # The player is too broke for us, show the door to him
        print(f'You do not have enough stonks, come back later')
# buy_clue(conn)