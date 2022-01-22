import function
import loadingscreen
import shutil, os
from time import sleep
from os import system
import os
import time

#displays the loading screen
loadingscreen.launch()

#set the current player to one
player = 1

gameOver = False

while not gameOver:
    #call the finctioon to clear the screen
    function.clearScreen()

    possibleMoves = function.checkPossibleMoves(player)
    #count the number of cell to display it after
    cellNumb = function.cellCount()

    if cellNumb["total"] == 64:
        # Mark the game as over if all the cell are filed
        gameOver = True

        # Handle the end of the game to print out the winner and statistics
        function.handelGameOver()
        time.sleep(3)
        function.saveScore(cellNumb)
    else:
        if len(possibleMoves) == 0:
            # The current player cannot play, so pass their turn
            player = function.getOtherPlayer(player)
            continue
        coords = function.renderer(player, possibleMoves, cellNumb)
        function.updateBoard(coords, player)
        player = function.getOtherPlayer(player)

time.sleep(4)

