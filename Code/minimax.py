from Board import Board

def heuristicWhite(board, depth, alpha, beta):
    """Returns a tuple (score, bestMove) for the position at the given depth"""
    color = 'white'

    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        print('base case white')
        return (board.evaluate(color), None)
    else:
        print('Evaluating white else...')
        bestMove = None
        best_score = 0
        for move in board.legalMoves(color):
            print('white move: {}{}'.format(move[0], move[1]))
            board.movePiece(move[0], move[1])
            if depth - 1 > 0:
                score, move = heuristicBlack(board, depth - 1, alpha, beta)
            # if score > best_score:
            bestMove = move
            # if score > alpha: # white maximizes her score
            #     alpha = score
            #     bestMove = move
                # if alpha >= beta: # alpha-beta cutoff
                #     break
        return (alpha, bestMove)

def heuristicBlack(board, depth, alpha, beta):
    """Returns a tuple (score, bestMove) for the position at the given depth"""
    color = 'black'

    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        print('base case black')
        return (board.evaluate(color), None)
    else:
        print('Evaluating black else...')
        bestMove = None
        best_score = 0
        for move in board.legalMoves(color):
            print('black move: {}{}'.format(move[0], move[1]))
            board.movePiece(move[0], move[1])
            if depth - 1 > 0:
                score, move = heuristicWhite(board, depth - 1, alpha, beta)

            bestMove = move
            # if score < beta: # black minimizes his score
            #     beta = score
            #     bestMove = move
                # if alpha >= beta: # alpha-beta cutoff
                #     break
        return (beta, bestMove)