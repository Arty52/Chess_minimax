# from Board import Board
# from Square import Square

class Game(object):

	# def heuristicX(int alpha, int beta, int depthLeft):
	# 	if depthLeft == 0:
	# 		return Game.evaluate()


	def alphabeta(position, depth, alpha, beta):
		"""Returns a tuple (score, bestmove) for the position at the given depth"""
		if depth == 0 or position.is_checkmate() or position.is_draw():
			return (position.evaluate(), None)
		else: 
			if position.to_move == "white":
				bestmove = None
				for move in position.legal_moves():
					new_position = position.make_move(move)
					score, move = alphabeta(new_position, depth - 1, alpha, beta)
					if score > alpha: # white maximizes her score
						alpha = score
						bestmove = move
						if alpha >= beta: # alpha-beta cutoff
							break
				return (alpha, bestmove)
			else:
				bestmove = None
				for move in position.legal_moves():
					new_position = position.make_move(move)
					score, move = alphabeta(new_position, depth - 1, alpha, beta)
					if score < beta: # black minimizes his score
						beta = score
						bestmove = move
						if alpha >= beta: # alpha-beta cutoff
							break
				return (beta, bestmove)