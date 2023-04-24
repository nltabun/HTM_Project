#

def buy_fuel(player, fuel_amount):
    if fuel_amount / 25 > player.money:
        return 'Cannot afford that amount of fuel.'
    else:
        new_player_money = player.money - fuel_amount / 25
        new_player_fuel = player.fuel_reserve + fuel_amount

        player.fuel_reserve = new_player_fuel
        player.money = new_player_money
        player.current_ap -= 1

        return f'You now have {new_player_money} TSLA stock and {new_player_fuel} liters of fuel.'


def load_fuel(player, fuel_amount):
    if player.plane.current_fuel >= player.plane.fuel_capacity:
        print('Fuel tank is already full.')
        return 'Fuel tank is already full.'
    
    old_current_fuel = player.plane.current_fuel
    old_fuel_reserve = player.fuel_reserve

    try:
        fuel_amount = int(fuel_amount)
    except Exception:
        print('Invalid value.')
        return 'Invalid value.'
    
    if fuel_amount > player.fuel_reserve:
        print('Not enough fuel.')
        return 'Not enough fuel.'
    elif player.plane.current_fuel + fuel_amount > player.plane.fuel_capacity:
        print('Can\'t load that much fuel.')
        return 'Can\'t load that much fuel.'
    else:
        player.plane.current_fuel += fuel_amount
        player.fuel_reserve -= fuel_amount

    if fuel_amount == '':
        empty_space = player.plane.fuel_capacity - player.plane.current_fuel

        if empty_space > player.fuel_reserve:
            player.plane.current_fuel += player.fuel_reserve
            player.fuel_reserve = 0
        else:
            player.plane.current_fuel += empty_space
            player.fuel_reserve -= empty_space
    
    player.current_ap -= 1
    
    return f'Plane fuel tank: {old_current_fuel} -> {player.plane.current_fuel}\nPlayer fuel reserve: {old_fuel_reserve} -> {player.fuel_reserve}\n'


def fuel_management(player):
    options = ('1','2','4')
    if player.name != 'Elon Musk':
        while True:
            print('Fuel Management\n\nDo you want to..\n(1) Buy fuel\n(2) Load fuel\n(4) Cancel')
            option = input('> ')

            if option in options:
                break
            else:
                print(f'Incorrect input.\n')

        if option == '1':
            buy_fuel(player)
        elif option == '2':
            while True:
                loading_fuel = load_fuel(player)
                if loading_fuel == False:
                    break
        elif option == '4':
            return
    else:
        load_fuel(player)
