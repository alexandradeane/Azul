# Made by Alexandra Deane
import random

# On an actual Azul Board:
# 1 = Blue
# 2 = Yellow
# 3 = Red
# 4 = Black
# 5 = Snow

BackgroundPassiveBoard = [[1, 2, 3, 4, 5],
                          [5, 1, 2, 3, 4],
                          [4, 5, 1, 2, 3],
                          [3, 4, 5, 1, 2],
                          [2, 3, 4, 5, 1]]

def InitializeGame():
    cloth_bag = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
                3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
                4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
                5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    random.shuffle(cloth_bag)
    box_lid = []
    factories = {"Factory 1": [], "Factory 2": [], "Factory 3": [],
                "Factory 4": [], "Factory 5": [], "Center": [],}
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

#Printing Stuff Functions

def PrintPassive(grid):
    print ("\nYour current Wall:")
    print (" ", end = "")
    for col in range(5):
        if (col > 0): print ("\n", end = " ")
        print ("[", end = " ")
        for row in range(5):
            if (row > 0): print (",", end = " ")
            print (grid[row][col], end = " ")
        print ("]", end = " ")
    print ("\n", end = "")

def PrintActive(board):
    print ("\nYour current pattern lines:")
    print ("First:  ", board["First"])
    print ("Second: ", board["Second"])
    print ("Third:  ", board["Third"])
    print ("Fourth: ", board["Fourth"])
    print ("Fifth:  ", board["Fifth"])
    pass

def PrintFloor(floor):
    print ("\nFloor:", floor)

def PrintFactories(factories):
    print ("\nFactories on the table:")
    print ("Factory 1: ", factories["Factory 1"])
    print ("Factory 2: ", factories["Factory 2"])
    print ("Factory 3: ", factories["Factory 3"])
    print ("Factory 4: ", factories["Factory 4"])
    print ("Factory 5: ", factories["Factory 5"])
    print ("In the center: ", factories["Center"])
    pass

def DisplayGame(game_state):
    player = game_state["Next Player"]
    print("*** ", player, "***")
    PrintFactories(game_state["Factories"])
    if player == "Player 1":
        PrintPassive(game_state["Player 1"]["Passive Board"])
        PrintActive(game_state["Player 1"]["Active Board"])
        PrintFloor(game_state["Player 1"]["Floor"])
    elif player == "Player 2":
        PrintPassive(game_state["Player 2"]["Passive Board"])
        PrintActive(game_state["Player 2"]["Active Board"])
        PrintFloor(game_state["Player 2"]["Floor"])
    else:
        print("Error: Missing a player?")

# Do Stuff to Factories

def EmptyFactories(game_state): #Do not use except for testing. Deletes tiles.
    game_state["Factories"]["Factory 1"] = []
    game_state["Factories"]["Factory 2"] = []
    game_state["Factories"]["Factory 3"] = []
    game_state["Factories"]["Factory 4"] = []
    game_state["Factories"]["Factory 5"] = []
    #for tile in game_state["Factories"]["Center"][:]:
    #    game_state["Box Lid"].append(tile)
    game_state["Factories"]["Center"] = []

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

#Player Moves

def UpdateGameState(game_state, move):
    #Extra check just to make sure it is in fact a valid move.
    if not (ValidFactory(game_state, move["Factory"]) and ValidColour(game_state, move["Colour"], move["Factory"]) and ValidRow(game_state, move["Row"], move["Colour"])):
        print ("This is not a valid move. Best not to update gamestate")
        return
    player = game_state["Next Player"]
    colour = move["Colour"]
    my_tiles = game_state["Factories"][move["Factory"]][:]
    number_of_colour = my_tiles.count(colour)
    row_name = move["Row"]
    row = RowStringtoNum(row_name)
    
    #Add as many tiles of that colour on the factory to the row
    for j in range(number_of_colour):
        if row_name == "Floor":
            game_state[player]["Floor"].append(colour)
        else:
            if len(game_state[player]["Active Board"][row_name]) < row:
                game_state[player]["Active Board"][row_name].append(colour)
            else: game_state[player]["Floor"].append(colour)
    
    #Moves the rest of the tiles on factory to the center
    if not move["Factory"] == "Center":
        game_state["Factories"][move["Factory"]] = []
        for i in range(4):
            if my_tiles[i] == colour:
                continue
            game_state["Factories"]["Center"].append(my_tiles[i])
    #(unles they are already there)
    elif move["Factory"] == "Center":
        for k in range(number_of_colour):
            game_state["Factories"]["Center"].remove(colour)
    OrderCenter(game_state)

