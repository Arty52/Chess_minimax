from random import randint
from Square import Square
from Piece import Piece
from Strategy import Strategy
import sys

class Board(object):

    blackIsInCheckmate = False
    whiteIsInCheckmate = False

    squares = {}

    setup = {}

    capturedPieces = []

    _cacheSquares = []
    _cacheLocationsUsed = []

    def __init__(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)
    
    """
    Initial setup. For this assignment we are using just
    two kings and one rook
    """
    def setupRandom(self):

        pieces = {
            'white': ('King', 'Rook'),
            'black': ('King',)
        }

        for color, pieceTypes in pieces.items():
            for pieceType in pieceTypes:
                pieceLocation = Square.parsePosition(Board.randomSquare())
                self.addPiece(color, pieceType, pieceLocation['row'], pieceLocation['col'])

    def clearBoard(self):
        for i in range(8):
            for j in range(8):
                self.squares[Square.position(i, j)] = Square(i, j)
    
    # Save the state of existing, individual pieces on the board
    def saveState(self):
        pieces = []

        for loc, square in self.squares.items():
            if square.isOccupied():
                pieces.append( (loc, square.getPiece()) )

        return pieces

    def restoreState(self, savedState):
        
        self.clearBoard()

        for loc, piece in savedState:
            pieceLocation = Square.parsePosition(loc)

            self.squares[Square.position(pieceLocation['row'], pieceLocation['col'])].assignPiece(piece)

    def cloneBoard(self):
        # create new board
        clone = Board()

        print(self)
        for loc, square in self.squares.items():
            if square.isOccupied():
                piece = square.getPiece()
                print(piece)
                # clone.addPiece(square.getPiece)
        
        # for piece in square
        # clone.addPiece()
        # for piece in saveState:
        #     print(piece)
        
        return clone

    def addPiece(self, color, pieceType, row, column):
        '''
        Add piece to the board at (row, column)
        :param color: str
        :param pieceType: str
        :param row: int
        :param column: int
        :return: None
        '''

        pieceObject = Piece(type=pieceType, color=color)
        self.squares[Square.position(row, column)].assignPiece(pieceObject)
    
    def movePiece(self, fromSquare, toSquare):
        '''
        :type fromSquare: Square
        :type toSquare: Square
        :return: None
        '''

        piece = fromSquare.getPiece()

        '''If toSquare is occupied, capture piece'''
        if toSquare.isOccupied() and toSquare.getPiece().isAlive():
            if toSquare.getPiece().getType() == 'King':
                print()
                print('King Captured! Game Over')
                print()
                for loc, square in self.squares.items():
                    if square.isOccupied() and square == fromSquare:
                        square.removePiece()
                self.addPiece(piece.getColor(), piece.getType(), toSquare.getRow(), toSquare.getColumn())
                print(self)
                sys.exit()
            
            self.capturedPieces.append(toSquare.getPiece())

        piece = fromSquare.getPiece()
        fromSquare.removePiece()
        
        for loc, square in self.squares.items():
            if square.isOccupied() and square == fromSquare:
                # print('Occupied:')
                # print(loc, square)
                square.removePiece()
            
        # toSquare.assignPiece(piece)
        
        # Add piece to the board
        # print('from: {} {}'.format(piece, fromSquare))
        # print('to: {} {}'.format(piece, toSquare))
        self.addPiece(piece.getColor(), piece.getType(), toSquare.getRow(), toSquare.getColumn())

    def legalMoves(self, color):
        '''
        Generate all legal moves for the specified color.
        Returns a list of tuples (from, to)
        :type color: str
        :return: [(Square, Square)]
        '''

        moves = []

        for loc, square in self.squares.items():
            if square.isOccupied() and square.getPiece().isAlive() and square.getPiece().isColor(color):
                for move in square.generateMoves():
                    ##original return method
                    moves.append( (square, move) )

        return moves

    def getLegalMoves(self, color):
        '''
        Generate all legal moves for the specified color.
        Returns a list of tuples (from, to)
        :type color: str
        :return: [(Square, Square)]
        '''

        moves = []

        for loc, square in self.squares.items():
            if square.isOccupied() and square.getPiece().isAlive() and square.getPiece().isColor(color):
                for move in square.generateMoves():
                    ##original return method
                    #moves.append( (square, move) )

                    ##method that returns (from row, from column, to row, to column) 
                    #moves.append( (square.getRow(),square.getColumn(),move.getRow(),move.getColumn()) )

                    ##method that returns (Color, Piece, to row, to column)
                    #moves.append( (square.getPiece().getColor(),square.getPiece().getType(), move.getRow(), move.getColumn()) )

                    ##method that returns (Piece, to row, to column)
                    moves.append( (square.getPiece().getType(), move.getRow(), move.getColumn()) )


                    ##method that returns (Color, Piece, to row, to column)
                    #moves.append( (move.getRow(), move.getColumn()) )

        return moves

    # O(n)
    def getPieceSquare(self, color, pieceType):
        for loc, square in self.squares.items():
            if square.isOccupied() and square.getPiece().isColor(color) and square.getPiece().isType(pieceType):
                return square

        return None

    def inCheck(self, color):
        otherPlayersSquares = []

        for loc, square in self.squares.items():
            if square.isOccupied() and not square.getPiece().isColor(color):
                otherPlayersSquares.append(square)

        otherPlayersMoves = []
        for sq in otherPlayersSquares:
            otherPlayersMoves += sq.generateMoves()

        myKing = self.getPieceSquare(color, 'King')

        if not myKing:
            return False
        
        for move in otherPlayersMoves:
            if move == myKing:
                return True

        return False

    def isDraw(self):
        return False

    def newCheckmate(self, color):
        my_moves    = self.getLegalMoves(color)
        other_moves = self.getLegalMoves(Board.oppositeColor(color))

        my_possible_moves = []
        enemy_possible_moves = []

        for move in my_moves:
            my_possible_moves.append((move[1],move[2]))

        for move in other_moves:
            enemy_possible_moves.append((move[1],move[2]))

        # Return True if enemy_possible_moves is a subset of my_possible_moves
        for loc, square in self.squares.items():
            if square.isOccupied() and not square.getPiece().isColor(color):
                for my_move in my_possible_moves:
                    if square.getRow() == my_move[0] and square.getColumn() == my_move[1]:
                        return set(enemy_possible_moves).issubset(my_possible_moves)

        return False

    def isCheckmate(self, color):

        # Perform some caching for multiple checkmate lookups
        if (color == 'white' and self.whiteIsInCheckmate) or (color == 'black' and self.blackIsInCheckmate):
            return True

        if not self.inCheck(color):
            return False

        otherKingSquare = self.getPieceSquare(Board.oppositeColor(color), 'King')

        currentState = self.saveState()

        otherKingsMoves = otherKingSquare.generateMoves()

        stillInCheck = True

        for move in otherKingsMoves:
            self.movePiece(otherKingSquare, move)

            if not self.inCheck(color):
                stillInCheck = False
                if color == 'white':
                    self.whiteIsInCheckmate = True
                else:
                    self.blackIsInCheckmate = True

        # Reset the board to the original state
        self.restoreState(currentState)

        # If still in check (after checking all available moves), checkmate
        print('Checkmate? ', stillInCheck)
        return stillInCheck

    @staticmethod
    def oppositeColor(color):
        return 'black' if color == 'white' else 'white'

    def __str__(self):
