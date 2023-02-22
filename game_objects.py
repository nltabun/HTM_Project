#

class Airplane:
    def __init__(self, name, fuel_capacity=10000, fuel_efficiency=1.0):
        self.name = name
        self.fuel_capacity = fuel_capacity
        self.fuel_efficiency = fuel_efficiency
        # ? current_fuel ?


class Player:
    def __init__(self, id, name, money, fuel, location, plane=Airplane('Default Plane')):
        self.id = id
        self.name = name
        self.money = money
        self.fuel = fuel
        self.location = location
        self.plane = plane # Currently not stored between sessions. TODO Add to database?
        # ? Max range = 1.0km * fuel (<= plane.fuel_capacity) * plane.fuel_efficiency ?
    
    def __str__(self):
        return  f'Player: {self.name}, TSLA stocks: {self.money}, Fuel: {self.fuel}, Current location: {self.location}\n' \
                f'Plane: {self.plane.name}, Fuel Capacity: {self.plane.fuel_capacity}, Fuel Efficiency: {self.plane.fuel_efficiency}'

    def sql_values(self):
        return f'\'{self.id}\', {self.fuel}, {self.money}, {self.location}, \'{self.name}\''


#if __name__ == "__main__":
#    test_player = Player('Player 1', 250, 1000, 'KBOS')
#    test_musk = Player('Elon Musk', 1000000, 9999999, 'KBOI', Airplane('Air Force Musk'))
#    print(test_player.sql_values())
#    print(test_musk)
