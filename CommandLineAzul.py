#runs in python 3.6
from AzulFunctions import *

# Move = {"Factory": "Factory 1", "Colour": 1, "Row": "First"}

print ("Initializing GameState")
GameState = InitializeGame()

print ("Commencing the gameplay loop")
while True:
    print("\nNEXT PLAYER:")
    DisplayGame(GameState)
    move = {"Factory": "Factory 4", "Colour": 3, "Row": "Fourth"}
    #Player goes

    if GameState["Next Player"] == "Player 1":
        move = Player1_Move(GameState)
    else:
        move = Player2_Move(GameState)

    #Gamestate is updated accordingly
    print("\n", move,"\n")
    UpdateGameState(GameState, move)
    print("UPDATED PLAYER BOARD:")
    DisplayGame(GameState)
    UpdatePlayer(GameState)
    
    #Checks for end of round
    if NoMoreTiles(GameState):
        print("End of round!")
        ScoreRound(GameState, "Player 1")
        ScoreRound(GameState, "Player 2")
        #reset for next round

    #if end-conditions are met, break. For now, stop after one move
