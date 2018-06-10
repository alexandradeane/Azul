# Written by Alexandra Deane
# runs in python 3.6

"""
ToDo:
Getting ERROR: Scoreround saying that it is NOT a valid scoring move
congratulate winner
test a whole bunch
"""

from AzulFunctions import *

# Sample_Move = {"Factory": "Factory 1", "Colour": 1, "Row": "First"}

print("Initializing GameState")
GameState = InitializeGame()

print("Commencing the gameplay loop")
while True:
    print("\nNEXT PLAYER:")
    DisplayGame(GameState)

    # Player gives their move
    if GameState["Next Player"] == "Player 1":
        move = Player1_Move(GameState)
    else:
        move = Player2_Move(GameState)

    # Gamestate is updated accordingly
    print("\n", move, "\n")
    UpdateGameState(GameState, move)
    print("UPDATED PLAYER BOARD:")
    DisplayGame(GameState)
    UpdatePlayer(GameState)
    """
    ### Testing the scoring and endgame
    EmptyFactories(GameState)
    GameState["Player 1"]["Active Board"] = {"First": [1],
                                         "Second": [2, 2],
                                         "Third": [3, 3],
                                         "Fourth": [2, 2, 2],
                                         "Fifth": [4, 4]}
    ###
    """
    # Checks for end of round
    if NoMoreTiles(GameState):
        print("*** End of the round! ***")
        print("Scoring Player 1")
        ScoreRound(GameState, "Player 1")
        print("Scoring Player 2")
        ScoreRound(GameState, "Player 2")
        if EndConditionsMet(GameState):
            break
        if not EnoughTilesInBag(GameState):
            BoxLidToBag(GameState)
        if not EnoughTilesInBag(GameState):
            print("ERROR: Not enough tiles in your bag even after refilling")
            break
        PutTilesOnFactories(GameState)
        print(GameState["Scoreboard"])

print("Congratulations to the winner!")