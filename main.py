from os import system, name as os_name
from colorama import init, Fore, Back
from typing import Literal
from copy import deepcopy

# The command string to clear the screen according to the operating system
CLEAR_CMD = 'cls' if os_name == 'nt' else 'clear'

# Bi-dimensional tuple describing the coordinate offsets for one move in every possible direction
MOVEMENTS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

# Bi-dimensional tuple describing the opposite movements to those defined in the MOVEMENTS constant
OPPOSITE_MOVEMENTS = ((1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1))

# A bi-dimensional list describing an estimation of the worth of each square on the board
WEIGHTING = [
    [99, -8, 8, 6, 6, 8, -8, 99],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [8, -4, 7, 4, 4, 7, -4, 8],
    [6, -3, 4, 0, 0, 4, -3, 6],
    [6, -3, 4, 0, 0, 4, -3, 6],
    [8, -4, 7, 4, 4, 7, -4, 8],
    [-8, -24, -4, -3, -3, -4, -24, -8],
    [99, -8, 8, 6, 6, 8, -8, 99],
]

# Misc types for: coordinates, one movement, the possible player symbols, the possible symbols on the
# board, and for a statistics dictionary about the number of pieces of each player and the total pieces
# placed on the board
# The coordinates of a square, according to CoordsType are given the following way:
#     - First vertical position from the top
#     - Second horizontal position from the left
#     - Both numbers start from zero and end at 7
CoordsType = tuple[int, int]
MovementType = tuple[int, int]
PlayerSymbolType = Literal["O", "X"]
SymbolType = Literal["O", "X", "-"]
PiecesCountType = dict[str, int]
BoardType = list[list[SymbolType]]


def clear_screen() -> None:
    """
    Utility Function: erases terminal screen (regardless of the OS).

    No input

    Returns: None

    No local variables
    """
    system(CLEAR_CMD)


def print_game(possible_moves: list[CoordsType] = [], last_move: CoordsType = None) -> None:
    """
    Function: prints the playing board with characters, line by line.

    Input:
        - `possible_moves` (`list[tuple[int, int]]`; optional): a list of coordinate tuples
        - `last_move` (`tuple[int, int]`; optional): the coordinates of the last move

    Returns: None

    Local variables:
        - `counter` (`int`): counts the number of lines of the board to print it
        - `row_index` (in loop; `int`): keeps track of the row index.
        - `col_index` (in loop; `int`): keeps track of the column index
        - `square` (`str`): the value of each square of the board
        - `is_possible` (`bool`): checks if the coordinates of the square are in the `possible_moves` list
        - `colour` (`str`): gives a colour to the square depending on whether it is a possible move or not
        - `player_colour` (`str`): gives the square a colour depending on the symbol of the player
        - `last_move_colour` (`str`): colour the square if it was the last move
    """
    # Show a heading so that the user can identify the squares more easily
    print(Fore.YELLOW + "   A   B   C   D   E   F   G   H" + Fore.RESET)
    # Row counter
    counter: int = 1
    for row_index in range(8):
        # Show the column number
        print(Fore.YELLOW + str(counter) + Fore.RESET, end="  ")
        counter += 1
        for col_index in range(8):
            # Load the square given the row and column indexes
            square: SymbolType = game[row_index][col_index]
            # Check if the square is a possible move
            is_possible: bool = (row_index, col_index) in possible_moves

            # Colours for the different squares!
            possible_colour: str = Fore.LIGHTYELLOW_EX if is_possible else ""
            player_colour: str = Fore.MAGENTA if square == "O" else (
                Fore.RED if square == "X" else Fore.CYAN)
            last_move_colour: str = (Back.LIGHTMAGENTA_EX if square == "O" else Back.LIGHTRED_EX)\
                if (row_index, col_index) == last_move else ""

            # Show the square with an appropriate colour
            print(player_colour + possible_colour + last_move_colour + square + Fore.RESET + Back.RESET, end="   ")

        # Skip a line
        print("\n")


