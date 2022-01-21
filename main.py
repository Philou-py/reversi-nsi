from os import system, name as os_name, get_terminal_size, path
try:
    from colorama import init, Fore, Back
except ModuleNotFoundError:
    raise ModuleNotFoundError("Veuillez installer les dépendances de l'application à l'aide de la commande \
suivante : pip install -r requirements.txt") from None
from typing import Literal
from copy import deepcopy
from csv import reader, writer
from datetime import datetime

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
# board, a statistics dictionary about the number of pieces of each player and the total pieces
# placed on the board, and for the variable containing a representation of the board.
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
    square_coords: str = input(Fore.GREEN + "Où souhaitez-vous poser un pion ? " + Fore.RESET).upper()

    # Keep re-asking for the coordinates while they are not given in the correct format
    while not (len(square_coords) == 2 and
               square_coords[0].isalpha() and
               "A" <= square_coords[0] <= "H" and
               square_coords[1].isdigit() and
               1 <= int(square_coords[1]) <= 8):
        square_coords = input(Fore.LIGHTBLUE_EX +
            "Entrez les coordonnées de la case (exemple: A4) : " + Fore.RESET).upper()

    # Once in the desired format, parse the input string to actual coordinates
    coords: CoordsType = (int(square_coords[1]) - 1, ord(square_coords[0]) - ord("A"))

    # If the square is not a possible move, then call this function again
    if possible_moves and coords not in possible_moves:
        print(Fore.RED + "Vous ne pouvez pas placer un pion sur cette case !" + Fore.RESET)
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
    Function: computes the score of the given square if the player placed a piece on it, thanks
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


def show_table(table: list[list[str | datetime | int]], last_game_id: int = -1) -> None:
    """
    Function: prints out a table of scores for a particular player containing rows corresponding
    to the following fields: the ID of the game, the opponent, the date / time, whether the game was
    won, the number of pieces of the player and the number of opponent pieces.

    Input:
        - `table` (`list[list[str | datetime | int]]`): a bi-dimensional list containing the results
          of games meant to the viewed by one specific player
        - `last_game_id` (`int`; optional): the ID of the last game played so that the results get highlighted

    Returns: None

    Local variables:
        - `FIELD_NAMES` (`list[str]`): the list containing the header of the table
        - `SEP_FORMAT` (`str`): an arbitrarily formatted template string to format a line of seperators
        - `ROW_FORMAT` (`str`): an arbitrarily formatted template string to format a row of the table
        - `row` (`list[str | datetime | int]`): one element of the `table` parameter (iteratively)
          representing the results of one game
        - `colour` (`str`): a string containing a colour for a row if it corresponds to the last game played
    """
    FIELD_NAMES: list[str] = ["#", "Adversaire", "Date / heure", "Gagnée", "Pions J", "Pions Adv"]

    # Setting a given length for each column of the table is required
    # See: https://docs.python.org/3/library/string.html#format-specification-mini-language
    SEP_FORMAT: str = "+{:-^5}+{:-^16}+{:-^25}+{:-^10}+{:-^11}+{:-^11}+"
    ROW_FORMAT: str = "|{:^5}|{:^16}|{:^25}|{:^10}|{:^11}|{:^11}|"

    print(SEP_FORMAT.format(*([""] * 6)))
    # Print the table header
    print(ROW_FORMAT.format(*FIELD_NAMES))
    print(SEP_FORMAT.format(*([""] * 6)))

    for row in table:
        colour: str = ""
        if row[0] == last_game_id:
            # Colour the row if it corresponds to the last game played
            colour = Fore.LIGHTCYAN_EX

        print(colour + ROW_FORMAT.format(*row) + (Fore.RESET + Fore.CYAN if colour else ""))

    print(SEP_FORMAT.format(*([""] * 6)))


