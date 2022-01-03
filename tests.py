from typing import Literal
import main

SymbolType = Literal["O", "X", "-"]
BoardType = list[list[SymbolType]]

print("Testing the update_coords function...", end=" ")
assert main.update_coords((0, 0), (1, 0)) == (
    1, 0), "The update_coords function did not produce expected output!"
print("passed")


print("Testing the get_other_player function...", end=" ")
assert main.get_other_player("O") == "X" and \
    main.get_other_player("X") == "O", "The get_other_player function did not produce expected output!"
print("passed")


print("Testing the can_use_mov function...", end=" ")
assert main.can_use_mov((0, 0), (-1, 0)) == False and \
    main.can_use_mov((7, 7), (1, 0)) == False, "The can_use_mov function did not produce expected output!"
print("passed")


print("Testing the count_surrounding_squares function...", end=" ")
game: BoardType = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'O', '-', '-', '-', '-'], # Testing with the second last square of this row
    ['-', '-', '-', 'O', 'X', 'X', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.count_surrounding_squares("O", (1, 6), (1, -1), game) == 2,\
    "The count_surrounding_squares function did not produce expected output!"
print("passed")


print("Testing the get_opposite_mov function...", end=" ")
assert main.get_opposite_mov((1, 0)) == (-1, 0),\
    "The get_opposite_mov function did not produce expected output!"
print("passed")


print("Testing the get_closest_other_piece function...", end=" ")
game: BoardType = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'X', 'O', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', 'X', '-', '-'],
    ['-', '-', 'O', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.get_closest_other_piece("X", (4, 5), (-1, -1), game) == "-" and\
    main.get_closest_other_piece("X", (4, 5), (0, -1), game) == "O",\
    "The get_closest_other_piece function did not produce expected output!"
print("passed")


print("Testing the would_be_stable function...", end=" ")
game: BoardType = [
    ['-', '-', '-', '-', '-', 'O', 'X', 'X'],
    ['-', '-', '-', '-', '-', '-', 'X', '-'],
    ['-', '-', '-', '-', 'O', 'X', 'X', 'X'],
    ['-', '-', '-', 'O', 'O', 'O', '-', '-'],
    ['-', '-', 'O', 'O', 'O', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.would_be_stable("X", (0, 4), game) == True and\
    main.would_be_stable("X", (4, 5), game) == False,\
    "The would_be_stable function did not produce expected output!"
print("passed")


print("Testing the count_pieces function...", end=" ")
game = [
    ['-', '-', '-', '-', '-', 'X', '-', 'O'],
    ['-', 'O', 'X', '-', '-', '-', 'O', '-'],
    ['-', '-', 'O', 'X', 'X', 'O', 'X', 'X'],
    ['-', '-', 'X', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'X', 'O', '-', '-', '-'],
    ['-', '-', 'O', '-', 'X', 'X', 'X', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.count_pieces(game) == {"O": 8, "X": 12, "total": 20},\
    "The count_pieces function did not produce expected output!"
print("passed")


print("Testing the get_possible_moves function...", end=" ")
game = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'X', 'O', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert sorted(main.get_possible_moves("O", game)) == sorted([(2, 4), (5, 3), (4, 2), (3, 5)]),\
    "The get_possible_moves function did not produce expected output!"
print("passed")


print("Testing the update_board function...", end=" ")
game = [
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['-', '-', 'O', 'X', 'X', '-', 'O', 'O'],
    ['X', 'X', 'X', 'O', 'X', 'X', 'O', 'X'],
    ['-', '-', 'X', 'X', 'O', 'X', 'O', 'X'],
    ['-', '-', 'X', 'X', 'X', 'O', 'O', 'X'],
    ['-', '-', 'X', '-', '-', 'X', 'O', 'X'],
    ['-', '-', 'X', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.update_board((1, 5), "O", game) == [
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['-', '-', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['X', 'X', 'X', 'O', 'X', 'O', 'O', 'X'],
    ['-', '-', 'X', 'X', 'O', 'O', 'O', 'X'],
    ['-', '-', 'X', 'X', 'X', 'O', 'O', 'X'],
    ['-', '-', 'X', '-', '-', 'X', 'O', 'X'],
    ['-', '-', 'X', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ], "The update_board function did not produce expected output!"
print("passed")

print("Testing the compute_score function...", end=" ")
game = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'X', 'O', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
# Detailed calculation of the score:
#   For the X player:
#    - 4 for the position of the square of coordinates `(4, 5)`
#    - 15 because the square of coordinates `(4, 5)` can't be taken back by the other player
#      at the next turn
#   For the O player at the next turn (negative points):
#    - -4 for the position of the square of coordinates `(3, 5)`
#    - -4 for the position of the square of coordinates `(5, 3)`
#    - -7 for the position of the square of coordinates `(5, 5)`
assert main.compute_score("X", (4, 5), game) == 4 + 15 + -1 * (4 + 4 + 7),\
    "The compute_score function did not produce expected output!"
print("passed")


print("Testing the get_computer_move function...", end=" ")
game = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'O', 'X', '-', '-', '-'],
    ['-', '-', '-', 'X', 'O', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
]
assert main.get_computer_move([(2, 3), (4, 5), (5, 4), (3, 2)], game) == (2, 3)
print("passed")


print("\nAll tests passed!")