def get_input(possible_moves: list[CoordsType] = None) -> CoordsType:
    """
    Function: asks the user to enter the coordinates (with a letter and a number)
    of the square to place the piece on. Retries while the user input format
    isn't correct and while the square is not in the list of possible moves (if provided).

    Input:
        - `possible_moves` (`list[tuple[int, int]]`; optional): a list of coordinate tuples

    Returns: a tuple containing the real coordinates of the element in the game array.

    Local variables:
        - `square_coords` (`str`): the input that the user enters (supposed to correspond to the
          coordinates of a square)
        - `coords` (`tuple[int, int]`): the coordinates tuple that is garanteed to refer to an existing
          square on the board
    """
    # Get user input and ignore letter case
    square_coords: str = input("Où souhaitez-vous poser un pion ? ").upper()

    # Keep re-asking for the coordinates while they are not given in the correct format
    while not (len(square_coords) == 2 and
               square_coords[0].isalpha() and
               "A" <= square_coords[0] <= "H" and
               square_coords[1].isdigit() and
               1 <= int(square_coords[1]) <= 8):
        square_coords = input(
            "Entrez les coordonnées de la case (exemple: A4) : ").upper()

    # Once in the desired format, parse the input string to actual coordinates
    coords: CoordsType = (int(square_coords[1]) - 1, ord(square_coords[0]) - ord("A"))

    # If the square is not a possible move, then call this function again
    if possible_moves and coords not in possible_moves:
        print("Vous ne pouvez pas placer un pion sur cette case !")
        return get_input(possible_moves)

    return coords


def update_coords(coords: CoordsType, mov: MovementType) -> CoordsType:
    """
    Utility Function: computes the coordinates of the square positioned relatively
    to the original one thanks to the provided direction.

    Input:
        - `coords` (`tuple[int, int]`): a tuple containing the coordinates of the original square
        - `mov` (`tuple[int, int]`): a tuple containing the vertical and the horizontal offsets

    Returns: a tuple of the new coordinates after a move according to the `mov` parameter.

    No local variables
    """
    return (coords[0] + mov[0], coords[1] + mov[1])


def get_other_player(player_symbol: PlayerSymbolType) -> PlayerSymbolType:
    """
    Utility Function: gets the symbol of the other player.

    Input:
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the current player

    Returns: the symbol of the other player (either "O" or "X").

    No local variables
    """
    return "X" if player_symbol == "O" else "O"


def can_use_mov(coords: CoordsType, movement: MovementType) -> bool:
    """
    Utility Function: checks if the cursor movement can be applied, considering the coordinates
    of the current square and the edges of the board.

    Input:
        - `coords` (`tuple[int, int]`): the coordinates tuple of the current square
        - `movement` (`tuple[int, int]`): the movement tuple describing the move to attempt

    Returns: a boolean indicating whether the movement can be applied.

    No local variables
    """
    # Check that the coordinates are within the boundaries of the board
    return 0 <= coords[0] + movement[0] <= 7 and 0 <= coords[1] + movement[1] <= 7


def count_surrounding_squares(
        player_symbol: PlayerSymbolType,
        coords: CoordsType,
        direction: MovementType,
        board: BoardType
    ) -> int:
    """
    Function: counts the number of squares that can be gained by the
    current player in one direction by placing a piece on a certain square.

    Input:
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the current player
        - `coords` (`tuple[int, int]`): the coordinates tuple of the square in which to add a piece of the `player_symbol` colour
        - `direction` (`tuple[int, int]`): a movement tuple describing one move in the desired direction
        - `board` (`list[list[Literal["O", "X", "-"]]]`): the game board

    Returns: the number of squares that can be surrounded by the player according to the `direction` parameter

    Local variables:
        - `current_square` (`str`): the content of the square whose coordinates are given thanks to
          the `coords` argument
        - `pointer` (`tuple[int, int]`): a coordinates tuple that is updated at each iteration of the loop
          to move one square away, according to the `direction` argument
        - `nb_squares` (`int`): the number of squares that can be sourrounded by the player
    """
    # Store current square in a dedicated variable for convenience
    current_square: SymbolType = board[coords[0]][coords[1]]

    # Check if the current square is empty (or occupied by current player) and that it does not
    # exceed the limits of the board
    if (current_square == "-" or current_square == player_symbol) and can_use_mov(coords, direction):
        # Use a pointer that will move according to the given direction in order to check if
        # opponent squares can be taken by the current player
        pointer: CoordsType = update_coords(coords, direction)
        # Keep track of the number of square that can be possibly surrounded
        nb_squares: int = 0

        # Move to the next square until we reach either one border of the board, a white square
        # or a square of the current player
        while board[pointer[0]][pointer[1]] == get_other_player(player_symbol):
            nb_squares += 1
            if not can_use_mov(pointer, direction):
                break
            pointer = update_coords(pointer, direction)

        # If the final square is one of the current player, then all the counted squares can be sourrounded
        if board[pointer[0]][pointer[1]] == player_symbol:
            return nb_squares

    return 0


