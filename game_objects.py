#

class Airplane:
    def __init__(self, name, fuel_capacity=10000, fuel_efficiency=1.0):
        self.name = name
        self.fuel_capacity = fuel_capacity
        self.fuel_efficiency = fuel_efficiency
        self.current_fuel = 0
        # TODO self.speed = ?


class Player:
    def __init__(self, id, name, money, fuel, location, plane=Airplane('Default Plane')):
        self.id = id
        self.name = name
        self.money = money
        self.fuel = fuel
        self.location = location
        self.plane = plane
        self.range = 1.0 * self.plane.current_fuel * self.plane.fuel_efficiency
        # TODO self.ap = ? (base ap + speed?)
    
    def __str__(self):
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
