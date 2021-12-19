from os import system, name as os_name
from colorama import init, Fore
from typing import Literal

# Initialise the `colorama` library to apply properly the colours in the future
init()

# The command to clear the screen according to the operating system
CLEAR_CMD = 'cls' if os_name == 'nt' else 'clear'

# Bi-dimensional tuple describing the coordinate offsets for one move in every possible direction
MOVEMENTS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

# Misc types for: coordinates, one movement, the possible player symbols, statistics dictionary about
# the number of pieces of each player and the total pieces placed on the board
CoordsType = tuple[int, int]
MovementType = tuple[int, int]
PlayerSymbolType = Literal["O", "X"]
PiecesCountType = dict[str, int]


def clear_screen() -> None:
    """
    Utility Function: erases terminal screen (regardless of the OS).
    No input
    Returns: None
    No local variables
    """
    system(CLEAR_CMD)


def print_game(possible_moves: list[CoordsType] = []) -> None:
    """
    Function: prints the playing board with characters, line by line.
    Input:
        - `possible_moves` (`list[tuple[int, int]]`; optional): a list of coordinate tuples
    Returns: None
    Local variables:
        - `counter` (`int`): counts the number of lines of the board to print it
        - `row_index` (in loop; `int`): keeps track of the row index.
        - `col_index` (in loop; `int`): keeps track of the column index
        - `square` (`str`): the value of each square of the board
        - `is_possible` (`bool`): checks if the coordinates of the square are in the `possible_moves` list
        - `colour` (`str`): gives a colour to the square depending on whether it is a possible move or not
        - `colour_reset` (`str`): resets the colour after the square if it has been coloured
        - `player_colour` (`str`): gives the square a colour depending on the symbol of the player
        - `player_colour_reset` (`str`): resets the colour after the square if it has been coloured
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
            square: str = game[row_index][col_index]
            # Check if the square is a possible move
            is_possible: bool = (row_index, col_index) in possible_moves

            # Colours to the squares!
            colour: str = Fore.LIGHTYELLOW_EX if is_possible else ""
            colour_reset: str = Fore.RESET if is_possible else ""
            player_colour: str = Fore.MAGENTA if square == "O" else (
                Fore.RED if square == "X" else Fore.CYAN)
            player_colour_reset: str = Fore.RESET

            # Show the square with an appropriate colour
            print(player_colour + colour + square + colour_reset + player_colour_reset, end="   ")

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
    square_coords: str = input("Entrez les coordonnées de la case : ").upper()

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
    Utility Function: computes the coordinates of the square positionned relatively
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
        - `player_symbol` (`str`): the symbol of the current player
    Returns: the symbol of the other player (either "O" or "X").
    No local variables
    """
    return "X" if player_symbol == "O" else "O"


def can_use_mov(coords: CoordsType, movement: MovementType) -> bool:
    """
    Utility Function: checks if the cursor movement can be applied,
    taking into account the coordinates of the current square and the
    edges of the board.
    Input:
        - `coords` (`tuple[int, int]`): the coordinates tuple of the current square
        - `movement` (`tuple[int, int]`): the movement tuple describing the move to attempt
    Returns: a boolean indicating whether the movement can be applied.
    No local variables
    """
    # Check that the coordinates are within the boundaries of the board
    return 0 <= coords[0] + movement[0] <= 7 and 0 <= coords[1] + movement[1] <= 7


def count_surrounding_squares(player_symbol: PlayerSymbolType, coords: CoordsType, direction: MovementType) -> int:
    """
    Function: counts the number of squares that can be gained by the
    current player in one direction by placing a piece on a certain square.
    Input:
        - `player_symbol` (`str`): the symbol of the current player
        - `coords` (`tuple[int, int]`): the coordinates tuple of the square in which to add a piece of the `player_symbol` colour
        - `direction` (`tuple[int, int]`): a movement tuple describing one move in the desired direction
    Returns: the number of squares that can be surrounded by the player according to the `direction` parameter
    Local variables:
        - `current_square` (`str`): the content of the square whose coordinates are given thanks to
          the `coords` argument
        - `pointer` (`tuple[int, int]`): a coordinates tuple that is updated at each iteration of the loop in accordance
          with the `direction` argument
        - `nb_squares` (`int`): the number of squares that can be sourrounded by the player
    """
    # Store current square in a dedicated variable for convenience
    current_square: str = game[coords[0]][coords[1]]

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
        while game[pointer[0]][pointer[1]] == get_other_player(player_symbol):
            nb_squares += 1
            if not can_use_mov(pointer, direction):
                break
            pointer = update_coords(pointer, direction)

        # If the final square is one of the current player, then all the counted squares can be sourrounded
        if game[pointer[0]][pointer[1]] == player_symbol:
            return nb_squares

    return 0


