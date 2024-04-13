import chess.svg
import chess.pgn
import chess.engine
import time
import requests
import json

board = chess.Board()
bot_token = "lip_aO2neoPU45kTorbEbWX9"
movehistory =[]
totalnumberof = {}
pieceValues = {
    'P': 100,
    'N': 320,
    'B': 330,
    'R': 500,
    'Q': 900,
    'K': 20000
}

#Matrices for piece-square tables NOT MY VALUES - from: https://www.chessprogramming.org/Simplified_Evaluation_Function
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

def calculate_Score():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    #Total number of white and black pieces e.g wPawns = white pawns, bPawns = black pawns etc. Stored in a dictionary incase I need to use them later
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

    #calculation I have used for material is based on the standard piece value NOT MY FORMULA
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
    except Exception as e:
        print(f"An error occurred: {e}")
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
    except Exception as e:
        print(f"An error occurred: {e}")
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
                print("Failed to connect. Check your game ID and bot token.")
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
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

def alpha_beta_Pruning(alpha, beta, depthleft):
    # Initialize the best score as a very low value
    bestscore = -9999

    # If the depth limit is reached, return the result of quiescence search
    if depthleft == 0:
        return quiescence_Search(alpha, beta)

    # Iterate through all legal moves
    for move in board.legal_moves:
        # Make the move on the board
        board.push(move)
        
        # Recursively call alpha_beta_Pruning with updated alpha, beta, and reduced depth
        score = -alpha_beta_Pruning(-beta, -alpha, depthleft - 1)
        
        # Undo the move
        board.pop()
        
        # If the score is greater than or equal to beta, cutoff and return score
        if score >= beta:
            return score
        
        # Update the best score if the current score is better
        if score > bestscore:
            bestscore = score
        
        # Update alpha if the current score is better than alpha
        if score > alpha:
            alpha = score
    
    # Return the best score found in this branch
    return bestscore

def quiescence_Search(alpha, beta):
    # Calculate the static evaluation score of the current position
    pat = calculate_Score()
    
    # If the static evaluation score is greater than or equal to beta, return beta
    if pat >= beta:
        return beta
    
    # Update alpha if the static evaluation score is greater than alpha
    if alpha < pat:
        alpha = pat

    # Iterate through all legal moves
    for move in board.legal_moves:
        # Only consider capture moves
        if board.is_capture(move):
            # Make the move on the board
            board.push(move)
            
            # Recursively call quiescence_Search with updated alpha and beta
            score = -quiescence_Search(-beta, -alpha)
            
            # Undo the move
            board.pop()

            # If the score is greater than or equal to beta, return beta
            if score >= beta:
                return beta
            
            # Update alpha if the current score is greater than alpha
            if score > alpha:
                alpha = score
    
    # Return the updated alpha value
    return alpha


def find_best_move(depth): #Function to find the best move with a given depth
    bestMove = chess.Move.null()
    bestValue = -100000
    
    # Initialize alpha and beta values for alpha-beta pruning
    alpha = -100000
    beta = 100000
    
    # Iterate through all legal moves
    for move in board.legal_moves:
        # Make the move on the board
        board.push(move)
        
        # Call alpha_beta_Pruning to evaluate the board after the move
        boardValue = -alpha_beta_Pruning(-beta, -alpha, depth-1)
        
        # Update the best move and value if the current move yields a better value
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move
        
        # Update alpha if the current value is greater than alpha
        if boardValue > alpha:
            alpha = boardValue
        
        # Undo the move
        board.pop()
    
    # Append the best move to the move history and return it
    movehistory.append(bestMove)
    return bestMove

def whatcolour(game_data, username):
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

def get_value(string):
    try:
        return [value[string] for value in get_masters(bot_token)['moves']]
    except:
        print("Couldn't find any games with specified string: {string}")
        return None

