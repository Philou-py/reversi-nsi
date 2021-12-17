
board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0],
         [0,0,0,2,1,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

column = ("A","B","C","D","E","F","G","H")

def getInput():
    rowInput = input("Enter the coordinates : ").upper()
    for i in range(len(column)):
        if rowInput[1] == column[i]:
            x = i
    coords = (x, int(rowInput[0]) - 1)
    return coords



def coordinatesUpdate(coords:tuple, player:int):
    board[coords[1]][coords[0]] = player
 

def cellCount():
    count={1: 0, 2: 0}
    for ellement in board:
        for cell in ellement:
            if cell != 0: count[cell] += 1
    print(count)


def playerChanger(player):
    if player ==  1: return 2
    return 1

