import random


def event1(player):

    probability = random.randint(1, 2)  # Decide your fate with a 50 / 50 chance

    if probability == 1:  # unlucky man
        what_happens = random.randint(1, 2)  # decide your "punishment" with your bad luck

        if what_happens == 1:
            message = 'You were robbed'
            player.money = player.money - 100   # you lose money
            if player.money < 0:
                player.money = 0
        else:
            message = 'Some of your fuel got stolen'
            player.plane.current_fuel = player.plane.current_fuel - 5000  # you lose some fuel
            if player.plane.current_fuel < 0:
                player.plane.current_fuel = 0
    else:
        message = None

    return message


def event2(player):

    probability = random.randint(1, 2)  # Decide your fate with a 50 / 50 chance

    if probability == 1:
        what_happens = random.randint(1, 100)

        if what_happens < 10:
            message = 'You were kidnapped by the cartel, you lose 1 whole round'
            player.end_turn()

        elif 10 < what_happens < 55:
            message = 'You were robbed'
            player.money = player.money - 100  # you lose money
            if player.money < 0:
                player.money = 0

        else:
            message = 'Some of your fuel got stolen'
            player.plane.current_fuel = player.plane.current_fuel - 5000  # you lose some fuel

            if player.plane.current_fuel < 0:
                player.plane.current_fuel = 0

    else:
        message = None

    return message