def merge_sort(output_list):
    if len(output_list) <= 1:
        return output_list
    
    mid = len(output_list) // 2
    left_half = output_list[:mid]
    right_half = output_list[mid:]
    
    merge_sort(left_half)
    merge_sort(right_half)
    
    i = 0
    j = 0
    k = 0
    
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            output_list[k] = left_half[i]
            i += 1
        else:
            output_list[k] = right_half[j]
            j += 1
        k += 1
    
    while i < len(left_half):
        output_list[k] = left_half[i]
        i += 1
        k += 1
    
    while j < len(right_half):
        output_list[k] = right_half[j]
        j += 1
        k += 1
    
    return output_list

def openingmove(colour):
    white_values = get_value("white")
    black_values = get_value("black")
    moves = get_value("uci")
    ratios = [white / black for white, black in zip(white_values, black_values)]
    sortedratios = merge_sort(ratios)
    map = {}
    for move, ratio in zip(moves, ratios):
        map[ratio] = move

    if colour == "white":
        return map[sortedratios[-1]]
    if colour == "black":
        return map[sortedratios[0]]
    print("Invalid colour")
    return None


def play_as_white():
    move = find_best_move(int(depth))
    board.push(move)
    play_move(game_id, str(move), bot_token)
    time.sleep(3)
    x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    while(x == len(movehistory)):
        time.sleep(5)
        x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    opponents_move = (read_game_state(game_id, bot_token)['state']['moves'].split(" ")[-1])
    board.push_san(opponents_move)
    movehistory.append(opponents_move)
    return(board)

def play_as_black():
    x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    while(x == len(movehistory)):
        time.sleep(5)
        x = len(read_game_state(game_id, bot_token)['state']['moves'].split(" "))
    opponents_move = (read_game_state(game_id, bot_token)['state']['moves'].split(" ")[-1])
    board.push_san(opponents_move)
    movehistory.append(opponents_move)
    move = find_best_move(int(depth))
    board.push(move)
    play_move(game_id, str(move), bot_token)
    time.sleep(3)
    return(board)

def play(colour):
    if colour == "white":
        return play_as_white()
    else:
        return play_as_black()


try:
    depth = int(input("Welcome to Dillon Rahman's NEA.\nA chess engine written in Python. \nPlease enter the depth that will be used for the engine:\nReccomended depth: 3\n"))
    if depth < 1:
        print("Please enter a depth greater than 0.")
        exit()
    option = input("AI vs AI? (1): \nAI vs User? (2):  \nLichess(3) \nLoad Position? (4):")
    if option == "1":
        board = chess.Board()
        while not board.is_game_over(claim_draw=True):
            if board.turn:
                move = find_best_move(int(depth))
                movehistory.append(move)
                board.push(move)
                print("\n" + str(move) + "\n")
            else:
                move = find_best_move(int(depth))
                movehistory.append(move)
                board.push(move)
                print("\n" + str(move) + "\n")
            print(board)
        if board.is_checkmate():
            print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
        elif board.is_stalemate():
            print("Stalemate in " + str(len(movehistory)) + " moves.")
        print(movehistory)
    if option == "2":
        board = chess.Board()
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
            print(board)
        if board.is_checkmate():
            print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
        elif board.is_stalemate():
            print("Stalemate in " + str(len(movehistory)) + " moves.")
        print(movehistory)
    elif option == "3":
        game_id = input("Enter game ID: ")
        board = chess.Board()
        try:
            colour = whatcolour(read_game_state(game_id, bot_token), "dillonnea")
            if len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")) > 1:
                print("Game has already started. Please try another game ID")
                exit()
            while not board.is_game_over(claim_draw=True):
                board = play(colour)
            if(read_game_state(game_id, bot_token)['state']['status'] == "draw"):
                print(str(read_game_state(game_id, bot_token)['state']['status']) + " in " + str(len(movehistory)) + " moves.")
            else:
                winner = read_game_state(game_id, bot_token)['state']['winner']
                print("Checkmate by " + str(winner) + "in " + str(len(movehistory)) + " moves.")
        except:
            exit()
    elif option == "4":
        fen_string = input("Enter FEN string: ")
        board = chess.Board()
        if load_Fen(fen_string):
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
    elif option == "5":
        print(openingmove("white"))
        print(openingmove("black"))
    else:
        print("Invalid option.")
except ValueError:
    print("Please enter an integer.")

            
