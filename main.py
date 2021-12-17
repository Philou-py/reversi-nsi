from os import system, name as os_name
from colorama import init, Back, Fore

init()

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
CLEAR_CMD = 'cls' if os_name == 'nt' else 'clear'

def clear_screen():
    system(CLEAR_CMD)

def print_game(game, possible_moves = []):
    print(Fore.YELLOW + "   A   B   C   D   E   F   G   H" + Fore.RESET)
    counter = 1
    for row_index in range(8):
        print(Fore.YELLOW + str(counter) + Fore.RESET, end = "  ")
        counter += 1
        for col_index in range(8):
            square = game[row_index][col_index]
            is_possible = (row_index, col_index) in possible_moves
            color = Fore.LIGHTYELLOW_EX if is_possible else ""
            color_reset = Fore.RESET if is_possible else ""
            player_color = Fore.MAGENTA if square == "O" else (Fore.RED if square == "X" else Fore.CYAN)
            player_color_reset = Fore.RESET
            print(player_color + color + square + color_reset + player_color_reset, end = "   ")
        print("\n")

def get_input(possible_moves):
    square_coords = input("Entrez les coordonnées de la case : ").upper()
    while not (len(square_coords) == 2 and \
            square_coords[0].isalpha() and \
            "A" <= square_coords[0] <= "H" and \
            square_coords[1].isdigit() and \
            1 <= int(square_coords[1]) <= 8):
        square_coords = input("Entrez les coordonnées de la case (exemple: A4) : ").upper()
    coords = (int(square_coords[1]) - 1, ord(square_coords[0]) - ord("A"))
    if coords not in possible_moves:
        print("Vous ne pouvez pas placer un pion sur cette case !")
        return get_input(possible_moves)
    return coords

def update_coords(coords, dir):
    return (coords[0] + dir[0], coords[1] + dir[1])

def get_other_player(player_symbol):
    if player_symbol == "O": return "X"
    else: return "O"

def can_use_dir(coords, direction):
    return 0 <= coords[0] + direction[0] <= 7 and 0 <= coords[1] + direction[1] <= 7

def count_surrounding_squares(player_symbol, coords, direction, game):
    current_square = game[coords[0]][coords[1]]
    if (current_square == "-" or current_square == player_symbol) and can_use_dir(coords, direction):
        pointer = update_coords(coords, direction)
        nb_squares = 0
        while game[pointer[0]][pointer[1]] == get_other_player(player_symbol):
            nb_squares += 1
            if not can_use_dir(pointer, direction): break
            pointer = update_coords(pointer, direction)
        if game[pointer[0]][pointer[1]] == player_symbol:
            return nb_squares
    return 0

def count_pieces(game):
    count = { "O": 0, "X": 0 }
    for row in game:
        for col in row:
            if col != "-": count[col] += 1
    count["total"] = count["O"] + count["X"]
    return count

def get_possible_moves(player_symbol, game):
    possible_moves = []
    for row_index in range(8):
        for col_index in range(8):
            coords = (row_index, col_index)
            for direction in DIRECTIONS:
                if game[row_index][col_index] == "-":
                    surrounding_squares = count_surrounding_squares(player_symbol, coords, direction, game)
                    if surrounding_squares > 0:
                        possible_moves.append(coords)
                        break
    return possible_moves

def update_board(coords, player_symbol, game):
    if game[coords[0]][coords[1]] == "-": # Make sure that the square is empty
        for direction in DIRECTIONS:
            nb_squares = count_surrounding_squares(player_symbol, coords, direction, game)
            if nb_squares > 0:
                game[coords[0]][coords[1]] = player_symbol
                pointer = update_coords(coords, direction)
                for _ in range(nb_squares):
                    game[pointer[0]][pointer[1]] = player_symbol
                    pointer = update_coords(pointer, direction)

def handle_game_over(pieces_count):
    if pieces_count["O"] > pieces_count["X"]:
        print("Le joueur O a gagné !")
    elif pieces_count["X"] > pieces_count["O"]:
        print("Le joueur X a gagné !")
    else:
        print("Egalité !")

game_over = False
game = [["-" for _ in range(8)] for _ in range(8)]

game[3][3] = "O"
game[3][4] = "X"
game[4][3] = "X"
game[4][4] = "O"

current_player = "O"
while not game_over:
    clear_screen()
    possible_moves = get_possible_moves(current_player, game)
    nb_pieces = count_pieces(game)
    if nb_pieces["total"] == 64:
        game_over = True
        handle_game_over(nb_pieces)
    else:
        if len(possible_moves) == 0:
            current_player = get_other_player(current_player)
            continue
        print(f"Au joueur {current_player} de jouer !")
        print(f"Joueur O : {nb_pieces['O']} pions ; joueur X : {nb_pieces['X']} pions\n")
        print_game(game, possible_moves)
        update_board(get_input(possible_moves), current_player, game)
        current_player = get_other_player(current_player)
