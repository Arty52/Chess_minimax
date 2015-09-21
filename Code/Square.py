from string import ascii_uppercase

class Square(object):

	MAX_ROW_BOUND = 7
	MAX_COL_BOUND = 7
	MIN_ROW_BOUND = 0
	MIN_COL_BOUND = 0

	row = 0
	column = 0
	occupied = False
	Piece = None

	def __init__(self, *args, **kwargs):
		if len(args) == 2:
			self.row = args[0]
			self.column = args[1]
		else:
			positionParts = Square.parsePosition(args[0])
			self.row = positionParts['row']
			self.column = positionParts['col']

	def getRow(self):
		return self.row

	def getColumn(self):
		return self.column

	def isOccupied(self):
		return self.occupied

	def removePiece(self):
		self.occupied = False

		self.Piece = None

	def assignPiece(self, piece):
		if piece is None:
			self.occupied = False
		else:
			self.occupied = True

		self.Piece = piece

	def getPiece(self):
		'''
		@return: Piece
		'''
		return self.Piece

	def generateMoves(self):

		moves = []

		if self.Piece.type == 'Rook':
			# Straight Moves
			for i in range(self.MAX_ROW_BOUND):
				if i is not self.row:
					moves.append(Square(i, self.column))

			for i in range(self.MAX_COL_BOUND):
				if i is not self.column:
					moves.append(Square(self.row, i))

		elif self.Piece.type == 'King':
			##
			# Add moves below...
			##

			# Make sure we're still in bounds
			if self.row - 1 >= self.MIN_ROW_BOUND:

				newRow = self.row - 1
				
				for i in range(self.column - 1, self.column + 2):
					if i >= self.MIN_COL_BOUND and i <= self.MAX_COL_BOUND:
						moves.append(Square(newRow, i))

			##
			# Add moves in same row...
			##
			for i in range(self.column - 1, self.column + 2):
				if i >= self.MIN_COL_BOUND and i <= self.MAX_COL_BOUND and i is not self.column:
					moves.append(Square(self.row, i))

			##
			# Add moves above...
			##
			if self.row + 1 <= self.MAX_ROW_BOUND:

				newRow = self.row + 1
				
				for i in range(self.column - 1, self.column + 2):
					if i >= self.MIN_COL_BOUND and i <= self.MAX_COL_BOUND:
						moves.append(Square(newRow, i))

		return moves

	@staticmethod
	def columnIndex(column):
		try:
			column = int(column) - 1
		except:
			column = ascii_uppercase.index(column)

		return column

	@staticmethod
	def indexColumn(column):
		return ascii_uppercase[column]

	@staticmethod
	def position(row, column):
		return ascii_uppercase[int(column)] + str(int(row) + 1)

	@staticmethod
	def parsePosition(positionDescription):
		if len(positionDescription) is not 2:
			raise Exception('Invalid position specified')

		col = positionDescription[0]
		row = positionDescription[1]

		# Return 0 based location of the piece
		return {
			'col': ("A", "B", "C", "D", "E", "F", "G", "H").index(col),
			'row': int(row) - 1
		}

	# Compare if two Square objects are equal (same location)
	def __eq__(self, otherSquare):
		return self.row == otherSquare.row and self.column == otherSquare.column

	def __str__(self):
		if self.Piece is None:
			piece = ""
		else:
			piece = str(self.Piece)

		properties = {
			'piece'  : piece,
			'row'    : self.row + 1,
			'column' : ascii_uppercase[self.column],
		}

		return '%(piece)s(%(column)s%(row)d)' % properties