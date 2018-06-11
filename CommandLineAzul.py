"""
Written by Alexandra Deane
runs with Python 3.6

This is a simple implementation of the board game Azul for rwo players

Todo:
congratulate winner, Write a display function for after scoring,
rewrite with better fundamental data structure (integers instead of strings),
make a simple way to add an AI script, think about graphics
"""

from AzulFunctions import *

print("Initializing GameState")
GameState = InitializeGame()

print("Commencing the gameplay loop")
while True:
    print("\nNEXT PLAYER:")
    DisplayGame(GameState)

    # Player enters their move
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

    # Check for end of round
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