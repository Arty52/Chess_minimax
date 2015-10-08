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
    
    #Input: N/A
    #Output: N/A
    #Purpose: To initialize the board object as a configuration of 8x8 square objects
    def __init__(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)
    
    #Input: N/A
    #Output: N/A
    #Purpose: To clear the board object of all pieces
    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)
    
    #Input: N/A
    #Output: N/A
    #Purpose: To save the board object in its current state, includes pieces
    # Save the state of existing, individual pieces on the board
    def save_board(self):
        pieces = []

        for loc, square in self.squares.items():
            if square.square_occupied():
                pieces.append( (loc, square.get_square_piece()) )

        return pieces
    
    #Input: N/A
    #Output: N/A
    #Purpose: To restore the board object to a previously saved state
    def restore_board(self, savedState):
        
        self.clear_board()

        for loc, piece in savedState:
            pieceLocation = Square.parse_position(loc)

            self.squares[Square.position(pieceLocation['row'], pieceLocation['col'])].assign_piece_to_square(piece)

    #Input: Board object, color of a piece, type of the piece, row number, column number
    #Output: N/A
    #Purpose: Adds a chess piece of a particular color and type to the board at the row and column indicated
    def add_piece(self, color, pieceType, row, column):

        pieceObject = Piece(type=pieceType, color=color)
        self.squares[Square.position(row, column)].assign_piece_to_square(pieceObject)

    #Input: Board object, the current square that the piece is in, and the square that the piece will move to
    #Output: The board with the piece in a new position
    #Purpose: To move a specific piece to a new space
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
            if next_square.get_square_piece().get_type() == 'King' and next_square.get_square_piece().get_color() == 'white' \
                                                                   and current_square.get_square_piece().get_color() == 'black':
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
            
            # Capture white rook
            if next_square.get_square_piece().get_type() == 'Rook' and next_square.get_square_piece().get_color() == 'white' \
                                                                   and current_square.get_square_piece().get_color() == 'black':
                output_board_file = open('gameResult.txt', 'w')
                print()
                print('White Rook Captured! Stalemate!')
                print('\nWhite King Captured! Stalemate!\n\n', file = output_board_file)
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

    #Input: Board object, and a team color
    #Output: Returns a list of tuples containing the piece type, the color of the piece, the row and column of possible moves
    #Purpose: To return all moves for a particular color with each piece type and color included
    def get_possible_moves(self, color):

        moves = []

        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().alive() and square.get_square_piece().test_color(color):
                for move in square.generate_moves():
                    moves.append( (square.get_square_piece().get_type(), move.get_square_row(), move.get_square_column()) )

        return moves

    #Input: Board object, and a team color
    #Output: a list of tuples that contains the square, and moves
    #Purpose: to return all moves for a particular color
    def possible_moves(self, color):

        moves = []

        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().alive() and square.get_square_piece().test_color(color):
                for move in square.generate_moves():
                    ##original return method
                    moves.append( (square, move) )

        return moves

    #Input: Board object, color of the piece, type of the piece
    #Output: returns the square where the piece is
    #Purpose: To find the square containing a particular piece
    def get_piece_square(self, color, pieceType):
        for loc, square in self.squares.items():
            if square.square_occupied() and square.get_square_piece().test_color(color) and square.get_square_piece().test_type(pieceType):
                return square

        return None

    #Input: Board object, and a team color
    #Output: returns true or false depending on whether or not a piece is in check
    #Purpose: Determines if a piece is in check
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

    #Input: Board object, a team color
    #Output: returns true or false if a king is in checkmate
    #Purpose: Used to determine if a team has gotten checkmate on the other team
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

    #Input: a team color
    #Output: the opposite team's color
    #Purpose: To get the opposite team's color for use within minimax
    @staticmethod
    def op_color(color):
        return 'black' if color == 'white' else 'white'

    #Input: Board object
    #Output: the board, organized to look like a chess board
    #Purpose: Overloads the print operator to allow the program to print all necessary pieces of the board
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

    #Input: Board object, a team color
    #Output: a numerical value
    #Purpose: Checks a move and scores it based on the Heuristic
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

    #Input: a Piece object
    #Output: returns true or false
    #Purpose: To report if a piece is alive or not
    def alive(self):
        return self.alive

    #Input: a Piece object
    #Output: returns true or false
    #Purpose: To report the type of the piece
    def get_type(self):
        return self.type

    #Input: a Piece object
    #Output: returns true or false
    #Purpose: To report the color of the piece
    def get_color(self):
        return self.color

    #Input: a Piece object
    #Output: returns true or false
    #Purpose: to use in a statement to check for valid condition
    def test_type(self, test):
        return self.type == test

    #Input: a Piece object
    #Output: returns true or false
    #Purpose: to use in a statement to check for valid condition
    def test_color(self, testColor):
        return self.color == testColor

    #Input: a Piece object
    #Output: N/A
    #Purpose: initializes the pieces
    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.color = kwargs['color']

    #Input: a Piece object
    #Output: 
    #Purpose: overloads the print operator to allow printing of special piece characters
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

    #Input: Square object
    #Output: N/A
    #Purpose: Initializes the square class
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

    #Input: a Square object
    #Output: the row of the square
    #Purpose: Allows the program to get the row of a square
    def get_square_row(self):
        return self.row

    #Input: a Square object
    #Output: the column of the square
    #Purpose: Allows the program to get the column of a square
    def get_square_column(self):
        return self.column

    #Input: a Square object
    #Output: True or false
    #Purpose: Allows the program to see if a square is occupied or not
    def square_occupied(self):
        return self.occupied

    #Input: a Square object
    #Output: N/A
    #Purpose: Removes a piece from a particular square
    def remove_piece_from_square(self):
        self.occupied = False

        self.Piece = None

    #Input: a Square object, and a piece object
    #Output: N/A
    #Purpose: Assigns a piece to square
    def assign_piece_to_square(self, piece):
        if piece is None:
            self.occupied = False
        else:
            self.occupied = True

        self.Piece = piece

    #Input: a Square object
    #Output: returns the piece in the square
    #Purpose: Allows the program to identify what piece is in a particular square
    def get_square_piece(self):
        return self.Piece

    #Input: a Square object
    #Output: returns the moves for each piece
    #Purpose: Allows the program to get all of the moves of all pieces
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

    #Input: a row and column
    #Output: returns the location of a square
    #Purpose: Returns the location of a square in a standard chess format, e.g. 'A5'
    @staticmethod
    def position(row, column):
        return ascii_uppercase[int(column)] + str(int(row) + 1)

    #Input: a position
    #Output: the row and column
    #Purpose: Returns the row and column
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

    #Input: two Square objects
    #Output: true or false
    #Purpose: overloads the == operator to allow comparison between two squares
    # True if squares in same location else False
    def __eq__(self, other_square):
        return self.row == other_square.row and self.column == other_square.column

    #Input: a Square object
    #Output: returns the square's properties
    #Purpose: overloads the print operator to allow printing of a square
    def __str__(self):
        if self.Piece is None:
            piece = ""
        else:
            piece = str(self.Piece)

        # Dictionary
        properties = {
            'piece'  : piece,
            'row'    : self.row + 1,
            'column' : ascii_uppercase[self.column],
        }

        return '%(piece)s(%(column)s%(row)d)' % properties