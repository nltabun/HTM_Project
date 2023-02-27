#

class Airplane:
    def __init__(self, name, fuel_capacity=10000, fuel_efficiency=1.0, current_fuel=0):
        self.name = name
        self.fuel_capacity = fuel_capacity
        self.fuel_efficiency = fuel_efficiency # lower = better
        self.current_fuel = current_fuel # int(8)
        # TODO self.speed = ?

    def stats(self): # returns plane statistics
        return f'\'{self.name}\', {self.fuel_capacity}, {self.fuel_efficiency}, {self.current_fuel}'


class Player:
    def __init__(self, id, name, money, fuel, location, plane=Airplane('Default Plane')):
        self.id = id # varchar(40)
        self.name = name # varchar(40)
        self.money = money # int(8)
        self.fuel = fuel # int(8)
        self.location = location # varchar(10)
        self.plane = plane # varchar(40)
        self.range = 1.0 * self.plane.current_fuel * self.plane.fuel_efficiency # max single flight distance
        # TODO self.ap = ? (base ap + speed?)
    
    def __str__(self): # returns statistics for the player and their plane
        return  f'Player: {self.name}, TSLA stocks: {self.money}, Fuel: {self.fuel}, Current location: {self.location}\n' \
                f'Plane: {self.plane.name}, Current Fuel: {self.plane.current_fuel}, Fuel Capacity: {self.plane.fuel_capacity}, Fuel Efficiency: {self.plane.fuel_efficiency}'

    def sql_values(self):
        return f'\'{self.id}\', {self.fuel}, {self.money}, {self.location}, \'{self.name}\', \'{self.plane.name}\', {self.plane.current_fuel}'


#if __name__ == "__main__":
#    test_player = Player('Player', 'Player 1', 250, 1000, 'KBOS')
#    test_musk = Player('Elon Musk', 1000000, 9999999, 'KBOI', Airplane('Air Force Musk'))
#    print(test_player)
#    print('')
#    print(test_player.sql_values())
#    print(test_musk)
