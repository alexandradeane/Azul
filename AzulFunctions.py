# Written by Alexandra Deane
# runs in Python 3.6

import random

BackgroundPassiveBoard = [[1, 2, 3, 4, 5],
                          [5, 1, 2, 3, 4],
                          [4, 5, 1, 2, 3],
                          [3, 4, 5, 1, 2],
                          [2, 3, 4, 5, 1]]

def InitializeGame():
    cloth_bag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    random.shuffle(cloth_bag)
    box_lid = []
    factories = {"Factory 1": [], "Factory 2": [], "Factory 3": [],
                 "Factory 4": [], "Factory 5": [], "Center": [], }
    active_player_board1 = {"First": [], "Second": [], "Third": [],
                            "Fourth": [], "Fifth": []}
    active_player_board2 = {"First": [], "Second": [], "Third": [],
                            "Fourth": [], "Fifth": []}
    passive_player_board1 = [[0 for col in range(5)] for row in range(5)]
    passive_player_board2 = [[0 for col in range(5)] for row in range(5)]
    first_player_generator = random.randrange(2) + 1
    first_player = "Player " + str(first_player_generator)
    player1_floor = []
    player2_floor = []
    scoreboard = {"Player 1": 0, "Player 2": 0}

    game_state = {"Player 1": {"Active Board": active_player_board1,
                               "Passive Board": passive_player_board1,
                               "Floor": player1_floor},
                  "Player 2": {"Active Board": active_player_board2,
                               "Passive Board": passive_player_board2,
                               "Floor": player2_floor},
                  "Cloth Bag": cloth_bag, "Box Lid": box_lid,
                  "Factories": factories, "Scoreboard": scoreboard,
                  "Next Player": first_player}

    PutTilesOnFactories(game_state)
    OrderFactories(game_state)
    return game_state

### Printing Stuff Functions ###

def PrintPassive(grid):
    print(" ", end="")
    for col in range(5):
        if col > 0: print("\n", end=" ")
        print("[", end=" ")
        for row in range(5):
            if (row > 0): print(",", end=" ")
            print(grid[col][row], end=" ")
        print("]", end=" ")
    print("\n", end="")

def PrintActive(board):
    print("First:  ", board["First"])
    print("Second: ", board["Second"])
    print("Third:  ", board["Third"])
    print("Fourth: ", board["Fourth"])
    print("Fifth:  ", board["Fifth"])
    pass

def PrintFloor(floor):
    print("\nFloor:", floor, "\n")

def PrintFactories(factories):
    print("Factory 1: ", factories["Factory 1"])
    print("Factory 2: ", factories["Factory 2"])
    print("Factory 3: ", factories["Factory 3"])
    print("Factory 4: ", factories["Factory 4"])
    print("Factory 5: ", factories["Factory 5"])
    print("In the center: ", factories["Center"])
    pass

def DisplayGame(game_state):
    player = game_state["Next Player"]
    print("******** ", player, "********")
    print("\nFactories on the table:")
    PrintFactories(game_state["Factories"])
    print("\nYour current Wall:")
    PrintPassive(game_state[player]["Passive Board"])
    print("\nYour current pattern lines:")
    PrintActive(game_state[player]["Active Board"])
    PrintFloor(game_state[player]["Floor"])
    print("**************************")
### Do Stuff to Factories ###

def EmptyFactories(game_state):  # Do not use except for testing. Deletes tiles.
    game_state["Factories"]["Factory 1"] = []
    game_state["Factories"]["Factory 2"] = []
    game_state["Factories"]["Factory 3"] = []
    game_state["Factories"]["Factory 4"] = []
    game_state["Factories"]["Factory 5"] = []
    # for tile in game_state["Factories"]["Center"][:]:
    #    game_state["Box Lid"].append(tile)
    game_state["Factories"]["Center"] = []

def EnoughTilesInBag(game_state):
    tiles = len(game_state["Cloth Bag"])
    #print("Number of tiles left in cloth bag: ", tiles)
    if tiles >= 20:
        return True
    return False

def BoxLidToBag(game_state):
    for tile in game_state["Box Lid"][:]:
        game_state["Cloth Bag"].append(tile)
    game_state["Box Lid"] = []
    random.shuffle(game_state["Cloth Bag"])