def UpdatePlayer(game_state):
    #Now update who's turn it is
    if game_state["Next Player"] == "Player 1":
        game_state["Next Player"] = "Player 2"
    else:
        game_state["Next Player"] = "Player 1"

def NoMoreTiles(game_state):
    for factory in game_state["Factories"]:
        if game_state["Factories"][factory]:
            #print ("There's tiles in here!")
            return False
    #print("No tiles anywhere :)")
    return True

def BagIsEmpty(game_state):
    if not game_state["Cloth Bag"]:
        print ("The bag is empty!")
        return True
    return False

def Player1_Move(game_state):
    nextMove = Player2_Move(game_state)
    return nextMove

def Player2_Move(game_state):
    factory = "Default"
    colour = 0
    row = "Zeroith"
    #Get some valid user input for factory
    while True:
        try:
            factory = str(input("Please enter 'Factory #': "))
        except ValueError:
            print("You did not enter a string")
            continue
        else:
            if not ValidFactory(game_state, factory):
                continue
            break
    #Get some valid user input for colour
    while True:
        try:
            colour = int(input("Which colour do you take? "))
        except ValueError:
            print("You did not enter a number")
            continue
        else:
            if not ValidColour(game_state, colour, factory):
                continue
            break
    #Get some valid user input for row to put tile
    while True:
        try:
            row = str(input("Which row will you put it in? "))
        except ValueError:
            print("You did not enter a string")
            continue
        else:
            if not ValidRow(game_state, row, colour):
                continue
            break
    if factory == "Default" or colour == 0 or row == "Zeroith":
        print ("ERROR, the moves never changed from the default")
    nextMove = {"Factory": factory, "Colour": colour, "Row": row}
    return nextMove


def ValidFactory(game_state, factory):
    #make sure there are tiles on this factory
    if factory not in game_state["Factories"]:
        print ("That is not a factory, try again.")
        return False
    if not game_state["Factories"][factory]:
        print ("That factory is empty, try again.")
        return False
    return True

def ValidColour(game_state, colour, factory):
    #make sure that they entered a colour in the game
    if colour not in [1, 2, 3, 4, 5]:
        print ("We don't play with that colour")
        return False
    #make sure there are tiles of this colour on the factory
    for tile in game_state["Factories"][factory]:
        if tile == colour:
            return True
    print ("There is none of that colour on", factory)
    return False

def ValidRow(game_state, row, colour):
    if row == "Floor":
        return True
    #make sure that they entered a row in the game
    if row not in ["First", "Second", "Third", "Fourth", "Fifth"]:
        print ("That is not technically a row")
        return False
    #Check that row does not contain tiles of another colour
    for color in game_state[game_state["Next Player"]]["Active Board"][row]:
        if color == colour:
            continue
        print ("There are other colours in this row already")
        return False
    #Check that passive board row does not contain a tile of this colour
    for brick in game_state[game_state["Next Player"]]["Passive Board"][RowStringtoNum(row)-1]:
        if brick == colour:
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
        print ("The string you are trying to convert is not a row.")
        return 0

#Scoring

def PlaceToPutTile(colour, row, player): #returns x,y coords of where to put tile
    ro = row - 1
    col = 100
    for i in range(5):
        if BackgroundPassiveBoard[ro][i] == colour:
            col = i
    if col == 100: print("ERROR! Your backgroundpassiveboard is screwed up")
    return ro, col

def RowIsFull(game_state, row, player): #row is passed as an string
    if len(game_state[player]["Active Board"][row]) == RowStringtoNum(row):
        return True
    return False

def MoveAndScoreTile(game_state, colour, x, y, row, player): #still have to write
    #move tile to passive board
    #add points for that tile
    #as well as move the rest of tiles to box lid
    pass

def ScoreFloor(game_state, player): #still have to write
    #only count the first seven
    #as well as move tiles to box lid
    pass

def ScoreRound(game_state, player):
    for row in ["First", "Second", "Third", "Fourth", "Fifth"]:
        if RowIsFull(game_state, row, player):
            colour = game_state[player]["Active Board"][row][0]
            x, y = PlaceToPutTile(colour, RowStringtoNum(row), player)
            MoveAndScoreTile(game_state, colour, x, y, row, player)
    ScoreFloor(game_state, player)

if __name__ == "__main__":
    GameState = InitializeGame()

    player = GameState["Next Player"]
    GameState[player]["Active Board"] = {"First": [3], "Second": [3, 3], "Third": [4, 4, 4], "Fourth": [2, 2], "Fifth": [5, 5, 5, 5, 5]}
    ScoreRound(GameState, player)

    DisplayGame(GameState)
    print ("Score: ", GameState["Scoreboard"])
