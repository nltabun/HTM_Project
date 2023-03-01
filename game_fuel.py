#

def buying_fuel(player):
    print(f'BUYING FUEL\n'
          f'\nYou have {player.money} TSLA Stock')

    fuel = int(input('How much fuel do you want to buy? 1 TSLA Stock = 1Km of range. Enter the amount you want to buy: '))
    if fuel > player.money:
        print(f'\nYou cannot afford that amount of fuel.\n')
    else:
        new_player_money = player.money - fuel
        new_player_fuel = player.fuel + fuel

        player.fuel = new_player_fuel
        player.money = new_player_money

        print(f'\nYou now have {new_player_money} TSLA stock and {new_player_fuel}km of range\n')