def PutTilesOnFactories(game_state):
    for i in range(4):
        tile = game_state["Cloth Bag"].pop()
        game_state["Factories"]["Factory 1"].append(tile)
        tile = game_state["Cloth Bag"].pop()
        game_state["Factories"]["Factory 2"].append(tile)
        tile = game_state["Cloth Bag"].pop()
        game_state["Factories"]["Factory 3"].append(tile)
        tile = game_state["Cloth Bag"].pop()
        game_state["Factories"]["Factory 4"].append(tile)
        tile = game_state["Cloth Bag"].pop()
        game_state["Factories"]["Factory 5"].append(tile)

def OrderFactories(game_state):
    for factory in game_state["Factories"]:
        factory_copy = game_state["Factories"][factory][:]
        sorted_factory = list()
        for tile_type in [1, 2, 3, 4, 5]:
            for num in range(factory_copy.count(tile_type)):
                sorted_factory.append(tile_type)
        game_state["Factories"][factory] = sorted_factory

def OrderCenter(game_state):
    center_copy = game_state["Factories"]["Center"][:]
    sorted_center = list()
    for tile_type in [1, 2, 3, 4, 5]:
        for num in range(center_copy.count(tile_type)):
            sorted_center.append(tile_type)
    game_state["Factories"]["Center"] = sorted_center

### Player Moves ###

def UpdateGameState(game_state, move):
    # Extra check just to make sure it is in fact a valid move.
    if not (ValidFactory(game_state, move["Factory"])
            and ValidColour(game_state, move["Colour"], move["Factory"])
            and ValidRow(game_state, move["Row"], move["Colour"])):
        print("This is not a valid move. Best not to update gamestate")
        return
    player = game_state["Next Player"]
    colour = move["Colour"]
    my_tiles = game_state["Factories"][move["Factory"]][:]
    number_of_colour = my_tiles.count(colour)
    row_name = move["Row"]
    row = RowStringtoNum(row_name)
    # Add as many tiles of that colour on the factory to the row
    for j in range(number_of_colour):
        if row_name == "Floor":
            game_state[player]["Floor"].append(colour)
        else:
            if len(game_state[player]["Active Board"][row_name]) < row:
                game_state[player]["Active Board"][row_name].append(colour)
            else:
                game_state[player]["Floor"].append(colour)
    # Moves the rest of the tiles on factory to the center
    if not move["Factory"] == "Center":
        game_state["Factories"][move["Factory"]] = []
        for i in range(4):
            if my_tiles[i] == colour:
                continue
            game_state["Factories"]["Center"].append(my_tiles[i])
    # (unles they are already there)
    elif move["Factory"] == "Center":
        for k in range(number_of_colour):
            game_state["Factories"]["Center"].remove(colour)
    OrderCenter(game_state)

def UpdatePlayer(game_state):
    # Now update who's turn it is
    if game_state["Next Player"] == "Player 1":
        game_state["Next Player"] = "Player 2"
    else:
        game_state["Next Player"] = "Player 1"

def NoMoreTiles(game_state):
    for factory in game_state["Factories"]:
        if game_state["Factories"][factory]:
            # print ("There's tiles in here!")
            return False
    # print("No tiles anywhere :)")
    return True

def BagIsEmpty(game_state):
    if not game_state["Cloth Bag"]:
        print("The bag is empty!")
        return True
    return False

def Player1_Move(game_state):
    factory = "Default"
    colour = 0
    row = "Zeroith"
    # Get some valid user input for which factory to take from
    while True:
        try:
            factory_num = input("Please enter Factory # (or 'c' for center): ")
            if factory_num == 'c' or factory_num == 'C'\
                or factory_num == 'center' or factory_num == 'Center'\
                or factory_num == 'CENTER' or factory_num == 'centre'\
                or factory_num == 'Centre' or factory_num == 'CENTRE':
                    factory = 'Center'
            else:
                factory_num = int(factory_num)
                factory = "Factory " + str(factory_num)
        except ValueError:
            print("You did not enter an integer value, please try again")
        else:
            #print("FACTORY: ", factory)
            if not ValidFactory(game_state, factory):
                continue
            break
    # Get some valid user input for row to put tile
    while True:
        try:
            colour = int(input("Which colour do you take? "))
        except ValueError:
            print("You did not enter an integer value, please try again")
            continue
        else:
            if not ValidColour(game_state, colour, factory):
                continue
            break
    # Get some valid user input for row to put tile
    while True:
        row_str = input("Which row will you put it in? ")
        if row_str in ["First", "Second", "Third", "Fourth", "Fifth"]:
            break
        row_str = int(row_str)
        if row_str == 1:
            row = "First"
        if row_str == 2:
            row = "Second"
        if row_str == 3:
            row = "Third"
        if row_str == 4:
            row = "Fourth"
        if row_str == 5:
            row = "Fifth"
        if not ValidRow(game_state, row, colour):
            continue
        break

    if factory == "Default" or colour == 0 or row == "Zeroith":
        print("ERROR PLAYER 1 MOVE, the moves never changed from the default")
    move = {"Factory": factory, "Colour": colour, "Row": row}
    return move

