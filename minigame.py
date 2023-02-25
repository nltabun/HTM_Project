import mysql.connector
import random



def minigame(connection):
    id = random.randint(1, 25) #randomizer for the random question
    correct_answer = ''

    # Fetching and printing a question from the database
    sql = (f"select * from minigame where id = {id}")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for rivi in result:
            correct_answer = rivi[6]
            print(f"{rivi[1]} \n"
                  f"(a){rivi[2]} \n"
                  f"(b){rivi[3]} \n"
                  f"(c){rivi[4]} \n"
                  f"(d){rivi[5]}")

            # Assigning the letter for correct answer
            if rivi[6] == rivi[2]:
                correct_answer = 'a'
            elif rivi[6] == rivi[3]:
                correct_answer = 'b'
            elif rivi[6] == rivi[4]:
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
        # adding prize money to be added in the near future
    else:
        print('Wrong answer, now you lose your pension.')
        # penalty to be added in the near future

#minigame()