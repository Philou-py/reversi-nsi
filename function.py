from colorama import init, Fore
from os import system, name as os_name
from typing import Literal
import os

#Initialise the `colorama` library to apply properly the colours in the future
init()

#Bi-dimensional list that defines the game board
board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0],
         [0,0,0,2,1,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

#Bi-dimensional tuple describing the coordinate offsets for one move in every possible direction
MOVEMENTS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))


PiecesCountType = dict[str, int]

#Tuple which defines the name of the columns
column = ("A","B","C","D","E","F","G","H")


def indexFinder(char: str):
    """""
    Function: find the index of the column from the letter
    
    Input: 
        -'char'
    Returns: a tuple that contains the index of the column

    Local variables: None
    """""
    for i in range(len(column)):
        if char == column[i]:
            return i+1

def getInput(player):
    """""
    Function: take player input and check if they are valid

    Input:
        -'player' the current player number

    Returns: a tuple which contains the coordinates of the move to be played on the board

    Local variables:
        -'rowInput': store player input to process it
        -'coords': stock the final coordinates
    """""
    rowInput = input("Enter the coordinates : ").upper()       
    while not (len(rowInput) == 2 and
        rowInput[0].isalpha() and
        "A" <= rowInput[0] <= "H" and
        rowInput[1].isdigit() and
        1 <= int(rowInput[1]) <= 8):
        rowInput = input("Enter the coordinates (exemple: B3) : ").upper()
    coords = (ord(rowInput[0]) - ord("A"), int(rowInput[1]) - 1)
    return coords

def cellCount():
    """""
    Function: count the number of pieces of each player

    Input: None

    Returns: a dictionary containing the number of pieces of each player and the total

    Local variables:
        -'count': a dictionary with 3 keys (1, 2, 'total') which allows to store the values
    """""
    count = {1:0, 2:0, "total":0}
    for row in board:
        for cell in row:
            if cell != 0:
                count[cell]+=1
                count["total"]+=1
    return count


def canUseMov(coords, movement) -> bool:
    """""
    Function: checks if the cursor movement can be applied, considering the coordinates
    of the current square and the edges of the board.

    Input:
        -'coords' the coordinates of a cell
        -'movement' the movement that we want to apply to the cell (see the 'MOVEMENTS' variable)

    Returns: returns a boolean depending on whether the movement can be applied

    Local variables: none.
    """""
    return 0 <= coords[0] + movement[0] <= 7 and 0 <= coords[1] + movement[1] <= 7


def getOtherPlayer(player):
    """""
    Function: change the player

    Input: 
        -'player' the current player

    Returns: an int which is the number of the other player

    Local variables: none.
    """""
    if player == 1: return 2
    return 1


def nextCoords(coords, direction):
    """""
    Function:

    Input:
        -'coords' the coordinates of a cell
        -'direction' the movement that we want to apply to the cell (see the 'MOVEMENTS' variable)

    Returns: next coordinate after the deplacement

    Local variables: none.
    """""
    return (coords[0]+ direction[0], coords[1]+direction[1])


def countSurroundingCell(player, coords, direction):
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    cell = board[coords[0]][coords[1]]
    if (cell == 0 or cell == player) and canUseMov(coords, direction):
        pointer = nextCoords(coords, direction)
        cellNumb = 0
        while board[pointer[0]][pointer[1]] == getOtherPlayer(player):
            cellNumb += 1
            if not canUseMov(pointer, direction):
                break
            pointer = nextCoords(pointer, direction)
        if board[pointer[0]][pointer[1]] == player:
            return cellNumb
    return 0


def checkPossibleMoves(player):
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    possibleMoves = []
    for xIndex in range(8):
        for yindex in range(8):
            coords = (xIndex, yindex)
            for direction in MOVEMENTS:
                if board[xIndex][yindex] == 0:
                    surroundingCell = countSurroundingCell(player, coords, direction)
                    if surroundingCell > 0:
                        possibleMoves.append(coords)
                        break
    return possibleMoves

def updateBoard(coords, player):
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    if board[coords[0]][coords[1]] == 0:
        for direction in MOVEMENTS:
            cellNumb = countSurroundingCell(player, coords, direction)
            if cellNumb > 0:
                board[coords[0]][coords[1]] = player
                pointer = nextCoords(coords, direction)
                for _ in range(cellNumb):
                    board[pointer[0]][pointer[1]] = player
                    pointer = nextCoords(pointer, direction)
                 

def handelGameOver():
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    count = cellCount()
    if count[1] > count[2]:
        print(f"le joueur 1 a gagné")
    if count[1] < count[2]:
        print(f"le joueur 2 a gagné")
    else:
        print(f"equality")


def renderer(player, possibleMoves, cellNumb):
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    clearScreen()
    print("   A  B  C  D  E  F  G  H")
    for colIndex in range(8):
        print(colIndex+1, end="")
        colIndex += 1
        for rowIndex in range(8):
            is_possible = possibleMoves
            if (rowIndex,colIndex-1) in is_possible:
                print(" ", Fore.BLUE+"■"+Fore.RESET, end='')
            elif board[rowIndex][colIndex-1] == 0:
                print(" ", Fore.GREEN+"■"+Fore.RESET, end='')
            elif board[rowIndex][colIndex-1] == 1:
                print(" ", Fore.WHITE+"■"+Fore.RESET, end="")
            elif board[rowIndex][colIndex-1] == 2:
                print(" ", Fore.RED+"■"+Fore.RESET, end="")
        print("\r")
    print(f"white : {cellNumb[1]} | black : {cellNumb[2]} | total : {cellNumb['total']}/64")
    print(f"It's player {player}'s turn")
    coords = getInput(player)
    return coords

def clearScreen():
    """""
    Function:

    Input:

    Returns:

    Local variables:
    """""
    system('cls' if os_name == 'nt' else 'clear')
