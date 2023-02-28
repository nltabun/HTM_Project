# Gets players money
def player_money(connection):
    sql = (f"SELECT stonks FROM game WHERE id = \'player\'")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return int(str(result).strip('[(,)]'))

# Gets players fuel
def player_fuel(connection, player):
    player_current_fuel = player.fuel

    #sql = (f"SELECT fuel FROM game WHERE id = \'player\'")
    #cursor = connection.cursor()
    #cursor.execute(sql)
    #result = cursor.fetchall()
    #return int(str(result).strip('[(,)]'))
    return player_current_fuel

#
def buying_fuel(connection, player):
    cursor = connection.cursor()
    player_money = player.money

    print(f'BUYING FUEL\n'
          f'\nYou have {player_money} TSLA Stock')

    fuel = int(input('Do you want to by fuel? 1 TSLA Stock = 1Km of range. Enter the amount you want to buy: '))
    if fuel > player_money:
        print(f'\nYou cannot afford that amount of fuel.\n')
    else:

        new_player_money = player_money - fuel
        new_player_fuel = player.fuel + fuel

        player.fuel = new_player_fuel
        player.money = new_player_money

        update = f'UPDATE game SET stonks = {new_player_money} WHERE id = \'player\''
        cursor.execute(update)
        update = f'UPDATE game SET fuel = {new_player_fuel} WHERE id = \'player\''
        cursor.execute(update)

        print(f'\nYou now have {new_player_money} TSLA stock and {new_player_fuel}km of range\n')

