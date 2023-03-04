#

def buy_fuel(player):
    print(f'BUYING FUEL\n'
          f'\nYou have {player.money} TSLA Stock')

    fuel = int(input('How much fuel do you want to buy? 1 TSLA Stock = 1Km of range. Enter the amount you want to buy: '))
    if fuel > player.money:
        print(f'\nYou cannot afford that amount of fuel.\n')
    else:
        new_player_money = player.money - fuel
        new_player_fuel = player.fuel_reserve + fuel

        player.fuel_reserve = new_player_fuel
        player.money = new_player_money

        print(f'\nYou now have {new_player_money} TSLA stock and {new_player_fuel}km of range\n')


def load_fuel(player):
    active = True
    if player.id == 'Player':
        print(f'\nLoad Fuel\n{player.fuel_status()}\n')
        if player.plane.current_fuel >= player.plane.fuel_capacity:
            print('Fuel tank is already full. Returning...')
            active = False
            return active
        else:
            fuel_amount = ''    
            fuel_amount = input('How much fuel do you want to load? (Type "C" to cancel) (Default: max)\n> ')

        if fuel_amount.capitalize() == 'C':
            active = False
            return active
    elif player.id == 'Musk':
        fuel_amount = ''
    else:
        print('Invalid player id. Cannot execute "load fuel".')
        active = False
        return active
    
    old_current_fuel = player.plane.current_fuel
    old_fuel_reserve = player.fuel_reserve 
    
    if fuel_amount != '':
        try:
            fuel_amount = int(fuel_amount)
        except Exception:
            print('\nInvalid value.\n')
            active = True
            return active
        
        print(fuel_amount, player.fuel_reserve)
        print(type(fuel_amount), type(player.fuel_reserve))
        if fuel_amount > player.fuel_reserve:
            do_max = input('You don\'t have that much fuel. Load as much as you can? ("Y" to confirm)\n> ')
        
            if do_max.capitalize() == 'Y':
                fuel_amount = ''
            else:
                active = True
                return active
        elif player.plane.current_fuel + fuel_amount > player.plane.fuel_capacity:
            do_max = input('Can\'t load that much fuel. Load as much as you can? ("Y" to confirm)\n> ')
            
            if do_max.capitalize() == 'Y':
                fuel_amount = ''
            else:
                active = True
                return active
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
    
    if player.id == 'Player':
        print(f'Plane fuel tank: {old_current_fuel} -> {player.plane.current_fuel}\n'
            f'Player fuel reserve: {old_fuel_reserve} -> {player.fuel_reserve}\n')
        input('Press "Enter" to continue')
    
    active = False
    return active


def fuel_management(player):
    options = ('1','2','4')
    if player.id == 'Player':
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
    
    if player.id == 'Musk':
        load_fuel(player)