def count_pieces() -> PiecesCountType:
    """
    Function: calculates the number of pieces of each player.
    No input
    Returns: a dictionary describing the number of pieces of each player and the sum
    of the number of pieces. Available keys are `O`, `X` and `total`.
    Local variables:
        - `count` (`dict`): the ditionary containing the number of pieces of each player and the
          sum of the number of pieces. Its form is: {"O": int, "X": int, "total": int}
        - `row` (`list[str]`): each row of the board (iteratively)
        - `square` (`str`): each square of the board (iteratively)
    """
    count: PiecesCountType = {"O": 0, "X": 0, "total": 0}

    # Scan every square to know if it is occupied and by which player
    for row in game:
        for square in row:
            if square != "-":
                count[square] += 1
                # Also increment total count
                count["total"] += 1

    return count


def get_possible_moves(player_symbol: PlayerSymbolType) -> list[CoordsType]:
    """
    Function: computes the list of available squares for a player.
    Input:
        - `player_symbol` (`str`): the symbol of the current player
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
                if game[row_index][col_index] == "-":
                    surrounding_squares: int = count_surrounding_squares(
                        player_symbol, coords, direction)

                    if surrounding_squares > 0:
                        # The square is a possible move, so append it to the list of possible moves
                        possible_moves.append(coords)
                        # Stop the loop, because one direction is enough to place a piece on the square
                        break

    return possible_moves


def update_board(coords: CoordsType, player_symbol: PlayerSymbolType) -> None:
    """
    Function: updates the game board after a player has placed a piece
    in a certain square.
    Input:
        - `coords` (`tuple[int, int]`): the coordinates tuple of the square in which to add a piece
          of the `player_symbol` colour
        - `player_symbol` (`str`): the symbol of the current player
    Returns: None
    Local variables:
        - `direction` (`tuple[int, int]`): each direction tuple (iteratively)
        - `nb_squares` (`int`): the number of squares that should be replaced by `player_symbol`
          in each direction (iteratively)
        - `pointer` (`tuple[int, int]`): a coordinates tuple corresponding to each square (iteratively)
          in one direction to replace it with `player_symbol`; gets updated at each iteration by the
          `update_coords` function
    """
    # Make sure that the square is empty before placing the piece on it
    if game[coords[0]][coords[1]] == "-":
        # Find affected opponent squares in all directions
        for direction in MOVEMENTS:
            # Count the squares that can be surrounded by the player
            nb_squares = count_surrounding_squares(
                player_symbol, coords, direction)

            if nb_squares > 0:
                # Change the originally empty square to the player's symbol
                game[coords[0]][coords[1]] = player_symbol

                # Use a pointer to update `nb_squares` squares to the player's symbol
                pointer = update_coords(coords, direction)
                for _ in range(nb_squares):
                    game[pointer[0]][pointer[1]] = player_symbol
                    pointer = update_coords(pointer, direction)


def handle_game_over(pieces_count: PiecesCountType) -> None:
    """
    Function: handle the end of a game and log the winner and statistics to the console.
    Input:
        - `pieces_count` (`int`): a dictionary containing the number of pieces of each player and the total pieces
    Returns: None
    No local variables
    """
    if pieces_count["O"] > pieces_count["X"]:
        print(
            f"Le joueur O a gagné avec {pieces_count['O']} pions contre {pieces_count['X']} !")
    elif pieces_count["X"] > pieces_count["O"]:
        print(
            f"Le joueur X a gagné avec {pieces_count['X']} pions contre {pieces_count['O']} !")
    else:
        print(
            f"Egalité ! Les deux joueurs avaient tous les deux {pieces_count['O']} pions !")

# Keep track of the state of the game (gets updated to `True` when all squares have been filled)
game_over: bool = False

# The bi-dimensional list of strings representing the game board
game: list[list[str]] = [["-" for _ in range(8)] for _ in range(8)]

# Pre-fill the board with four initial pieces before the game starts
game[3][3] = "O"
game[3][4] = "X"
game[4][3] = "X"
game[4][4] = "O"

# Keep track of the current player
current_player: PlayerSymbolType = "O"

while not game_over:
    # Clear the screen to show a new board with the updated pieces
    clear_screen()

    # Compute the possible moves for one of the player (at their turn)
    possible_moves: list[CoordsType] = get_possible_moves(current_player)

    # Describe the number of pieces of both players and the total pieces on the board 
    nb_pieces: PiecesCountType = count_pieces()

    if nb_pieces["total"] == 64:
        # All squares are filled
        # Mark the game as over
        game_over = True

        # Handle the end of the game to print out the winner and statistics
        handle_game_over(nb_pieces)

    else:
        if len(possible_moves) == 0:
            # The current player cannot play, so pass their turn
            current_player = get_other_player(current_player)
            continue
        
        # Show the user whose turn it is
        print(f"Au joueur {current_player} de jouer !")

        # Statistics about the number of pieces and the total number of pieces
        print(
            f"Joueur O : {nb_pieces['O']} pions ; joueur X : {nb_pieces['X']} pions\n")

        # Show the board by passing the possible moves of the current player
        print_game(possible_moves)

        # Ask the user for input and update the board accordingly
        update_board(get_input(possible_moves), current_player)

        # Switch players
        current_player = get_other_player(current_player)

