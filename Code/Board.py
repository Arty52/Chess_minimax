import sys
from Heuristic import Heuristic
from string import ascii_uppercase

'''
===================================================================================
Board Class:
-Initializes an empty board state
-Adds all the pieces into the correct spots
-Displays the Board
-Can tell us all possible moves
-Can tell if the board state is in checkmate
-Made by 8x8 Square objects
-Moves Piece objects into the Square objects
-Helps evaluate the moves

===================================================================================
'''
class Board:

    squares = {}
    
    def __init__(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)
    
    # Save the state of existing, individual pieces on the board
    def save_board(self):
        pieces = []

        for loc, square in self.squares.items():
            if square.square_occupied():
                pieces.append( (loc, square.get_square_piece()) )

        return pieces

    def restore_board(self, savedState):
        
        self.clear_board()

        for loc, piece in savedState:
            pieceLocation = Square.parse_position(loc)

            self.squares[Square.position(pieceLocation['row'], pieceLocation['col'])].assign_piece_to_square(piece)

    def add_piece(self, color, pieceType, row, column):

        pieceObject = Piece(type=pieceType, color=color)
        self.squares[Square.position(row, column)].assign_piece_to_square(pieceObject)
    
    def move_piece(self, current_square, next_square):

        piece = current_square.get_square_piece()

        '''If next_square is occupied, capture piece'''
        if next_square.square_occupied() and next_square.get_square_piece().alive():
            
            # Capture black king
            if next_square.get_square_piece().get_type() == 'King' and next_square.get_square_piece().get_color() == 'black':
                output_board_file = open('gameResult.txt', 'w')
                print()
                print('Black King Captured! Game Over')
                print('\nBlack King Captured! Game Over\n\n', file = output_board_file)
                print(self, file = output_board_file)
                print()
                for loc, square in self.squares.items():
                    if square.square_occupied() and square == current_square:
                        square.remove_piece_from_square()
                self.add_piece(piece.get_color(), piece.get_type(), next_square.get_square_row(), next_square.get_square_column())
                print(self)
                sys.exit()

            # Capture white king
            if next_square.get_square_piece().get_type() == 'King' and next_square.get_square_piece().get_color() == 'white' and current_square.get_square_piece().get_color() == 'black':
                output_board_file = open('gameResult.txt', 'w')
                print()
                print('White King Captured! Game Over')
                print('\nWhite King Captured! Game Over\n\n', file = output_board_file)
                print(self, file = output_board_file)
                print()
                for loc, square in self.squares.items():
                    if square.square_occupied() and square == current_square:
                        square.remove_piece_from_square()
                self.add_piece(piece.get_color(), piece.get_type(), next_square.get_square_row(), next_square.get_square_column())
                print(self)
                sys.exit()

        piece = current_square.get_square_piece()
        current_square.remove_piece_from_square()
        
        for loc, square in self.squares.items():
            if square.square_occupied() and square == current_square:
                square.remove_piece_from_square()

        self.add_piece(piece.get_color(), piece.get_type(), next_square.get_square_row(), next_square.get_square_column())

    def get_possible_moves(self, color):

        moves = []

        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().alive() and square.get_square_piece().test_color(color):
                for move in square.generate_moves():
                    moves.append( (square.get_square_piece().get_type(), move.get_square_row(), move.get_square_column()) )

        return moves
        
    def possible_moves(self, color):

        moves = []

        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().alive() and square.get_square_piece().test_color(color):
                for move in square.generate_moves():
                    ##original return method
                    moves.append( (square, move) )

        return moves

    def get_piece_square(self, color, pieceType):
        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().test_color(color) and square.get_square_piece().test_type(pieceType):
                return square

        return None

    def evaluate_check(self, color):
        otherPlayersSquares = []

        for loc, square in self.squares.items():
            if square.square_occupied() and not square.get_square_piece().test_color(color):
                otherPlayersSquares.append(square)

        otherPlayersMoves = []
        for sq in otherPlayersSquares:
            otherPlayersMoves += sq.generate_moves()

        myKing = self.get_piece_square(color, 'King')

        if not myKing:
            return False
        
        for move in otherPlayersMoves:
            if move == myKing:
                return True

        return False

    def checkmate(self, color):
        my_moves    = self.get_possible_moves(color)
        other_moves = self.get_possible_moves(Board.op_color(color))

        my_possible_moves = []
        enemy_possible_moves = []

        for move in my_moves:
            my_possible_moves.append((move[1],move[2]))

        for move in other_moves:
            enemy_possible_moves.append((move[1],move[2]))

        # Return True if enemy_possible_moves is a subset of my_possible_moves

        for loc, square in self.squares.items():
            if square.square_occupied() and not square.get_square_piece().test_color(color):
                for my_move in my_possible_moves:
                    if square.get_square_row() == my_move[0] and square.get_square_column() == my_move[1]:
                        if color == 'white':
                            return set(enemy_possible_moves).issubset(my_possible_moves)
                        else:
                            return set(my_possible_moves).issubset(enemy_possible_moves)

        return False

    @staticmethod
    def op_color(color):
        return 'black' if color == 'white' else 'white'

    # Display board 
    def __str__(self):
        column_view = '  %s  ' * 8 % tuple( [ ascii_uppercase[c] for c in list(range(8)) ] )
        board_view = "  %s\n" % (column_view,)
        board_view += '  ' + '-' * len(column_view) + "\n"

        for row in range(7, -1, -1):
            row_view = str(row + 1)

            for col in range(8):
                if self.squares[Square.position(row, col)].square_occupied():
                    piece = str(self.squares[Square.position(row, col)].get_square_piece())
                else:
                    piece = "  "
                row_view += '| %s ' % (piece)

            row_view += "| %d\n" % (row + 1)
            board_view += row_view
            board_view += '  ' + '-' * len(column_view) + "\n"

        board_view += ' ' + column_view

        return board_view

    def evaluate_move(self, color):

        if (color == 'white' and self.checkmate('black')) or (color == 'black' and self.checkmate('black')):
            # print('\n\n\nCHECKMATE BONUS\n\n\n')
            return 10000
        elif (color == 'white' and self.checkmate('white')) or (color == 'black' and self.checkmate('white')):
            # print('\n\n\nCHECKMATE Alert\n\n\n')
            return -10000
        
        # If able to check, reward square. If in check, add cost
        if self.evaluate_check(Board.op_color(color)):
            return 1000

        heuristic_bonus = 0

        white_moves = []
        black_moves = []

        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().alive():
                piece = square.get_square_piece()

                # Positional analysis
                heuristic_bonus = Heuristic.square_value(square, piece.get_color(), self)

                # Number of moves analysis
                if piece.test_color('white'):
                    white_moves += square.generate_moves()
                else:
                    black_moves += square.generate_moves()

        total = 10 * (len(white_moves) - len(black_moves))

        total += heuristic_bonus

        return total

