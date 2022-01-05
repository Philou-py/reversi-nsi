from colorama import init, Fore
from os import system, name as os_name
from typing import Literal

init()
board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0],
         [0,0,0,2,1,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

MOVEMENTS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
PiecesCountType = dict[str, int]
column = ("A","B","C","D","E","F","G","H")

def indexFinder(char):
    for i in range(len(column)):
        if char == column[i]:
            return i+1

def getInput(player):
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
    count = {1:0, 2:0, "total":0}
    for row in board:
        for cell in row:
            if cell != 0:
                count[cell]+=1
                count["total"]+=1
    return count


def canUseMov(coords, movement) -> bool:
    return 0 <= coords[0] + movement[0] <= 7 and 0 <= coords[1] + movement[1] <= 7


def getOtherPlayer(player):
    if player == 1: return 2
    return 1

def nextCoords(coords, direction):
    return (coords[0]+ direction[0], coords[1]+direction[1])


def countSurroundingCell(player, coords, direction):
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
    count = cellCount()
    if count[1] > count[2]:
        print(f"le joueur 1 a gagné")
    if count[1] < count[2]:
        print(f"le joueur 2 a gagné")
    else:
        print(f"equality")


def renderer(player, possibleMoves, cellNumb):
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
                print(" ", Fore.BLACK+"■"+Fore.RESET, end="")
        print("\r")
    print(f"white : {cellNumb[1]} | black : {cellNumb[2]} | total : {cellNumb['total']}/64")
    print(f"It's player {player}'s turn")
    coords = getInput(player)
    return coords

def clearScreen():
    system('cls' if os_name == 'nt' else 'clear')