def get_opposite_mov(mov: MovementType) -> MovementType:
    """
    Utility Function: gets the opposite movement of the one passed as first argument,
    using the OPPOSITE_MOVEMENTS constant as reference.

    Input:
        - `mov` (`tuple[int, int]`): the movement whose opposite is wanted

    Returns: the opposite movement to `mov`.

    No local variables
    """
    return OPPOSITE_MOVEMENTS[MOVEMENTS.index(mov)]


def get_closest_other_piece(
        symbol: SymbolType,
        coords: CoordsType,
        direction: MovementType,
        board: BoardType
    ) -> SymbolType | None:
    """
    Function: fetches the closest piece according to one direction different from the symbol given
    as first argument.

    Input:
        - `symbol` (`Literal["O", "X", "-"]`): the symbol of the square from which to begin the search
        - `coords` (`tuple[int, int]`): the coordinates of the current square
        - `direction` (`tuple[int, int]`): the direction in which to search
        - `board` (`list[list[Literal["O", "X", "-"]]]`): the game board

    Returns: the first square different from `symbol` found when scanning the board in the given direction.

    Local variables:
        - `is_off_limits` (`bool`): a boolean that indicates if the search is off the limits of the board
        - `pointer` (`tuple[int, int]`): a coordinates tuple that is updated at each iteration of the loop
          to move one square away, according to the `direction` argument
    """
    # Keep track of the position of the pointer when it reaches the edges of the board
    is_off_limits: bool = False

    # First check if the pointer can be moved in the given direction
    if can_use_mov(coords, direction):
        pointer: CoordsType = update_coords(coords, direction)

        # Keep going until reaching a different symbol
        while board[pointer[0]][pointer[1]] == symbol:
            if not can_use_mov(pointer, direction):
                # The pointer has reached the limits, so stop the loop
                is_off_limits = True
                break
            # Update pointer in the given direction
            pointer = update_coords(pointer, direction)

    else:
        is_off_limits = True
    return None if is_off_limits else board[pointer[0]][pointer[1]]


def would_be_stable(player_symbol: PlayerSymbolType, coords: CoordsType, board: BoardType) -> bool:
    """
    Function: determines if a square would be stable if a piece was placed onto it. A square is
    considered to be stable if it can't be taken by the other player at the next move.

    Input:
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the wanted player
        - `coords` (`tuple[int, int]`): the coordinates tuple of the empty square to be tested
        - `board` (`list[list[Literal["O", "X", "-"]]]`): the game board before the piece has been placed

    Returns: a boolean indicating if the square with a piece of `player_symbol` on it would be stable.

    Local variables:
        - `new_board` (`list[list[Literal["O", "X", "-"]]]`): the new game board with the piece placed on it
        - `is_stable` (`bool`): a boolean indicating whether the square is stable or not
        - `piece` (`Literal["-"]`)
    """
    # Make sure that the square is empty
    assert board[coords[0]][coords[1]] == "-",\
        "The square whose coordinates were passed as argument to the would_be_stable function is not empty!"

    # Create a new board simulating that the `player_symbol` places a piece on the square with
    # the `coords` coordinates
    new_board = update_board(coords, player_symbol, board)

    # First assume that the square is stable
    is_stable = True

    # Test each movement iteratively
    for mov in MOVEMENTS:
        # The square is not stable, if in one direction, the closest other piece is the opponent and
        # there is a free square in the opposite direction.
        if (get_closest_other_piece(player_symbol, coords, mov, new_board) == get_other_player(player_symbol) and\
                get_closest_other_piece(player_symbol, coords, get_opposite_mov(mov), new_board) == "-"):
            # (get_closest_other_piece(player_symbol, coords, mov, new_board) == "-" and\
            #     get_closest_other_piece(player_symbol, coords, get_opposite_mov(mov), new_board) == "-"):
            is_stable = False

    return is_stable


