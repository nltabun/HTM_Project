#

def buy_fuel(player, fuel_amount):
    if fuel_amount / 25 > player.money:
        return {"success" : False}
    else:
        old_player_fuel = player.fuel_reserve
        old_player_money = player.money

        player.fuel_reserve = old_player_fuel + fuel_amount
        player.money = old_player_money - fuel_amount / 25
        player.current_ap -= 1

        data = {
            "success" : True,
            "oldFuel" : old_player_fuel,
            "oldMoney" : old_player_money,
            "newFuel" : player.fuel_reserve,
            "newMoney" : player.money    
        }

        return data


def load_fuel(player, fuel_amount=''):
    if player.plane.current_fuel >= player.plane.fuel_capacity: # Fuel tank is already full.
        return {"success" : False}
    
    old_current_fuel = player.plane.current_fuel
    old_fuel_reserve = player.fuel_reserve

    if fuel_amount == '':
        empty_space = player.plane.fuel_capacity - player.plane.current_fuel

        if empty_space > player.fuel_reserve:
            player.plane.current_fuel += player.fuel_reserve
            player.fuel_reserve = 0
        else:
            player.plane.current_fuel += empty_space
            player.fuel_reserve -= empty_space
    else:
        try:
            fuel_amount = int(fuel_amount)
        except Exception: # Invalid value.
            return {"success" : False}
        
        if fuel_amount > player.fuel_reserve: # Not enough fuel.
            return {"success" : False}
        elif player.plane.current_fuel + fuel_amount > player.plane.fuel_capacity: # Can't load that much fuel.
            return {"success" : False}
        else:
            player.plane.current_fuel += fuel_amount
            player.fuel_reserve -= fuel_amount

    player.current_ap -= 1

    data = {
            "success" : True,
            "oldCurrentFuel" : old_current_fuel,
            "oldFuelReserve" : old_fuel_reserve,
            "newCurrentFuel" : player.plane.current_fuel,
            "newFuelReserve" : player.fuel_reserve    
        }
    
    return data

