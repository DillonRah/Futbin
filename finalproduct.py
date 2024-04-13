import chess
import time
import requests
import json
import unittest
import chess.engine

movehistory =[]
totalnumberof = {}
pieceValues = {
    'P': 0.71,
    'N': 2.93,
    'B': 3.00,
    'R': 4.56,
    'Q': 9.05,
    'K': 100
}

#https://www.reddit.com/r/chess/comments/e57lqz/stockfish_doesnt_use_the_traditional_piece_values/

def get_token(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

class PieceSquareTable:
    def __init__(self, values):
        if len(values) != 64:
            raise ValueError("Invalid number of values for piece square table")
            #validates that the inputed PSQ is an 8x8 table
        self.values = values

    def __getitem__(self, square):
        if not 0 <= square < 64:    
            raise ValueError("Square index out of range")
        return self.values[square]

board = chess.Board()
# Define your piece square table
pawnsPSQ = PieceSquareTable([
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0])

knightsPSQ = PieceSquareTable([
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,])
bishopsPSQ = PieceSquareTable([
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,])
rooksPSQ = PieceSquareTable([
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0])
queensPSQ = PieceSquareTable([
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20])
kingsPSQ = PieceSquareTable([
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20])

test_data = [
    {
        "depth": 1,
        "nodes": 8,
        "fen": "r6r/1b2k1bq/8/8/7B/8/8/R3K2R b KQ - 3 2",
        "solution": "e7f7"
    },
    {
        "depth": 1,
        "nodes": 8,
        "fen": "8/8/8/2k5/2pP4/8/B7/4K3 b - d3 0 3",
        "solution": "c4d3"
    },
    {
        "depth": 1,
        "nodes": 19,
        "fen": "r1bqkbnr/pppppppp/n7/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 2 2",
        "solution": "g1f3"
    },
    {
        "depth": 1,
        "nodes": 5,
        "fen": "r3k2r/p1pp1pb1/bn2Qnp1/2qPN3/1p2P3/2N5/PPPBBPPP/R3K2R b KQkq - 3 2",
        "solution": "f7e6"
    },
    {
        "depth": 1,
        "nodes": 44,
        "fen": "2kr3r/p1ppqpb1/bn2Qnp1/3PN3/1p2P3/2N5/PPPBBPPP/R3K2R b KQ - 3 2",
        "solution": "h8h2"
    },
    {
        "depth": 1,
        "nodes": 39,
        "fen": "rnb2k1r/pp1Pbppp/2p5/q7/2B5/8/PPPQNnPP/RNB1K2R w KQ - 3 9",
        "solution": "d7d8r"
    },
    {
        "depth": 1,
        "nodes": 9,
        "fen": "2r5/3pk3/8/2P5/8/2K5/8/8 w - - 5 4",
        "solution": "c3c4"
    },
    {
        "depth": 3,
        "nodes": 62379,
        "fen": "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
        "solution": "b1c3"
    },
    {
        "depth": 3,
        "nodes": 89890,
        "fen": "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
        "solution": "c4f7"
    },
    {
        "depth": 6,
        "nodes": 1134888,
        "fen": "3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1",
        "solution": "d8c7"
    }
]

def calculate_score(board):
    if board.is_checkmate():
        if board.turn:
            return float('-inf')
        else:
            return float('inf')
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    #Total number of white and black pieces e.g wPawns = white pawns, bPawns = black pawns etc. 
    #Stored in a dictionary incase I need to use them later
    totalnumberof['wPawns'] = len(board.pieces(chess.PAWN, chess.WHITE))
    totalnumberof['bPawns'] = len(board.pieces(chess.PAWN, chess.BLACK))
    totalnumberof['wKnights'] = len(board.pieces(chess.KNIGHT, chess.WHITE))
    totalnumberof['bKnights'] = len(board.pieces(chess.KNIGHT, chess.BLACK))
    totalnumberof['wBishops'] = len(board.pieces(chess.BISHOP, chess.WHITE))
    totalnumberof['bBishops'] = len(board.pieces(chess.BISHOP, chess.BLACK))
    totalnumberof['wRooks'] = len(board.pieces(chess.ROOK, chess.WHITE))
    totalnumberof['bRooks'] = len(board.pieces(chess.ROOK, chess.BLACK))
    totalnumberof['wQueens'] = len(board.pieces(chess.QUEEN, chess.WHITE))
    totalnumberof['bQueens'] = len(board.pieces(chess.QUEEN, chess.BLACK))

    total_material_Value = pieceValues['P'] * (totalnumberof['wPawns'] - totalnumberof['bPawns']) + pieceValues['N'] * (totalnumberof['wKnights']  - totalnumberof['bKnights']) + pieceValues['B'] * (totalnumberof['wBishops'] - totalnumberof['bBishops']) + pieceValues['R'] * (totalnumberof['wRooks'] - totalnumberof['bRooks']) + pieceValues['Q'] * (totalnumberof['wQueens'] - totalnumberof['bQueens'])
    #Calculating the value of all of the white patwKnightss (Sum each available white patwKnights and its positonal value)
    pawns_Score = sum([pawnsPSQ[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) 
    #Chess is a zero sum game, therefore take away the value of all of the black pawns because you are calculating the score from white's perspective.
    #Mirror the board to calculate the black pawns positional value as it's the same as the white pawns but from the other side of the board. 
    pawns_Score += sum([-pawnsPSQ[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    #The same for the knights, bishops, rooks, queens and kings
    knights_Score = sum([knightsPSQ[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knights_Score += sum([-knightsPSQ[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishops_Score= sum([bishopsPSQ[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishops_Score+= sum([-bishopsPSQ[chess.square_mirror(i)]for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooks_Score = sum([rooksPSQ[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooks_Score += sum([-rooksPSQ[chess.square_mirror(i)]for i in board.pieces(chess.ROOK, chess.BLACK)])
    queens_Score = sum([queensPSQ[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queens_Score += sum([-queensPSQ[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kings_Score = sum([kingsPSQ[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kings_Score += sum([-kingsPSQ[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    total_Score = total_material_Value + pawns_Score + knights_Score + bishops_Score+ rooks_Score + queens_Score + kings_Score #Evaluate the position based on the sum of al of the pieces (kinda self explanatory)
    if board.turn:
        return total_Score #If it's White's turn return the evaluation
    else:
        return -total_Score #Otherwise return the negative (Black's turn)

def load_Fen(FEN):
    try:
        board.set_fen(FEN)
        print("FEN string loaded successfully.\nInitial position:")
        return True
    except ValueError:
        print("Invalid FEN string.")
        return False
    
def read_game_state(game_id, bot_token):
    url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    headers = {"Authorization": f"Bearer {bot_token}"}

    try:
        with requests.get(url, headers=headers, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        game_state = json.loads(line.decode('utf-8'))
                        return game_state
            else:
                print("Failed to connect. Check your game ID and bot token.")
                return None
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def play_move(game_id, move, bot_token):
    url = f"https://lichess.org/api/bot/game/{game_id}/move/{move}"
    headers = {"Authorization": f"Bearer {bot_token}"}

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("Move successfully played.")
            return True
        else:
            print("Failed to play move.")
            return False
    except Exception as error:
        print(f"An error occurred: {error}")
        return False
    
def get_masters(bot_token):
    url = f"https://explorer.lichess.ovh/masters"
    headers = {"Authorization": f"Bearer {bot_token}"}

    try:
        with requests.get(url, headers=headers, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        game_state = json.loads(line.decode('utf-8'))
                        return game_state
            else:
                print("Failed to connect please check your token.")
                return None
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def find_black_info(game_data):
    if 'black' in game_data:
        return game_data['black']
    else:
        return None

def find_white_info(game_data):
    if 'white' in game_data:
        return game_data['white']
    else:
        return None
    
def get_last_move_from_lichess(game_id):
    lichess_api_url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    response = requests.get(lichess_api_url)
    if response.status_code == 200:
        moves = response.text.split()
        if len(moves) > 0:
            return moves[-1]
    return None

def play_last_move_on_board(game_id):
    last_move = get_last_move_from_lichess(game_id)
    if last_move:
        board = chess.Board()
        for move in last_move.split():
            board.push_san(move)
        print("Last move played:", last_move)
        print(board)
        return board
    else:
        print("Failed to retrieve last move.")
        return None

def alpha_beta_pruning(alpha, beta, depth, board):
    # When the depth is 0, we run the quiescsence search which goes deeper into the earch to find the best move
    best_score = float('-inf')
    if depth == 0:
        return quiescence_search(alpha, beta, board)
    
    # Checking all of the legal moves
    total_legal_moves = board.legal_moves
    for move in total_legal_moves:
        board.push(move)
        value = -alpha_beta_pruning(-beta, -alpha, depth - 1)
        board.pop()
        best_score = max(best_score, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            return beta  
    return best_score

def quiescence_search(alpha, beta, board):
    pat = calculate_score()
    if pat >= beta:
        return beta
    if alpha < pat:
        alpha = pat
    
    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]
    for move in capture_moves: #checking all of the capture moves as they are the most 'dangerous'
        board.push(move)
        value = -quiescence_search(-beta, -alpha, board)
        board.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            return beta  # Beta cut-off
    return alpha

def find_best_move(depth, board):
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    best_move = None
    
    #Check through all legal moves
    legal_moves = board.legal_moves
    for move in legal_moves:
        board.push(move)
        board_value = -alpha_beta_pruning(-beta, -alpha, depth - 1, board)
        if board_value > best_score:
            best_score = board_value
            best_move = move
        alpha = max(alpha, board_value)
        board.pop()
    movehistory.append(best_move)
    return best_move

def what_colour(game_data, username):
    if 'black' in game_data:
        black = game_data['black']
        white = game_data['white']
        try:
            if black['id'] == username:
                return "black"
        except:    
            if white['id'] == username:
                return "white"
    return "Not in game"

def get_value(string, bot_token):
    try:
        return [value[string] for value in get_masters(bot_token)['moves']]
    except:
        print("Couldn't find any games with specified string: {string}")
        return None

def merge_sort(listA):
    #base case if its a single element, return the list
    if len(listA) <= 1:
        return listA

    
    #split the list into two halves
    mid = len(listA) // 2
    left_half = listA[:mid]
    right_half = listA[mid:]
    
    #recursive call to apply mergesort again
    #this will continue until the two lists are of length 1
    merge_sort(left_half)
    merge_sort(right_half)
    
    i = 0
    j = 0
    k = 0
    
    #merge the two lists back together by comparing the elements
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            listA[k] = left_half[i]
            i += 1
        else:
            listA[k] = right_half[j]
            j += 1
        k += 1
    
    while i < len(left_half):
        listA[k] = left_half[i]
        i += 1
        k += 1
    
    while j < len(right_half):
        listA[k] = right_half[j]
        j += 1
        k += 1
    
    #return the sorted list
    return listA

def opening_move(colour, bot_token):
    # Assuming get_value() function returns white_values, black_values, and moves properly
    white_values = get_value("white", bot_token)
    black_values = get_value("black", bot_token)
    moves = get_value("uci", bot_token)
    
    ratios = [white / black for white, black in zip(white_values, black_values)]
    sorted_ratios = merge_sort(ratios)
    
    move_map = {}
    for move, ratio in zip(moves, ratios):
        move_map[ratio] = move

    if colour == "white":
        return move_map[sorted_ratios[-1]]
    elif colour == "black":
        return move_map[sorted_ratios[0]]
    else:
        print("Invalid colour:", colour)
        return None


def play_as_white(game_id, bot_token, depth, board):
    if(len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")) == 0):
        move = opening_move("white", bot_token)
        board.push_san(move)
        play_move(game_id, str(move), bot_token)
        time.sleep(1)
        movehistory.append(move)
        return(board)
    move = find_best_move(int(depth), board)
    board.push(move)
    play_move(game_id, str(move), bot_token)
    time.sleep(1)
    x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    while(x == len(movehistory)):
        time.sleep(2)
        x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    opponents_move = (read_game_state(game_id, bot_token)['state']['moves'].split(" ")[-1])
    board.push_san(opponents_move)
    movehistory.append(opponents_move)
    return(board)

def play_as_black(game_id, bot_token, depth, board):
    if(len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")) == 1):
        move = opening_move("black", bot_token)
        board.push_san(move)
        play_move(game_id, str(move), bot_token)
        time.sleep(1)
        movehistory.append(move)
        return(board)
    x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    while(x == len(movehistory)):
        time.sleep(5)
        x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    opponents_move = (read_game_state(game_id, bot_token)['state']['moves'].split(" ")[-1])
    board.push_san(opponents_move)
    movehistory.append(opponents_move)
    move = find_best_move(int(depth), board)
    board.push(move)
    play_move(game_id, str(move), bot_token)
    time.sleep(3)
    return(board)

def play(colour, game_id, bot_token, depth, board):
    if colour == "white":
        return play_as_white(game_id, bot_token, depth, board)
    else:
        return play_as_black(game_id, bot_token, depth,board)


class test_merge_sort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_sorted_list(self):
        sorted_list = [11, 24, 35, 36, 55]
        self.assertEqual(merge_sort(sorted_list), sorted_list)

    def test_reverse_sorted_list(self):
        reverse_sorted_list = [55, 36, 35, 24, 11]
        self.assertEqual(merge_sort(reverse_sorted_list), [11, 24, 35, 36, 55])

    def test_random_list(self):
        random_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.assertEqual(merge_sort(random_list), [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9])

class test_calculate_score(unittest.TestCase):
    def test_starting_position(self):
        board = chess.Board()
        self.assertEqual(calculate_score(), 0)

class test_find_best_move(unittest.TestCase):
    def not_null(self):
        # Create a basic board position
        board = chess.Board(fen='rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2')

        # Test the find_best_move function
        best_move = find_best_move(3)
        
        # Assert that the best move is not None
        self.assertIsNotNone(best_move)

        # Assert that the best move is a valid move
        self.assertIn(best_move, board.legal_moves)
    

    def set_positions(self):
        for position in test_data:
            board.set_fen(position['fen'])
            best_move = find_best_move(position['depth'])
            self.assertEqual(str(best_move), position['solution'])

def main(board):
    bot_token = get_token("tokens.txt")
    try:
        depth = int(input("Welcome to Dillon Rahman's NEA.\nA chess engine written in Python. \nPlease enter the depth that will be used for the engine:\nReccomended depth: 3\n"))
        if depth < 1:
            print("Please enter a depth greater than 0.")
            exit()
        option = input("AI vs AI? (1): \nAI vs Human? (2):  \nLichess(3) \nLoad Position? (4):")
        if option == "2":
            while not board.is_game_over(claim_draw=True):
                if board.turn:
                    move = find_best_move(int(depth))
                    movehistory.append(move)
                    board.push(move)
                    print("\n" + str(move) + "\n")
                else:
                    move = input("\nEnter your move: ")
                    move = board.push_san(move)
                    movehistory.append(move)
                    print("")
                    #move = find_best_move(int(depth))
                print(board)
            print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
            print(movehistory)
        elif option == "3":
            username = input("Enter your username: ")
            game_id = input("Enter game ID: ")
            colour = what_colour(read_game_state(game_id, bot_token), username)
            if len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")) > 1:
                print("Game has already started. Please try another game ID")
                exit()
            while not board.is_game_over(claim_draw=True):
                board = play(colour, game_id, bot_token, depth, board)
            if(read_game_state(game_id, bot_token)['state']['status'] == "draw"):
                print("Draw by " + str(read_game_state(game_id, bot_token)['state']['status']) + "in " + str(len(movehistory)) + " moves.")
            else:
                winner = read_game_state(game_id, bot_token)['state']['winner']
                print("Checkmate by " + str(winner) + "in " + str(len(movehistory)) + " moves.")
        elif option == "4":
            fen_string = input("Enter FEN string: ")
            board = chess.Board()
            try: 
                load_Fen(fen_string)
                print(board)
                while not board.is_game_over(claim_draw=True):
                    if board.turn:
                        move = find_best_move(int(depth))
                        movehistory.append(move)
                        board.push(move)
                        print("\n" + str(move) + "\n")
                    else:
                        move = input("\nEnter your move: ")
                        move = board.push_san(move)
                        movehistory.append(move)
                        print("")
                    print(board)
                print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
                print(movehistory)
            except:
                print("Invalid FEN string.")
        else:
            print("Invalid option.")
    except ValueError:
        print("Please enter an integer.")

if __name__ == "__main__":
    unittest.main()
    main(board)

