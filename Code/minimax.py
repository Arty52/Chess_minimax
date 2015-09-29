from Board import Board

def minimax(board):
    depth = 3
    color = 'white'
    moves = board.legalMoves(color)
    best_move = moves[0]
    best_score = float('-inf')
    for move in moves:
        print(board)
        clone = board
        clone.movePiece(move[0], move[1])
        print(move[0], move[1])
        print(clone)
        score = min_play(clone, depth - 1)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

def min_play(board, depth):
    color = 'black'
    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('inf')
    for move in moves:
        clone = board.movePiece(move[0], move[1])
        score = max_play(clone, depth - 1)
        if score < best_score:
            best_move = move
            best_score = score
    return best_score

def max_play(board, depth):
    color = 'white'
    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('-inf')
    for move in moves:
        clone = board.movePiece(move[0], move[1])
        score = min_play(clone, depth - 1)
        if score > best_score:
            best_move = move
            best_score = score
    return best_score



# def heuristicWhite(board, depth, alpha, beta):
#     """Returns a tuple (score, bestMove) for the position at the given depth"""
#     color = 'white'
#
#     if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
#         print('base case white')
#         return (board.evaluate(color), None)
#     else:
#         print('Evaluating white else...')
#         bestMove = None
#         best_score = 0
#         for move in board.legalMoves(color):
#             print('white move: {}{}'.format(move[0], move[1]))
#             board.movePiece(move[0], move[1])
#             score, move = heuristicBlack(board, depth - 1, alpha, beta)
#             if not move:
#                 move = move[1]
#             if score > alpha: # white maximizes her score
#                 alpha = score
#                 bestMove = move
#                 if alpha >= beta: # alpha-beta cutoff
#                     break
#         return (alpha, bestMove)
#
# def heuristicBlack(board, depth, alpha, beta):
#     """Returns a tuple (score, bestMove) for the position at the given depth"""
#     color = 'black'
#
#     if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
#         print('base case black')
#         return (board.evaluate(color), None)
#     else:
#         print('Evaluating black else...')
#         bestMove = None
#         best_score = 0
#         for move in board.legalMoves(color):
#             print('black move: {}{}'.format(move[0], move[1]))
#             board.movePiece(move[0], move[1])
#             score, move = heuristicWhite(board, depth - 1, alpha, beta)
#             if not move:
#                 move = move[1]
#             if score < beta: # black minimizes his score
#                 beta = score
#                 bestMove = move
#                 if alpha >= beta: # alpha-beta cutoff
#                     break
#         return (beta, bestMove)