def Player2_Move(game_state):
    nextMove = Player1_Move(game_state)
    return nextMove

def ValidFactory(game_state, factory):
    # make sure there are tiles on this factory
    if factory not in game_state["Factories"]:
        print("That is not a factory, try again.")
        return False
    if not game_state["Factories"][factory]:
        print("That factory is empty, try again.")
        return False
    return True

def ValidColour(game_state, colour, factory):
    # make sure that they entered a colour in the game
    if colour not in [1, 2, 3, 4, 5]:
        print("We don't play with that colour")
        return False
    # make sure there are tiles of this colour on the factory
    for tile in game_state["Factories"][factory]:
        if tile == colour:
            return True
    print("There is none of that colour on", factory)
    return False

def ValidRow(game_state, row, colour): #Row passed as a string
    if row == "Floor":
        return True
    # make sure that they entered a row in the game
    if row not in ["First", "Second", "Third", "Fourth", "Fifth"]:
        print("That is not technically a row")
        return False
    # Check that row does not contain tiles of another colour
    for color in game_state[game_state["Next Player"]]["Active Board"][row]:
        #print("colour: ", colour)
        if color == colour:
            continue
        print("There are other colours in this row already")
        return False
    # Check that passive board row does not contain a tile of this colour
    for brick in game_state[game_state["Next Player"]]["Passive Board"][RowStringtoNum(row) - 1]:
        if brick == colour:
            print("That colour is already on your wall")
            return False
    return True

def RowStringtoNum(string):
    if string == "First":
        return 1
    if string == "Second":
        return 2
    if string == "Third":
        return 3
    if string == "Fourth":
        return 4
    if string == "Fifth":
        return 5
    if string == "Floor":
        return True
    else:
        print("The string you are trying to convert is not a row.")
        return 0

### Scoring ###

def PlaceToPutTile(colour, row, player):  # returns x,y coords (indexed from 0)
    ro = row - 1
    col = 100
    for i in range(5):
        if BackgroundPassiveBoard[ro][i] == colour:
            col = i
    if col == 100: print("ERROR! Your backgroundpassiveboard is screwed up")
    return ro, col

def RowIsFull(game_state, row, player):  # row is passed as an string
    if len(game_state[player]["Active Board"][row]) == RowStringtoNum(row):
        return True
    return False

def OccupiedWallCord(game_state, player, x, y):
    if x < 0 or y < 0 or x > 4 or y > 4:
        return False
    if game_state[player]["Passive Board"][x][y]:
        return True
    return False

def MoveAndScoreTile(game_state, colour, x, y, row, player):
    # move tile to passive board
    game_state[player]["Passive Board"][x][y] = colour

    # add points for that tile
    x_points = 1
    # add one point for every tile to the right
    y_right = y + 1
    # print ("X_right, y: ", x, y_right)
    while OccupiedWallCord(game_state, player, x, y_right):
        x_points = x_points + 1
        y_right = y_right + 1
    #print("x_points counting right = ", x_points)
    # add one point for every tile to the left
    y_left = y - 1
    while OccupiedWallCord(game_state, player, x, y_left):
        x_points = x_points + 1
        y_left = y_left - 1
    #print("x_points counting left = ", x_points)
    y_points = 1
    # add one point for every tile above
    x_up = x - 1
    while OccupiedWallCord(game_state, player, x_up, y):
        y_points = y_points + 1
        x_up = x_up - 1
    #print("y_points counting up = ", y_points)
    # add one point for every tile below
    x_down = x + 1
    while OccupiedWallCord(game_state, player, x_down, y):
        y_points = y_points + 1
        x_down = x_down + 1
    #print("y_points counting down = ", y_points)
    #print("X-points: ", x_points)
    #print("Y-points: ", y_points)

    # Make sure not to count the original tile twice if there is only a row or only a column
    total_points = x_points + y_points
    if x_points == 1:
        total_points = total_points - 1
    if y_points == 1:
        total_points = total_points - 1
    if x_points == 1 and y_points == 1:
        total_points = total_points + 1
    #print("Total points gained: ", total_points)
    # Add the total points to the player's score
    game_state["Scoreboard"][player] = game_state["Scoreboard"][player] + total_points

    # as well as move the rest of tiles to box lid
    tiles_to_scrap = RowStringtoNum(row) - 1
    #print("Tiles to scrap: ", tiles_to_scrap)
    for tile in range(tiles_to_scrap):
        game_state["Box Lid"].append(colour)
    # now empty the rest of the row that was full
    game_state[player]["Active Board"][row] = []

