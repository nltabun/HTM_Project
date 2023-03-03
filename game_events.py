import random


def event(player):

    if player.location == "'KDTW'" or player.location == "'KSTL'" or player.location == "'KORD'":  # Detroit, St.Louis, Chicago
        probability = random.randint(1, 2)  # Decide your fate with a 50 / 50 chance

        if probability == 1:  # unlucky man
            what_happens = random.randint(1, 2)  # decide your "punishment" with your bad luck

            if what_happens == 1:
                print('You were robbed')
                player.money = player.money - 100   # you lose money
                if player.money < 0:
                    player.money = 0
            else:
                print('Some of your fuel got stolen')
                player.plane.current_fuel = player.plane.current_fuel - 100  # you lose some fuel
                if player.fuel < 0:
                    player.plane.current_fuel = 0

    elif player.location == "'MHPR'" or player.location == "'MMMX'" or player.location == "'MMGL'":  # Honduras, 2 mexican cities
        probability = random.randint(1, 2)  # Decide your fate with a 50 / 50 chance

        if probability == 1:
            what_happens = random.randint(1, 100)

            if what_happens < 10:
                print('You were kidnapped by the cartel, you lose 1 whole round')  # rip 1 round

            elif 10 < what_happens < 55:
                print('You were robbed')
                player.money = player.money - 100  # you lose money
                if player.money < 0:
                    player.money = 0

            else:
                print('Some of your fuel got stolen')
                player.fuel = player.fuel - 100  # you lose some fuel

                if player.fuel < 0:
                    player.plane.current_fuel = 0

