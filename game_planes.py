# Plane market

import game_init


def compare_planes(current_plane, selected_plane):
    print(f'____|-------------- Old Plane\n'
          f'Name -------------- {current_plane.name}\n'
          f'Fuel Capacity ----- {current_plane.fuel_capacity}\n'
          f'Fuel Efficiency --- {current_plane.fuel_efficiency}\n'
          f'Speed ------------- {current_plane.speed}\n'
          f'-------------------------------\n'
          f'____|-------------- New Plane\n'
          f'Name -------------- {selected_plane.name}\n'
          f'Fuel Capacity ----- {selected_plane.fuel_capacity}\n'
          f'Fuel Efficiency --- {selected_plane.fuel_efficiency}\n'
          f'Speed ------------- {selected_plane.speed}\n')



def plane_market(player):
    planes = game_init.generate_airplanes()

    while True:
        print(f'\nPLANE MARKET\n\nYour current plane is:\n{player.plane.stats()}\nFollowing planes are currently available:')
        i = 0
        for plane in planes:
            if i == 0:
                i += 1
                continue
            print(f'({i}) {plane.stats()} | Cost: {plane.cost} Stocks')
            i += 1
        print(f'\nYou currently have {player.money} Stocks.\n')

        choice = input('Enter the number of the plane you wish buy. (Type "C" to Cancel)\n> ')
        if choice.capitalize() == 'C':
            return
        else:
            if player.money >= planes[int(choice)].cost:
                compare_planes(player.plane, planes[int(choice)])
                confirm = input('Are you sure you want to buy this plane? ("Y" to confirm)\n> ')
                if confirm.capitalize() == 'Y':
                    player.fuel_reserve += player.plane.current_fuel # Return fuel from old plane to reserve
                    player.plane = planes[int(choice)]
                    player.money -= planes[int(choice)].cost
                    player.current_ap -= 1
                    break
            else:
                print('\nYou can\'t afford this plane\n')
    