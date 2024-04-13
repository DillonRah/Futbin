import chess.svg
import chess.pgn
import chess.engine

board = chess.Board()
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
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0])

knightsPSQ = PieceSquareTable([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50])
bishopsPSQ = PieceSquareTable([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20])
rooksPSQ = PieceSquareTable([
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0])
queensPSQ = PieceSquareTable([
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20])
kingsPSQ = PieceSquareTable([
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30])

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
    
def alpha_beta_Pruning(alpha, beta, depthleft):
    if depthleft == 0:
        return quiescence_Search(alpha, beta)
    best_score = float('-inf')
    for move in board.legal_moves:
        score = -alpha_beta_Pruning(-beta, -alpha, depthleft - 1)

        board.pop()
        alpha = max(alpha, score)
    
        if alpha >= beta:
            return alpha
        best_score = max(best_score, score)
    return best_score


def quiescence_Search(alpha, beta):
    pat = calculate_Score()
    alpha = max(alpha, pat)
    if pat >= beta:
        return beta
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_Search(-beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            alpha = max(alpha, score)
    return alpha



def find_best_Move(depth): 
    best_move = chess.Move.null()
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = -alpha_beta_Pruning(-beta, -alpha, depth - 1)
        if board_value > best_value:
            best_value = board_value
            best_move = move
    
        alpha = max(alpha, board_value)
        board.pop()
    movehistory.append(best_move)
    return best_move


def load_Fen(FEN):
    try:
        board.set_fen(FEN)
        print("FEN string loaded successfully.\nInitial position:")
        return True
    except ValueError:
        print("Invalid FEN string.")
        return False
        
depth = input("Welcome to Dillon Rahman's NEA.\nA chess engine written in Python. \nPlease enter the depth that will be used for the engine: ")
option = input("AI vs AI? (1): \nAI vs Human? (2): \nLoad Position? (3):")
match option:
    case "1":
        while not board.is_game_over(claim_draw=True):
            move = find_best_Move(int(depth))
            movehistory.append(move)
            print("\n" + str(move) + "\n")
            board.push(move)
            print(board)
        print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
        print(movehistory)
    case "2":
        while not board.is_game_over(claim_draw=True):
            if board.turn:
                move = find_best_Move(int(depth))
                movehistory.append(move)
                board.push(move)
                print("\n" + str(move) + "\n")
            else:
                move = input("\nEnter your move: ")
                move = board.push_san(move)
                movehistory.append(move)
                print("")
                #move = findbest_Move(int(depth))
            print(board)
        print("Checkmate by " + str(board.result()) + "in " + str(len(movehistory)) + " moves.")
        print(movehistory)
    case "3":
        fen_string = input("Enter FEN string: ")
        board = chess.Board()
        if load_Fen(fen_string):
            print(board)
            while not board.is_game_over(claim_draw=True):
                if board.turn:
                    move = find_best_Move(int(depth))
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