##        return self.getPieceSquare('white','King')
##        return self.getPieceSquare('white','Rook')
##        return self.getPieceSquare('black','King')

        columnDisplay = '  %s  ' * 8 % tuple( [ Square.indexColumn(c) for c in list(range(8)) ] )
        boardDisplay = "  %s\n" % (columnDisplay,)
        boardDisplay += '  ' + '-' * len(columnDisplay) + "\n"
        
        for row in range(7, -1, -1):
            rowDisplay = str(row + 1)
            
            for col in range(8):
                if self.squares[Square.position(row, col)].isOccupied():
                    piece = str(self.squares[Square.position(row, col)].getPiece())
                else:
                    piece = "  "
                rowDisplay += '| %s ' % (piece,)

            rowDisplay += "| %d\n" % (row + 1,)
            boardDisplay += rowDisplay
            boardDisplay += '  ' + '-' * len(columnDisplay) + "\n"
        boardDisplay += ' ' + columnDisplay
        
        return boardDisplay

    '''
    Formula developed by Claud Shannon 1949, modified for this assignment
    f(p) = 20000(K-K')
           + 900(Q-Q')
           + 500(R-R')
           + 300(B-B' + N-N')
           + 100(P-P')
           - 50(D-D' + S-S' + I-I')
           + 10(M-M') + ...
     
    KQRBNP = number of kings, queens, rooks, bishops, knights and pawns
    D,S,I = doubled, blocked and isolated pawns
    M = Mobility (the number of legal moves)
    '''

    def evaluate(self, color):

        whiteKing = 1
        whiteRook = 1
        blackKing = 1

        whiteMoves = []
        blackMoves = []

        if (color == 'white' and self.newCheckmate('black')) or (color == 'black' and self.newCheckmate('white')):
            print('\n\n\nCHECKMATE BONUS\n\n\n')
            return 1000000
        elif (color == 'white' and self.newCheckmate('white')) or (color == 'black' and self.newCheckmate('black')):
            return -1000000
            print('\n\n\nCHECKMATE Alert\n\n\n')

        if self.inCheck(Board.oppositeColor(color)):
            print('\nCheck bonus!\n')
            return 1000

        positionBonus = 0

        for loc, square in self.squares.items():
            if square.isOccupied() and square.getPiece().isAlive():
                piece = square.getPiece()

                # Positional analysis
                positionBonus = Strategy.squareToValue(square, piece.getColor(), self)

                # Number of moves analysis
                if piece.isColor('white'):
                    whiteMoves += square.generateMoves()
                else:
                    blackMoves += square.generateMoves()

        # Capture Analysis
        for piece in self.capturedPieces:
            if piece.isType('King'):
                if piece.isColor('white'):
                    whiteKing = 0
                else:
                    blackKing = 0
            elif piece.isType('Rook') and piece.isColor('white'):
                whiteRook = 0

        # Evaluate the available attacks on the board and give a bonus
        # attackBonus = self.evaluateAttackBonus(color, movesLookup)
        
        '''Reward for piece in same row/col'''
        # active_pieces = []
        # for loc, square in self.squares.items():
        #     if square.isOccupied():
        #         active_pieces.append((square.getRow(), square.getColumn()))
        # print(active_pieces)



        movesLookup = whiteMoves if color == 'black' else blackMoves

        # Evaluate the pieces under attack and subtract points for those positions
        # underAttack = self.evaluateUnderAttack(color, movesLookup)

        total = 20000 * (whiteKing - blackKing)
        total += 500 * (whiteRook) # No black rook exists
        total += 10 * (len(whiteMoves) - len(blackMoves))

        total += positionBonus
        # total += self.evaluateAttackBonus(color, movesLookup)
        # total += self.evaluateUnderAttack(color, movesLookup)

        # print('Evaluation of move = ' + str(total))

        return total

    def evaluateAttackBonus(self, color, moves):

        attackBonus = 0

        # King Attack
        kingLocation = self.getPieceSquare(Board.oppositeColor(color), 'King')
        print(color)
        print(kingLocation)

        # Rook Attack
        rookLocation = self.getPieceSquare(Board.oppositeColor(color), 'Rook')
        print(rookLocation)

        for move in moves:
            print(move)

            if move == kingLocation:
                attackBonus += Strategy.ATTACK_KING_BONUS

            if move == rookLocation:
                attackBonus += Strategy.ATTACK_ROOK_BONUS

        return attackBonus

    def evaluateUnderAttack(self, color, moves):

        underAttack = 0

        # Under Attack
        kingLocation = self.getPieceSquare(color, 'King')
        rookLocation = self.getPieceSquare(color, 'Rook')

        for move in moves:

            if move == kingLocation:
                underAttack -= Strategy.ATTACK_KING_BONUS

            if move == rookLocation:
                underAttack -= Strategy.ATTACK_ROOK_BONUS

        return underAttack

    @staticmethod
    def randomSquare():

        # Only generate the squares once since this operation is O(n^2)
        if not Board._cacheSquares:
            cols = ("A", "B", "C", "D", "E", "F", "G", "H")
            rows = range(8)

            for col in range(len(cols)):
                for row in rows:
                    Board._cacheSquares.append(cols[col] + str(row + 1))

        location = Board._cacheSquares[randint(0, len(Board._cacheSquares) - 1)]
        Board._cacheSquares.remove(location)

        return location