def count_pieces(board: BoardType) -> PiecesCountType:
    """
    Function: calculates the number of pieces of each player.

    No input

    Returns: a dictionary describing the number of pieces of each player and the sum
    of the number of pieces. Available keys are `O`, `X` and `total`.

    Local variables:
        - `count` (`dict`): the ditionary containing the number of pieces of each player and the
          sum of the number of pieces. Its form is: {"O": int, "X": int, "total": int}
        - `row` (`list[Literal["O", "X", "-"]]`): each row of the board (iteratively)
        - `symbol` (`Literal["O", "X", "-"]`): each square of the board (iteratively)
    """
    # First initialise the statistics dictionary with no pieces for each player
    count: PiecesCountType = {"O": 0, "X": 0, "total": 0}

    # Scan every square to know if it is occupied and by which player
    for row in board:
        for symbol in row:
            if symbol != "-":
                # Increment the number of squares for the `symbol` player
                count[symbol] += 1
                # Also increment total count
                count["total"] += 1

    return count


def get_possible_moves(player_symbol: PlayerSymbolType, board: BoardType) -> list[CoordsType]:
    """
    Function: computes the list of available squares for a player.

    Input:
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the current player

    Returns: a list of coordinate tuples indicating the possibilities
    available to the current player.

    Local variables:
        - `possible_moves` (`list[tuple[int, int]]`): the list of coordinate tuples indicating
          the possibilities available to the current player
        - `row_index` (`int`): the index of each row of the board (iteratively)
        - `col_index` (`int`): the index of each column of the board (iteratively)
        - `coords` (`tuple[int, int]`): the coordinate tuple of each square of the board (iteratively)
        - `surrounding_squares` (`int`): the number of surrounding squares for each square in one
          direction (iteratively)
    """
    possible_moves: list[CoordsType] = []

    # Go over each square in the grid and find out if the number of sourrounding squares is greater
    # than 0 (that means if the player can place a piece on the square in question)
    for row_index in range(8):
        for col_index in range(8):
            coords: CoordsType = (row_index, col_index)

            # Check each direction for every square
            for direction in MOVEMENTS:
                # Make sure to test only empty squares
                if board[row_index][col_index] == "-":
                    surrounding_squares: int = count_surrounding_squares(player_symbol, coords, direction, board)

                    if surrounding_squares > 0:
                        # The square is a possible move, so append it to the list of possible moves
                        possible_moves.append(coords)
                        # Stop the loop, because one direction is enough to place a piece on the square
                        break

    return possible_moves


def update_board(coords: CoordsType, player_symbol: PlayerSymbolType, board: BoardType) -> BoardType:
    """
    Function: updates the game board after a player has placed a piece
    in a certain square.

    Input:
        - `coords` (`tuple[int, int]`): the coordinates tuple of the square in which to add a piece
          of the `player_symbol` colour
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the current player

    Returns: None

    Local variables:
        - `direction` (`tuple[int, int]`): each direction tuple (iteratively)
        - `nb_squares` (`int`): the number of squares that should be replaced by `player_symbol`
          in each direction (iteratively)
        - `pointer` (`tuple[int, int]`): a coordinates tuple corresponding to each square (iteratively)
          in one direction to replace it with `player_symbol`; gets updated at each iteration by the
          `update_coords` function
    """
    # Make a deep copy of the game board in order to not modify the global game variable
    board = deepcopy(board)

    # Make sure that the square is empty before placing the piece on it
    if board[coords[0]][coords[1]] == "-":
        # Find affected opponent squares in all directions
        for direction in MOVEMENTS:
            # Count the squares that can be surrounded by the player
            nb_squares = count_surrounding_squares(player_symbol, coords, direction, board)

            if nb_squares > 0:
                # Change the originally empty square to the player's symbol
                board[coords[0]][coords[1]] = player_symbol

                # Use a pointer to update `nb_squares` squares to the player's symbol
                pointer = update_coords(coords, direction)
                for _ in range(nb_squares):
                    board[pointer[0]][pointer[1]] = player_symbol
                    pointer = update_coords(pointer, direction)
    return board