def ScoreFloor(game_state, player):
    # only count the first seven
    penalties = len(game_state[player]["Floor"])
    if penalties >= 1:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 1
    if penalties >= 2:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 1
    if penalties >= 3:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 2
    if penalties >= 4:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 2
    if penalties >= 5:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 2
    if penalties >= 6:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 3
    if penalties >= 7:
        game_state["Scoreboard"][player] = game_state["Scoreboard"][player] - 3
    # Move them to the box lid
    for tile in game_state[player]["Floor"][:]:
        game_state["Box Lid"].append(tile)
    # And erase them from the floor
    game_state[player]["Floor"] = []
    # make sure score isn't negative
    if game_state["Scoreboard"][player] < 0:
        game_state["Scoreboard"][player] = 0

def ScoreRound(game_state, player):
    for row in ["First", "Second", "Third", "Fourth", "Fifth"]:
        if RowIsFull(game_state, row, player):
            print("Scoring", row, "row", end=" --- ")
            colour = game_state[player]["Active Board"][row][0]
            print("colour: ", colour)
            x, y = PlaceToPutTile(colour, RowStringtoNum(row), player)
            #print("X: ", x , "Y: ", y)
            MoveAndScoreTile(game_state, colour, x, y, row, player)
    ScoreFloor(game_state, player)

def EndConditionsMet(game_state):
    for player in ["Player 1", "Player 2"]:
        for row in game_state[player]["Passive Board"]:
            if row[0] and row[1] and row[2] and row[3] and row[4]:
                #print ("Row ", row, " is all filled up")
                print ("IT IS FINALLY THE END OF THE GAME!")
                return True
    #print("No end game here")
    return False

if __name__ == "__main__":
    ### This is an entire setup to facilitate scoring tests ###



    GameState = InitializeGame()
    player = GameState["Next Player"]
    EmptyFactories(GameState)
    GameState[player]["Passive Board"] = [[0, 2, 3, 0, 5],
                                          [5, 0, 0, 0, 0],
                                          [0, 5, 1, 0, 3],
                                          [0, 0, 5, 1, 2],
                                          [2, 3, 4, 5, 1]]
    GameState[player]["Active Board"] = {"First": [],
                                         "Second": [1, 1],
                                         "Third": [4, 4],
                                         "Fourth": [2, 2],
                                         "Fifth": [5, 5, 5, 5]}
    GameState[player]["Floor"] = [3, 3, 1, 4, 5, 5, 3, 5, 2]
    GameState["Scoreboard"]["Player 1"] = 100

    assert ValidRow(GameState, "Second", 1) == True

    print("#################### BEFORE SCORING #########################")
    DisplayGame(GameState)
    print("Cloth Bag: ", GameState["Cloth Bag"])
    print("Box Lid: ", GameState["Box Lid"])
    print("#############################################################")
    ScoreRound(GameState, player)
    print("#################### AFTER SCORING ##########################")
    
    DisplayGame(GameState)
    GameState["Cloth Bag"] = [4, 7]
    GameState["Box Lid"] = [8, 8, 8, 8, 8, 9]

    print("Cloth Bag: ", GameState["Cloth Bag"])
    print("Box Lid: ", GameState["Box Lid"])

    print(EnoughTilesInBag(GameState))
    if not EnoughTilesInBag(GameState):
        BoxLidToBag(GameState)
    #PutTilesOnFactories()
    print("##### Score: ", GameState["Scoreboard"])
    
    DisplayGame(GameState)
    print("Cloth Bag: ", GameState["Cloth Bag"])
    print("Box Lid: ", GameState["Box Lid"])

    EndConditionsMet(GameState)

    #print("##### Score: ", GameState["Scoreboard"])

    #print(OccupiedWallCord(GameState, player, 2, 0))


    #lilGameState = {"Box Lid": [5, 8], "Cloth Bag": [2]}
    #print("lilGameState before: ", lilGameState)
    #BoxLidToBag(lilGameState)
    #print("lilGameState after: ", lilGameState)



