# Gets players money
def player_money(connection):
    sql = (f"SELECT stonks FROM game WHERE id = \'player\'")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return int(str(result).strip('[(,)]'))

# Gets players fuel
def player_fuel(connection):
    sql = (f"SELECT fuel FROM game WHERE id = \'player\'")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return int(str(result).strip('[(,)]'))

#
def buying_fuel(connection):
    cursor = connection.cursor()
    money = player_money(connection)

    print(f'BUYING FUEL\n'
          f'\nYou have {player_money(connection)} TSLA Stock')

    fuel = int(input('Do you want to by fuel? 1 TSLA Stock = 1Km of range. Enter the amount you want to buy: '))
    if fuel > money:
        print(f'\nYou cannot afford that amount of fuel.\n')
    else:

        new_player_money = money - fuel
        new_player_fuel = player_fuel(connection) + fuel

        update = f'UPDATE game SET stonks = {new_player_money} WHERE id = \'player\''
        cursor.execute(update)
        update = f'UPDATE game SET fuel = {new_player_fuel} WHERE id = \'player\''
        cursor.execute(update)

        print(f'\nYou now have {new_player_money} TSLA stock and {new_player_fuel}km of range\n')

