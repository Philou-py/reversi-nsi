import function

player = 1
gameOver = False

while not gameOver:
    function.clearScreen()
    possibleMoves = function.checkPossibleMoves(player)
    cellNumb = function.cellCount()

    if cellNumb["total"] == 64:
        # All squares are filled
        # Mark the game as over
        game_over = True

        # Handle the end of the game to print out the winner and statistics
        function.handelGameOver()
    else:
        if len(possibleMoves) == 0:
            # The current player cannot play, so pass their turn
            player = function.getOtherPlayer(player)
            continue
        coords = function.renderer(player, possibleMoves, cellNumb)
        function.updateBoard(coords, player)
        player = function.getOtherPlayer(player)
