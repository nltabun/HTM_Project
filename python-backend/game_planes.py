# Plane market

import game_init


def compare_planes(current_plane, selected_plane):
    compared_planes = {
        "old_plane" : {
        "name" : current_plane.name,
        "fuelCapacity" : current_plane.fuel_capacity,
        "fuelEfficiency" : current_plane.fuel_efficiency,
        "speed" : current_plane.speed
        },
        "new_plane" : {
        "name" : selected_plane.name,
        "fuelCapacity" : selected_plane.fuel_capacity,
        "fuelEfficiency" : selected_plane.fuel_efficiency,
        "speed" : selected_plane.speed
        },
        "cost" : selected_plane.cost 
    }

    return compared_planes


def buy_plane(player, selected_plane):
    try:
        if player.money >= selected_plane.cost:
            player.fuel_reserve += player.plane.current_fuel # Return fuel from old plane to reserve
            player.plane = selected_plane
            player.money -= selected_plane.cost
            player.travel_speed = selected_plane.speed
            player.current_ap -= 1

            return {"status" : 1}
        else:
            raise Exception('Not enough money.')
    except:
        return {"status" : 0}


def get_plane_data(player):
    try:
        planes = game_init.generate_airplanes(1)

        current_plane_index = 1 # Default plane
        for plane in planes:
            if plane.get("name") == player.plane.name:
                current_plane_index = plane.get("index")

        data = {
            "status" : 1,
            "currentPlaneIdx" : current_plane_index,
            "planes" : planes
        }

        return data
    except:
        return {"status" : 0}
    