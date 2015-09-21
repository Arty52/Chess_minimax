class Piece(object):

	# Piece can move in straight lines
	directionStraight = True

	# Piece can move in diagonal lines
	directionDiagonal = False

	# How many squares a piece can move per turn
	maxMovementSquares = 0

	# White or black
	color = None

	# King or Rook
	type = None

	# Is the piece still alive or dead?
	alive = True

	# Only required pieces for this assignment
	availableTypes = ['Rook', 'King']

	directionMap = {
		'Rook' : ['straight'],
		'King' : ['straight', 'diagonal']
	}

	maxMovementMap = {
		'Rook' : 0, #unlimited
		'King' : 1,
	}

	def isAlive(self):
		return self.alive

	def getType(self):
		return self.type

	def getColor(self):
		return self.color

	def isType(self, testType):
		return self.type == testType

	def isColor(self, testColor):
		return self.color == testColor

	def __init__(self, **kwargs):
		self.type = kwargs['type']
		self.color = kwargs['color']
		directions = self.directionMap[self.type]
		self.directionDiagonal = 'diagonal' in directions
		self.directionStraight = 'straight' in directions
		self.maxMovementSquares = self.maxMovementMap[self.type]

	def __str__(self):
		# if self.color == 'black':
		# 	if self.type == 'King':
		# 		return '♛ '
		# 	elif self.type == 'Rook':
		# 		return '♜ '
		# elif self.color == 'white':
		# 	if self.type == 'King':
		# 		return '♕ '
		# 	elif self.type == 'Rook':
		# 		return '♖ '
		
		# Return descriptive piece
		return self.color[0].lower() + self.type[0].upper()