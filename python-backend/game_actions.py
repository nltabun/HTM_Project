import game_movement
import math
import random


def play_minigame(connection):
    # Fetch a question from the database that hasn't been completed yet
    sql = f'SELECT * FROM minigame WHERE completed = 0 ORDER BY RAND() LIMIT 1'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if cursor.rowcount > 0: # If a question was found
        status = 0
    else: # If everything has been completed then get one anyways.
        status = -1
        sql = f'SELECT * FROM minigame ORDER BY RAND() LIMIT 1'
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
    
    # Question data formatted
    data = {
        "id": result[0],
        "question": result[1],
        "answers": [result[2], result[3], result[4], result[5]]
    }
   
    return data, status


def answer_minigame(connection, player, qid, answer):
    if player.done_minigame == 1:
        return {"status" : -1}


    sql = f'SELECT correct_answer, difficulty FROM minigame WHERE id = {qid}'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()


    # Checking if answer was correct
    if answer == result[0]:
        # Getting the value of the questions prize
        sql = f'SELECT value FROM prize WHERE id IN(SELECT difficulty FROM minigame WHERE difficulty = {result[1]})'
        cursor = connection.cursor()
        cursor.execute(sql)
        result_prize = cursor.fetchone()
        result_prize = int(result_prize[0])

        # Update the players money
        if player.location == 'PHNL':
            player.money = player.money + (result_prize * 3)  #triple the amount of money if in hawaii
        else:
            player.money = player.money + result_prize

        # Set minigame status to completed
        update = f'UPDATE minigame SET completed = 1 WHERE id = {qid}'
        cursor.execute(update)
        
        data = {
            "status" : 1,
            "prize" : result_prize
        }
    else:
        data = {
            "status" : 0,
        }

    # Reduce ap by 1 and disable minigames for this turn
    player.current_ap -= 1
    player.done_minigame = 1
            
    return data


# Function for buying clues
def buy_clue(connection, player, musk):
        # Player has enough stonks, now we deduct the price
        player.money = player.money - 100

        # Randomize which clue we return
        random_clue = random.randint(1, 3)  

        # Gives the bearing of musk compared to the player
        if random_clue == 1:
            player_coord = game_movement.get_player_coordinates(connection, player.location)
            musk_coord = game_movement.get_player_coordinates(connection, musk.location)
            data = {
                "status" : 1,
                "clueType" : 1,
                "clue" : get_bearing(player_coord, musk_coord)
            }
        # "Zone" in which Musk currently resides
        elif random_clue == 2:
            # Selects the zone where Musk is located at
            sql = f'SELECT ident, zone FROM airport WHERE ident = \'{musk.location}\''
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()

            if cursor.rowcount > 0:
                data = {
                    "status" : 1,
                    "clueType" : 2,
                }
                for row in result:
                    zone = row[1]
                    if zone == 1: # Musk is located in the east coast
                        data.update({"clue" : "EC"})
                    elif zone == 2: # Musk is located in the central US
                        data.update({"clue" : "CU"})
                    elif zone == 3: # Musk is located in the west coast
                        data.update({"clue" : "WC"})
                    elif zone == 4: # Outside of the United States of America
                        data.update({"clue" : "OA"})
            else:
                data = {
                    "status" : 0
                }
        # Three potential Musk locations 
        elif random_clue == 3:
            airports = game_movement.random_airports(connection)
            airports.append((game_movement.select_airport(connection, musk.location)[0][0], musk.location))
            print(airports)

            random.shuffle(airports)
            data = {
                "status" : 1,
                "clueType" : 3,
                "clue" : airports
            }

        # Reduce player ap and check "bought clue" for this turn
        player.current_ap -= 1
        player.bought_clue = 1
        print(data)
        return data



def get_bearing(player_coords, comp_coords):  # function found in https://www.programcreek.com/python/example/93521/geopy.Point
    """
    Calculates the bearing between two points.

    Parameters
    ----------
    player_coords: geopy.Point
    comp_coords: geopy.Point

    Returns
    -------
    point: int
        Bearing in degrees between the start and end points. <--- not anymore clown
    """

    direction = ''

    start_lat = math.radians(player_coords[0])
    start_lng = math.radians(player_coords[1])
    end_lat = math.radians(comp_coords[0])
    end_lng = math.radians(comp_coords[1])

    d_lng = end_lng - start_lng
    if abs(d_lng) > math.pi:
        if d_lng > 0.0:
            d_lng = -(2.0 * math.pi - d_lng)
        else:
            d_lng = (2.0 * math.pi + d_lng)

    tan_start = math.tan(start_lat / 2.0 + math.pi / 4.0)
    tan_end = math.tan(end_lat / 2.0 + math.pi / 4.0)
    d_phi = math.log(tan_end / tan_start)
    bearing = (math.degrees(math.atan2(d_lng, d_phi)) + 360.0) % 360.0

    if 0 < bearing < 22.5 or 337.5 < bearing < 360:
        direction = 'North'
    elif 22.5 < bearing < 67.5:
        direction = 'North East'
    elif 67.5 < bearing < 112.5:
        direction = 'East'
    elif 112.5 < bearing < 157.5:
        direction = 'South East'
    elif 157.5 < bearing < 202.5:
        direction = 'South'
    elif 202.5 < bearing < 247.5:
        direction = 'South West'
    elif 247.5 < bearing < 292.5:
        direction = 'West'
    elif 292.5 < bearing < 337.5:
        direction = 'North West'

    return direction
