import numpy
import sys
from copy import deepcopy

from minimax import minimax
# from minimax import heuristicWhite
from Board import Board

GAME_STATES = []
_filehandle = None

def importBoard():    
    try:
        with open(_filehandle) as fh:
        # with open('testcase1.txt') as fh:
            if fh:
                print('reading file')
                for i in fh:
                    line = i
                    # extract only integers from line
                    GAME_STATES.append([int(s) for s in line if s.isdigit()])

    except FileNotFoundError:
        print()
        print('Your file was not found!')
        print()

def outputBoard(board):
    # Open file so that we can write to it. This will create a new file if DNE
    # output_file_handle = open(_filehandle, 'w')
    
    white_king = None
    white_rook = None
    black_king = None
    
    # Get pieces
    for loc, square in board.squares.items():
        if square.isOccupied():
            if square.Piece.getType() == 'King' and square.Piece.getColor() == 'white':
                white_king = ( int(square.getRow()) + 1, int(square.getColumn()) + 1 )
            elif square.Piece.getType() == 'King' and square.Piece.getColor() == 'black':
                black_king = ( int(square.getRow()) + 1, int(square.getColumn()) + 1 )
            elif square.Piece.getType() == 'Rook':
                white_rook = ( int(square.getRow()) + 1, int(square.getColumn()) + 1 )

    """
    Correct output: x.K(5,6), x.R(8,5), y.K(6,8)
    on a single line. (Row, Column)
    """

    # Make string for output
    board_configuration = 'x.K({},{}), x.R({},{}), y.K({},{})'.format(white_king[0], white_king[1],\
                                                                      white_rook[0], white_rook[1],\
                                                                      black_king[0], black_king[1] )
    
    print('Board Configuration:')
    print(board_configuration)
    """
    Uncomment below to write to the file. Output will overwrite input
    """
    # Print piece positions to file
    # print('{}{}{}'.format(), file = output_file_handle)
    
    # print('The next board configuration has been stored to {} in the working directory.'.format(output_file_handle))
    # output_file_handle.close()

def playCase():
    for line in GAME_STATES:
        board = Board()
        try:
            # Subtract 1 to accomidate indexing
            print(line)
            board.addPiece('white', 'King', int(line[0])-1, int(line[1])-1)
            print('White king added: ♕  at {}{}'.format(int(line[0]), printCol(int(line[1]-1))))
            board.addPiece('white', 'Rook', int(line[2])-1, int(line[3])-1)
            print('White rook added: ♖  at {}{}'.format(int(line[2]), printCol(int(line[3]-1))))
            board.addPiece('black', 'King', int(line[4])-1, int(line[5])-1)
            print('Black king added: ♛  at {}{}'.format(int(line[4]), printCol(int(line[5]-1))))

        except ValueError:
            print()
            print('Your file is not formatted correctly, refer to documentation for more information')
            print('Program will now exit.')
            print()
            sys.exit()
            
        solve_game(board)
        # sys.exit()      #run only once

# Takes column value and returns column letter
def printCol(colVal):
    cols = ("A", "B", "C", "D", "E", "F", "G", "H")
    return cols[colVal]

def solve_game(board):

    print(board)
    savedState = board.saveState()
    
    '''DEEP COPY'''
    # save = deepcopy(savedState)
    # print(save)
     
    # moves = deepcopy(board.squares)
    # clone = Board()
    # clone.squares = moves
    
    ''' Print all moves possible '''
    # wMoves = board.getLegalMoves('white')
    # bMoves = board.getLegalMoves('black')
    # #print(len(moves))
    #
    # #Empty lists for appending moves
    # wRookMoves = []
    # wKingMoves = []
    # bKingMoves = []
    #
    # #loop to go through all the legal white piece moves
    # #   appends those moves to the correct list
    # for i in wMoves:
    #     #i[x] let's me parse through the tuples within the list
    #     if i[0] == 'Rook':
    #         wRookMoves.append( (i[1]+1,printCol(i[2])) )
    #     elif i[0] == 'King':
    #         wKingMoves.append( (i[1]+1,printCol(i[2])) )
    #
    # for i in bMoves:
    #     bKingMoves.append( (i[1]+1,printCol(i[2])) )
    #
    # #Just used to check if all the moves were put in
    # print("White Rook Moves:")
    # for j in wRookMoves:
    #     print(j)
    # print("White King Moves:")
    # for j in wKingMoves:
    #     print(j)
    # print("Black King Moves:")
    # for j in bKingMoves:
    #     print(j)
    

    
    # print(savedState[0][1].getType())
    # moves = clone.legalMoves('white')
    # clone = board.cloneBoard()
    # clone = Board()
#     print('moving from {} to {}'.format(moves[0][0],moves[0][1]))
    # clone.movePiece(moves[0][0],moves[0][1])
    # print(clone)
#     print(board)
    # clone = deepcopy(board)
    # clone.movePiece(moves[0][0],moves[0][1])
    # print('board')
    # print(board)
    # print('clone')
    # print(clone)
    # clone = Board()
    # print(clone)
    # clone.restoreState(savedState)
    # print(clone)
    # clone.movePiece(moves[0][0],moves[0][1])
    # print(clone)
 
    '''minimax'''
    move = minimax(board)
 
    # print(board)
    # print(save)
    # score, move = heuristicWhite(board, 3, -float("inf"), float("inf"))
    board.restoreState(savedState)
    print(savedState)
    print(board)
    #print board pieces
    for loc, square in board.squares.items():
        if square.isOccupied():
            print(square.getPiece(), square.getRow(), square.getColumn())
        '''populate object from board into move'''
        if square.isOccupied() and square == move[0]:
            print('match!')
            move[0].assignPiece(square.getPiece())
        if square.isOccupied() and square == move[1]:
            move[1].assignPiece(square.getPiece())


    print('Moving from {} to {} '.format(move[0], move[1]))
    board.movePiece(move[0], move[1])
    print(board)
    outputBoard(board)
    # print(clone)
    # board.setup()
    # print(board)
    # pieces = board.saveState()
    # board.clearBoard()
    # print(board)
    # board.restoreState(pieces)
    # print(board)


def main():
    global _filehandle
    
    print('Welcome to Art and Adam\'s minimax chess AI!')
    print()
    
    while True:
        _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
        if _filehandle != 'quit':
            importBoard()
            playCase()

        else:
            print('Goodbye!')
            break

if __name__ == '__main__':
    main()
