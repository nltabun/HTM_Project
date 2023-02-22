

def airport_visit():
    print("Welcome to (AIRPORT NAME). Select what you want to do.\n"
          "\n"
          "(A) Play Minigame\n"
          "(B) Buy Fuel\n"
          "(C) Buy a clue from Twitter\n")

    while True:
        selection = input("Selection: ")
        choices = ('A', 'B', 'C')
        if selection in choices:
            break
        else:
            print("Error in selection. Please use letters A, B or C.")
            continue
    if selection == 'A':
        print("MINIGAME STARTS")
    elif selection == 'B':
        print("BUYING FUEL")
    else:
        print("BUY A CLUE FROM TWITTER")


airport_visit()