'''
===================================================================================
Piece Class:
-Each piece object has a color, type, and can tell us whether or not it is alive
-A piece can be one of three different pieces (white Rook, white King, black King)

===================================================================================
'''
class Piece:

    # White or black
    color = None

    # King or Rook
    type = None

    # Is the piece still alive or dead?
    alive = True

    def alive(self):
        return self.alive

    def get_type(self):
        return self.type

    def get_color(self):
        return self.color

    def test_type(self, test):
        return self.type == test

    def test_color(self, testColor):
        return self.color == testColor

    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.color = kwargs['color']

    def __str__(self):
        if self.color == 'black':
            if self.type == 'King':
                return '♛ '
        elif self.color == 'white':
            if self.type == 'King':
                return '♕ '
            elif self.type == 'Rook':
                return '♖ '
        
        # Return descriptive piece
        return self.color[0].lower() + self.type[0].upper()

'''
===================================================================================
Square Class:
-Part of the board
-Holds the piece object
-Can tell us the row and column a piece is at
-Generates all possible moves and feeds them back to the Board class
-Can tell us if a square is empty or not
-Can assign/remove pieces to squares

===================================================================================
'''
class Square:
    
    def __init__(self, *args, **kwargs):
        self.MAX_ROW = 7
        self.MAX_COL = 7
        self.MIN_ROW = 0
        self.MIN_COL = 0

        self.row = 0
        self.column = 0
        self.occupied = False
        self.Piece = None

        if len(args) == 2:
            self.row = args[0]
            self.column = args[1]
        else:
            positionParts = Square.parse_position(args[0])
            self.row = positionParts['row']
            self.column = positionParts['col']

    def get_square_row(self):
        return self.row

    def get_square_column(self):
        return self.column

    def square_occupied(self):
        return self.occupied

    def remove_piece_from_square(self):
        self.occupied = False

        self.Piece = None

    def assign_piece_to_square(self, piece):
        if piece is None:
            self.occupied = False
        else:
            self.occupied = True

        self.Piece = piece

    def get_square_piece(self):
        return self.Piece

    def generate_moves(self):

        moves = []

        if self.Piece.type == 'Rook':
            
            # All possible row moves
            for i in range(self.MAX_ROW+1):
                if i is not self.row:
                    moves.append(Square(i, self.column))

            # All possible column moves
            for i in range(self.MAX_COL+1):
                if i is not self.column:
                    moves.append(Square(self.row, i))

        elif self.Piece.type == 'King':

            # Make sure we're still in bounds
            if self.row - 1 >= self.MIN_ROW:

                newRow = self.row - 1

                for i in range(self.column - 1, self.column + 2):
                    if i >= self.MIN_COL and i <= self.MAX_COL:
                        moves.append(Square(newRow, i))

            # All possible row moves
            for i in range(self.column - 1, self.column + 2):
                if i >= self.MIN_COL and i <= self.MAX_COL and i is not self.column:
                    moves.append(Square(self.row, i))

            # All possible column moves
            if self.row + 1 <= self.MAX_ROW:

                newRow = self.row + 1

                for i in range(self.column - 1, self.column + 2):
                    if i >= self.MIN_COL and i <= self.MAX_COL:
                        moves.append(Square(newRow, i))

        return moves

    @staticmethod
    def position(row, column):
        return ascii_uppercase[int(column)] + str(int(row) + 1)

    @staticmethod
    def parse_position(position_discription):
        if len(position_discription) is not 2:
            raise Exception('Invalid position specified')

        col = position_discription[0]
        row = position_discription[1]

        return {
            'col': ("A", "B", "C", "D", "E", "F", "G", "H").index(col),
            'row': int(row) - 1
        }

    # True if squares in same location else False
    def __eq__(self, other_square):
        return self.row == other_square.row and self.column == other_square.column

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