def show_stats(player_name: str) -> None:
    """
    Function: reads the `scores.csv` file, filter and sort the data in order to show the results
    and ranks the games played by a particular player.

    Input:
        - `player_name` (`str`): the name / username of a player

    Returns: None

    Local variables:
        - `file` (`TextIOWrapper`): the `scores.csv` file opened with the UTF-8 encoding
        - `csv_reader` (`_reader`): a reader to parse CSV files
        - `parsed_scores` (`list[list[str | datetime | int]]`): a bi-dimensional list containing the
          results of the games played by `player_name`
        - `counter` (`int`): a counter to give an ID to each game
        - `row` (`list[str]`): the list containing the data of the results of one game (iteratively)
        - `last_game_id` (`int`): the ID of the last game played
    """
    # Open the scores file and create a reader to read the CSV data
    # Setting the newline argument to "" is recommended
    file = open("scores.csv", encoding="UTF-8", newline="")
    csv_reader = reader(file)

    parsed_scores = []
    counter: int = 0
    for row in csv_reader:
        # Skip the first line as it contains only the headers
        # Only add the line to the scores if it concerns the player requested
        if counter != 0 and (row[0] == player_name or row[1] == player_name):
            parsed_scores.append([
                counter, row[1] if row[0] == player_name else row[0],
                datetime.fromisoformat(row[2]).strftime("%d/%m/%Y à %X"),
                "Oui" if row[3] == player_name else ("Egalité" if row[3] == "OX" else "Non"),
                int(row[4]) if row[0] == player_name else int(row[5]),
                int(row[5]) if row[0] == player_name else int(row[4])
            ])
        counter += 1

    file.close()

    # The last game played corresponds to the last line of the list
    last_game_id: int = parsed_scores[-1][0]

    # Sort the results from highest to lowest score
    parsed_scores.sort(key=lambda line: line[4], reverse=True)

    print(Fore.GREEN +\
        f"\nClassement de la partie comparée aux autres réalisées par le joueur {player_name} :"\
        + Fore.RESET)
    print(Fore.CYAN, end="")
    show_table(parsed_scores, last_game_id)
    print(Fore.RESET, end="")


def save_results(winner: PlayerSymbolType | Literal["OX"], o_pieces: int, x_pieces: int) -> None:
    """
    Function: asks the user for the name(s) of the player(s) and saves the results of a game to the
    `scores.csv` file.

    Input:
        - `winner` (`Literal["O", "X", "OX"]`): the symbol of the player, or "OX" if it was a tie
        - `o_pieces` (`int`): the number of pieces of the O player
        - `x_pieces` (`int`): the number of pieces of the X player

    Returns: None

    Local variables:
        - `file` (`TextIOWrapper`): the `scores.csv` file opened with the UTF-8 encoding in `append` mode
        - `csv_write` (`_writer`): a writer to write into the file
        - `o_player_name` (`str`): the name or username of the O player (should not contain `,` because it
          is the separator of the CSV file)
        - `x_player_name` (`str`): the name or username of the X player (should not contain `,` because it
          is the separator of the CSV file)
        - `date_time` (`str`): the date and time of the game in ISO format (obtained thanks to the datetime
          library)
    """
    # Check if `scores.csv` exists
    if not path.isfile("./scores.csv"):
        file = open("scores.csv", "w", encoding="UTF-8", newline="")
        file.write("o_player_name,x_player_name,date_time,winner,o_pieces_nb,x_pieces_nb\n")
        file.close()

    # Open the file in `append` mode to save the results in a new line at the bottom of the file
    # Setting the newline argument to "" is the recommended behaviour
    file = open("scores.csv", "a", encoding="UTF-8", newline="")
    csv_writer = writer(file)

    print(Fore.YELLOW)

    # Ask the name of the player to attach it to the results of the game
    o_player_name: str = input("Entrez le nom du joueur O : ")

    # Limit the name's length to 16 characters (for display purposes)
    while (not 0 < len(o_player_name) <= 16) or "," in o_player_name or o_player_name == "Computer":
        o_player_name = input("Entrez le nom du joueur O (longueur maximale : 16 caractères ; \",\" \
            non autorisé) : ")

    x_player_name: str = input("Entrez le nom du joueur X : ") if not against_ai else "Computer"

    if not against_ai:
        # Limit the name's length to 16 characters (for display purposes)
        while (not 0 < len(x_player_name) <= 16) or "," in x_player_name or x_player_name == "Computer":
            x_player_name = input("Entrez le nom du joueur X (longueur maximale : 16 caractères ; \",\" \
                non autorisé) : ")

    # Record a timestamp of the end of the game and store it in ISO format
    date_time: str = datetime.now().isoformat()

    # Write data to the CSV file
    csv_writer.writerow([
        o_player_name, x_player_name, date_time,
        o_player_name if winner == "O" else ("OX" if winner == "OX" else x_player_name),
        o_pieces, x_pieces
    ])

    file.close()
    print("Les résultats ont bien été enregistrés !")

    print(Fore.RESET, end="")

    # When saving results, show also the ranking of the game in comparison to the other games
    if winner == "O" or winner == "OX":
        show_stats(o_player_name)
        if not against_ai:
            show_stats(x_player_name)
    else:
        if not against_ai:
            show_stats(x_player_name)
        show_stats(o_player_name)


