class Position:

	piece      = None
	fromSquare = None
	toSquare   = None
	
	def __init__(self, frm, to):
		self.piece      = s.piece
		self.fromSquare = frm
		self.toSquare   = to

	def evaluate():
		pass

	def isCheckmate(self, board):
		if self.piece.getColor() == 'white':
			otherKingSquare = board.getPieceSquare('black', 'King')
		else:
			otherKingSquare = board.getPieceSquare('white', 'King')

		thisPiecesMoves = self.fromSquare.getMoves()

		# In check
		if self.toSquare == otherKingSquare:
			otherKingsMoves = otherKingSquare.getMoves()

	def isStalemate(self):
		pass

