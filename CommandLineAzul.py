# Written by Alexandra Deane
# runs with python 3.6

"""
Todo: congratulate winner, Write a display function for after scoring,
rewrite with better fundamental data structure (integers instead of strings),
make a simple way to add an AI script, think about graphics
"""

from AzulFunctions import *

# Sample_Move = {"Factory": "Factory 1", "Colour": 1, "Row": "First"}

print("Initializing GameState")
GameState = InitializeGame()

print("Commencing the gameplay loop")
while True:
    print("\nNEXT PLAYER:")
    DisplayGame(GameState)

    # Player gives move
    if GameState["Next Player"] == "Player 1":
        move = Player1_Move(GameState)
    else:
        move = Player2_Move(GameState)

    # Gamestate updated accordingly
    print("\n", move, "\n")
    UpdateGameState(GameState, move)
    print("UPDATED PLAYER BOARD:")
    DisplayGame(GameState)
    UpdatePlayer(GameState)

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
        print("Scores: ", GameState["Scoreboard"])

print("*** End of the game! ***")
print("Final Scoreboard: ", GameState["Scoreboard"])
print("Congratulations to the winner!")