def handle_game_over(pieces_count: PiecesCountType, last_move: CoordsType) -> None:
    """
    Function: handles the end of a game, prints out the winner and statistics and compares the game to
    the others saved in the `scores.csv` file.

    Input:
        - `pieces_count` (`int`): a dictionary containing the number of pieces of each player and the total pieces
        - `last_move` (`tuple[int, int]`; optional): the coordinates of the last move

    Returns: None

    Local variables:
        - `should_save_results_str` (`str`): a string input by the user to determine whether to save
          the results or not
        - `should_save_results` (`bool`): a boolean set to True if the user wanted to save the results
    """
    print_game([], last_move)

    print(Fore.GREEN)

    if pieces_count["O"] > pieces_count["X"]:
        winner = "O"
        print(f"Le joueur O a gagné avec {pieces_count['O']} pions contre {pieces_count['X']} !")

    elif pieces_count["X"] > pieces_count["O"]:
        winner = "X"
        print(f"Le joueur X a gagné avec {pieces_count['X']} pions contre {pieces_count['O']} !")

    else:
        winner = "OX"
        print(f"Egalité ! Les deux joueurs avaient tous les deux {pieces_count['O']} pions !")

    print(Fore.RESET)

    print(Fore.YELLOW)

    should_save_results_str = input("Souhaitez-vous enregistrer les résultats de cette partie ? ").lower()
    while should_save_results_str != "oui" and should_save_results_str != "non":
        should_save_results_str = input("Souhaitez-vous enregistrer les résultats de cette partie ? \
(oui / non) ").lower()

    print(Fore.RESET, end="")

    should_save_results = should_save_results_str == "oui"
    if should_save_results: save_results(winner, pieces_count["O"], pieces_count["X"])


# Don't start the game when importing a function from this module
if __name__ == "__main__":
    # Initialise the `colorama` library to apply properly the colours in the future
    init()

    # Terminal size check
    terminal_size = get_terminal_size()
    if terminal_size.columns < 100:
        print(Fore.RED)
        print("Votre terminal n'est pas assez large pour le bon affichage de ce programme !")
        print("Une largeur minimale de 100 caractères est recommandée !\n")
        print(Fore.RESET)
        input("Appuyez sur la touche Entrée pour continuer. ")

    if terminal_size.lines < 25:
        print(Fore.RED + "Une hauteur de terminal de 25 caractères est recommandée pour le bon \
affichage de ce programme !\n" + Fore.RESET)
        input("Appuyez sur la touche Entrée pour continuer. ")

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

    clear_screen()

    print(Fore.RED + "Bienvenue au jeu du Reversi !" + Fore.RESET)

    print(Fore.YELLOW,
    """
Voici les règles du jeu :

Chaque joueur dispose de pions marqués soit d'un O, soit d'un X qu'il peut placer,
à chaque tour, sur l'une des 64 cases du plateau de jeu. A son tour de jeu, le joueur
doit poser un pion de sa couleur sur une case vide, adjacente à un pion adverse
(prenant en compte les directions horizontale, verticale et diagonale) et tel qu'il
retourne au moins un pion adverse en les encadrant dans l'une ou plusieurs des directions.

La partie se termine lorsqu'aucun joueur ne peut plus poser de pion qui causerait un
retournement, ce qui arrive le plus souvent lorsque les 64 cases sont remplies, mais
ce qui peut également se produire lorsque l'un des joueurs ne possède plus de pion sur
le plateau.

Le joueur gagnant est celui qui possède le plus de pions de sa couleur sur le plateau à la
fin de la partie.

Sur le plateau de jeu, les cases vides sont symbolisées par un tiret bleu. Si cette case
représente une possibilité de jeu pour le joueur actif, celle-ci est de couleur jaune clair / blanc.
Les cases possédant un fond violet ou rouge indiquent la case dans laquelle le joueur précédent a
placé un pion.
    """, Fore.RESET)

    print(Fore.CYAN)

    # Make the user choose the game mode
    against_ai_input: str = input("Souhaitez-vous jouer contre l'ordinateur ? (oui / non) ").lower()

    # Re-ask while the input is incorrect
    while against_ai_input != "oui" and against_ai_input != "non":
        against_ai_input = input("Souhaitez-vous jouer contre l'ordinateur ? (oui / non) ").lower()

    against_ai: bool = against_ai_input == "oui"

    if against_ai:
        print("Compris ! Vous utiliserez les pions marqués avec un 'O', et l'ordinateur 'X'.")
    else:
        print("Compris ! Le joueur 1 utilisera les pions marqués avec un 'O' et le joueur 2 aura ceux avec un 'X'.")

    print(Fore.RESET)
    print(Fore.RED + "Bon jeu !" + Fore.RESET)

    # save_results("X", 41, 23)
    # show_stats("Philippe")

    input("\nAppuyez sur la touche Entrée pour commencer le jeu ! ")

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
            print(Fore.LIGHTGREEN_EX + f"Au joueur {current_player} de jouer !" + Fore.RESET)

            # Statistics about the number of pieces and the total number of pieces
            print(Fore.LIGHTBLUE_EX + 
                f"Joueur O : {nb_pieces['O']} pions ; joueur X : {nb_pieces['X']} pions\n" + Fore.RESET)

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

