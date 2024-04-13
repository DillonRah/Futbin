import chess
import unittest
import chess.engine


# Now, you can use this engine to analyze positions up to depth 1

# For example:
path = "C:\\Users\cheek\\Documents\\stockfish\\stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(path)
board = chess.Board("8/8/4k3/8/2p5/8/B2P2K1/8 w - - 0 1")

# Limit the depth of the engine's search
limit = chess.engine.Limit(depth=6)  # Set the depth limit to 5 plies

analysis = engine.analyse(board, limit)

# Check available keys in the analysis object
print(analysis['pv'])


# Close the engine when done
engine.quit()

totalnumberof = {}
pieceValues = {
    'P': 0.71,
    'N': 2.93,
    'B': 3.00,
    'R': 4.56,
    'Q': 9.05,
    'K': 100
}

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
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,])

knightsPSQ = PieceSquareTable([
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,])
bishopsPSQ = PieceSquareTable([
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,])
rooksPSQ = PieceSquareTable([
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,])
queensPSQ = PieceSquareTable([
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50])
kingsPSQ = PieceSquareTable([
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14])

class TestAlphaBetaPruning(unittest.TestCase):
    def test_alpha_beta_pruning(self):
        alpha = -float('inf')
        beta = float('inf')
        move = alpha_beta_pruning(alpha, beta, 3)
        self.assertEqual(move, "")

def calculate_score():
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
    
def alpha_beta_pruning(alpha, beta, depth):
    # When the depth is 0, we run the quiescsence search which goes deeper into the earch to find the best move
    best_score = float('-inf')
    if depth == 0:
        return quiescence_search(alpha, beta)
    
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


def quiescence_search(alpha, beta):
    pat = calculate_score()
    if pat >= beta:
        return beta
    if alpha < pat:
        alpha = pat
    
    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]
    for move in capture_moves: #checking all of the capture moves as they are the most 'dangerous'
        board.push(move)
        score = -quiescence_search(-beta, -alpha)
        board.pop()
        alpha = max(alpha, score)
        if alpha >= beta:
            return beta  # Beta cut-off
    return alpha


def find_best_move(depth): #Function to find the best move with a given depth
    bestMove = None
    current_best_Score = float('-inf')
    
    # Initialize alpha and beta values for alpha-beta pruning
    alpha = float('-inf')
    beta = float('inf')
    
    # Iterate through all legal moves
    total_legal_moves = board.legal_moves
    for move in total_legal_moves   :
        # Make the move on the board
        board.push(move)
        
        # evaluate the position by applying the alpha beta pruning algortithm
        boardValue = -alpha_beta_pruning(-beta, -alpha, depth-1)
        
        # Update the best move and value if the current move yields a better value
        if boardValue > current_best_Score:
            current_best_Score = boardValue
            bestMove = move
        
        # Update alpha if the current value is greater than alpha
        if boardValue > alpha:
            alpha = boardValue
        
        # Undo the move
        board.pop()
    
    # Append the best move to the move history and return it
    return bestMove

print(find_best_move(6))