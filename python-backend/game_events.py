import random


def trigger_event(player, evt):
    if evt == 'robber':
        message = 'You were robbed.'
        player.money = player.money - 100   # you lose money
        if player.money < 0:
            player.money = 0
    elif evt == 'thief':
        message = 'Some of your fuel got stolen.'
        player.plane.current_fuel = player.plane.current_fuel - 5000  # you lose some fuel
        if player.plane.current_fuel < 0:
            player.plane.current_fuel = 0
    elif evt == 'cartel':
        message = 'You were kidnapped by the cartel and lose the rest of your turn.'
        player.end_turn()

    return {"status" : 1, "message" : message}
    

def location_event(player):
    high_risk = {'KDTW', 'KSTL', 'KORD', 'MHPR', 'MMMX', 'MMGL'}
    cartel_risk = {'MHPR', 'MMMX', 'MMGL'}

    if player.location in high_risk:
        probability = random.randint(1, 2)  # 50% chance for bad things to happen
    else:
        probability = random.randint(1, 20) # 5% chance for bad things to happen

    if probability == 1:  # unlucky man
        if player.location in cartel_risk:
            what_happens = random.randint(1, 100)
        else:
            what_happens = random.randint(1, 90)

        if what_happens <= 45:
            result = trigger_event(player, 'robber')
        elif 45 < what_happens <= 90:
            result = trigger_event(player, 'thief')
        elif 90 < what_happens:
            result = trigger_event(player, 'cartel')
        else:
            pass
            
    else:
        result = {"status" : 1, "message" : "Nothing of note happened."}

    return result


def weather_event(player, weather): # TODO
    pass