def compute_score(player_symbol: PlayerSymbolType, coords: CoordsType, board: BoardType) -> int:
    """
    Function: computes the score of the given square if `player_symbol` placed a piece on it, thanks
    to three strategies: positional strategy, stable pieces strategy and a blocking strategy for
    the player after.

    Input:
        - `player_symbol` (`Literal["O", "X"]`): the symbol of the player for which to calculate the score
        - `coords` (`tuple[int, int]`): the coordinates of the square where a `player_symbol` piece
          will be placed for simulation
        - `board` (`list[list[Literal["O", "X"]]]`): the game board

    Returns: an integer representing the computed score of a square.

    Local variables:
        - `score` (`int`): the score for a square
        - `new_board` (`list[list[Literal["O", "X", "-"]]]`): the game board on which a `player_symbol`
          piece will be placed for a simulation
        - `other_players_moves` (`list[CoordsType]`): a list of the possible moves for the player after,
          assuming that the computer places a piece in the square of coordinates `coords`
        - `other_players_score` (`int`): the sum of the scores for each square in `other_players_moves`
        - `move` (`tuple[int, int]`): a coordinates tuple that takes the value of each item of
          `other_players_moves` iteratively
    """
    score: int = 0

    # Positional strategy: add a weight to each square that is determined by the WEIGHTING constant
    # The weight is added to the score of the square
    score += WEIGHTING[coords[0]][coords[1]]

    # Stable pieces strategy: add 15 to the score of the square if it would be stable
    if would_be_stable(player_symbol, coords, board):
        score += 15

    # Blocking strategy: calculate the same score for the player after to make sure the
    # player after does not have too good possibilities
    # Only use this strategy when the simulation is made for a move of the computer
    if player_symbol == "X":
        # Create a new board simulating a move of the computer on the `coords` square
        new_board: BoardType = update_board(coords, player_symbol, board)

        # List the possible moves for the `O` player
        other_players_moves: list[CoordsType] = get_possible_moves("O", new_board)

        other_players_score: int = 0

        # Sum the scores of each possible move
        for move in other_players_moves:
            other_players_score += compute_score("O", move, new_board)

        # Add this score as a penalty for the `coords` square
        score += -1 * other_players_score

    return score


def get_computer_move(possible_moves: list[CoordsType], board: BoardType) -> CoordsType:
    """
    Function: computes the best move, by establishing a score for each possible move.

    Input:
        - `possible_moves` (`list[tuple[int, int]]`): the list of possible moves for the
          computer
        - `board` (`list[list[Literal["O", "X", "-"]]]`): the game board

    Returns: the coordinates of the square that obtained the best score.

    Local variables:
        - `scores` (`list[int]`): the list of scores for each possible move
    """
    # Initialise a list to store the score of each possible move
    scores: list[int] = []

    # Scan every possible move and compute its score
    for possible_move in possible_moves:
        scores.append(compute_score("X", possible_move, board))

    # Find the move with the best score and return it
    return possible_moves[scores.index(max(scores))]


