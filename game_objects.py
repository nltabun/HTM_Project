#

class Airplane:
    def __init__(self, name, fuel_capacity=10000, fuel_efficiency=1.0, speed=850, current_fuel=0):
        self.name = name # varchar(40)
        self.fuel_capacity = fuel_capacity
        self.fuel_efficiency = fuel_efficiency # lower = better
        self.current_fuel = current_fuel # int(8)
        self.speed = speed

    def stats(self): # returns plane statistics
        return f'\'{self.name}\', {self.fuel_capacity}, {self.fuel_efficiency}, {self.current_fuel}'

    def range(self): # returns max single flight distance for the plane
        return 1.0 * self.current_fuel * self.fuel_efficiency 

class Player:
    def __init__(self, id, name, money, fuel, location, turn_limit, plane=Airplane('Default Plane')):
        self.id = id # varchar(40)
        self.name = name # varchar(40)
        self.money = money # int(8)
        self.fuel = fuel # int(8)
        self.location = location # varchar(10)
        self.turns_left = turn_limit # int(4)
        self.plane = plane # plane.name: varchar(40)
        self.travel_speed = plane.speed # ap per km
        self.max_ap = 5
        self.current_ap = self.max_ap

    def range(self): # returns max single flight distance for the players current plane
        return self.plane.range()
    
    def __str__(self): # returns statistics for the player and their plane
        return  f'Player: {self.name}, TSLA stocks: {self.money}, Fuel: {self.fuel}, Current location: {self.location}\n' \
                f'Plane: {self.plane.name}, Current Fuel: {self.plane.current_fuel}, Fuel Capacity: {self.plane.fuel_capacity}, Fuel Efficiency: {self.plane.fuel_efficiency}'

    def new_values(self): # returns player statistics in the correct format for inserting a new player into the database 
        return f'\'{self.id}\', {self.fuel}, {self.money}, {self.location}, \'{self.name}\', \'{self.plane.name}\', {self.plane.current_fuel}, {self.turns_left}'
    
    def update_values(self): # returns player statistics in the correct format to update a player in the database
        return f'fuel = {self.fuel}, stonks = {self.money}, location = {self.location}, plane = \'{self.plane.name}\', plane_fuel = {self.plane.current_fuel}, turns_left = {self.turns_left}'

