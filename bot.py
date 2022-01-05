import function as f
from function import MOVEMENTS, board

for coords in f.checkPossibleMoves(1):
    for direction in MOVEMENTS:
        print(direction)
#        if f.countSurroundingCell(1, (coords[0],coords[1]), direction) > 0:
        