def handle_game_over(pieces_count: PiecesCountType, last_move: CoordsType) -> None:
    """
    Function: handles the end of a game and logs the winner and statistics to the console.

    Input:
        - `pieces_count` (`int`): a dictionary containing the number of pieces of each player and the total pieces
        - `last_move` (`tuple[int, int]`; optional): the coordinates of the last move

    Returns: None

    No local variables
    """
    print_game([], last_move)
    if pieces_count["O"] > pieces_count["X"]:
        print(f"Le joueur O a gagné avec {pieces_count['O']} pions contre {pieces_count['X']} !")

    elif pieces_count["X"] > pieces_count["O"]:
        print(f"Le joueur X a gagné avec {pieces_count['X']} pions contre {pieces_count['O']} !")

    else:
        print(f"Egalité ! Les deux joueurs avaient tous les deux {pieces_count['O']} pions !")


# Don't start the game when importing a function from this module
if __name__ == "__main__":

    # Initialise the `colorama` library to apply properly the colours in the future
    init()

    # Keep track of the state of the game (gets updated to `True` when all squares have been filled)
    game_over: bool = False

    # The bi-dimensional list of strings representing the game board
    game: BoardType = [["-" for _ in range(8)] for _ in range(8)]

    # Pre-fill the board with four initial pieces before the game starts
    game[3][3] = "O"
    game[3][4] = "X"
    game[4][3] = "X"
    game[4][4] = "O"

    # Configuration for a game against https://reversi.zone with white disks
    # X: python program - O: website's AI
    # game[3][3] = "X"
    # game[3][4] = "X"
    # game[4][3] = "O"
    # game[4][4] = "X"
    # game[2][4] = "X"

    print("Bienvenue au jeu du Reversi !")

    # Make the user choose the game mode
    against_ai_input: str = input("Souhaitez-vous jouer contre l'ordinateur ? (oui/non) ").lower()

    # Re-ask while the input is incorrect
    while against_ai_input != "oui" and against_ai_input != "non":
        against_ai_input = input("Souhaitez-vous jouer contre l'ordinateur ? (oui/non) ").lower()

    against_ai: bool = against_ai_input == "oui"

    if against_ai:
        print("Compris ! Vous utiliserez les pions marqués avec un 'O', et l'ordinateur 'X'.\nBon jeu !")
    else:
        print("Compris ! Le joueur 1 utilisera les pions marqués avec un 'O' et le joueur 2 aura ceux avec un 'X'.\nBon jeu !")

    # Keep track of the current player
    current_player: PlayerSymbolType = "O"

    # Know if one player already skipped its turn and stop the game if both can't play
    last_turn_skipped: bool = False

    # Keep track of the last move
    last_move: CoordsType = (-1, -1)

    while not game_over:
        # Clear the screen to show a new board with the updated pieces
        clear_screen()

        # Compute the possible moves for one of the player (at their turn)
        possible_moves: list[CoordsType] = get_possible_moves(current_player, game)

        # Describe the number of pieces of both players and the total pieces on the board 
        nb_pieces: PiecesCountType = count_pieces(game)

        if nb_pieces["total"] == 64:
            # All squares are filled
            # Mark the game as over
            game_over = True

            # Handle the end of the game to print out the winner and statistics
            handle_game_over(nb_pieces, last_move)
            break

        if len(possible_moves) == 0:
            if last_turn_skipped:
                # The last player died, so end the game
                game_over = True
                handle_game_over(nb_pieces, last_move)
            else:
                last_turn_skipped = True

            # The current player cannot play, so skip their turn
            current_player = get_other_player(current_player)
            continue

        else:
            last_turn_skipped = False
        
        # Don't show messages if it is the computer's turn
        if not (against_ai and current_player == "X"):
            # Show the user whose turn it is
            print(f"Au joueur {current_player} de jouer !")

            # Statistics about the number of pieces and the total number of pieces
            print(
                f"Joueur O : {nb_pieces['O']} pions ; joueur X : {nb_pieces['X']} pions\n")

            # Show the board by passing the possible moves of the current player
            print_game(possible_moves, last_move)

        if against_ai == False or current_player == "O":
            # Ask the user for input
            move = get_input(possible_moves)
        else:
            move = get_computer_move(possible_moves, game)

        # Records the move for the next turn
        last_move = move

        # Update the board accordingly
        game = update_board(move, current_player, game)

        # Switch players
        current_player = get_other_player(current_player)

