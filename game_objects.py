#

class Airplane:

    def __init__(self, name, fuel_capacity=10000, fuel_efficiency=1.0, speed=850, current_fuel=0, cost=0):
        self.name = name # varchar(40)
        self.fuel_capacity = fuel_capacity
        self.fuel_efficiency = fuel_efficiency # lower = better
        self.current_fuel = current_fuel # int(8)
        self.speed = speed
        self.cost = cost

    def stats(self): # returns plane statistics
        return f'\'{self.name}\' | {self.fuel_capacity} | {self.fuel_efficiency} | {self.speed}'

    def range(self): # returns max single flight distance for the plane
        return 1.0 * (self.current_fuel / self.fuel_efficiency) / 12

class Player:
    def __init__(self, id, name, money, fuel, location, turns_left, plane=Airplane('Default Plane')):
        self.id = id # varchar(40)
        self.name = name # varchar(40)
        self.money = money # int(8)
        self.fuel_reserve = fuel # int(8)
        self.location = location # varchar(10)
        self.turns_left = turns_left # int(4)
        self.plane = plane # plane.name: varchar(40)
        self.travel_speed = plane.speed # ap per km
        self.max_ap = 5
        self.current_ap = self.max_ap
        self.done_minigame = 0
        self.bought_clue = 0
        self.enemy_location = ''
    
    def epitaph(self, player_loc):
        self.enemy_location = player_loc

    def range(self): # returns max single flight distance for the player
        travel_range = self.current_ap * self.travel_speed
        if self.plane.range() < travel_range: # if fuel and fuel efficiency is the limiting factor
            return self.plane.range()
        else: # if ap and speed are the limiting factor
            return travel_range
        
    def decrease_turns(self):
        self.turns_left = self.turns_left - 1
        
    def end_turn(self):
        self.current_ap = 0
        return

    def fuel_consumption(self, distance):
        self.plane.current_fuel = int(self.plane.current_fuel - (self.plane.fuel_efficiency * 12 * distance))


        
    def __str__(self): # returns statistics for the player and their plane
        return  f'Player: {self.name} | TSLA stocks: {self.money} | Fuel Reserve: {self.fuel_reserve} | Current location: {self.location} | Current AP: {self.current_ap}\n' \
                f'Plane: {self.plane.name} | Current Fuel: {self.plane.current_fuel} | Fuel Capacity: {self.plane.fuel_capacity} | Fuel Efficiency: {self.plane.fuel_efficiency}'

    def new_values(self): # returns player statistics in the correct format for inserting a new player into the database 
        return f'\'{self.id}\', {self.fuel_reserve}, {self.money}, {self.location}, \'{self.name}\', \'{self.plane.name}\', {self.plane.current_fuel}, {self.turns_left}'
    
    def update_values(self): # returns player statistics in the correct format to update a player in the database
        return f'fuel = {self.fuel_reserve}, stonks = {self.money}, location = {self.location}, plane = \'{self.plane.name}\', plane_fuel = {self.plane.current_fuel}, turns_left = {self.turns_left}'
    
    def fuel_status(self):
        return f'Plane fuel tank: {self.plane.current_fuel}/{self.plane.fuel_capacity}\nFuel reserve: {self.fuel_reserve}'

