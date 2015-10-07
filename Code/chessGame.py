import sys
from copy import deepcopy

from minimax import minimax, min_play, max_play
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
    output_file_handle = open(_filehandle, 'w')

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
    output_file_handle.write(board_configuration)  #uncomment up above
    
    # print('The next board configuration has been stored to {} in the working directory.'.format(output_file_handle))
    # output_file_handle.close()

def playCase(turn):
    for line in GAME_STATES:
        board = Board()
        try:
            # Subtract 1 to accomidate indexing
            # print(line)
            board.addPiece('white', 'King', int(line[0])-1, int(line[1])-1)
            # print('White king added: ♕  at {}{}'.format(int(line[0]), printCol(int(line[1]-1))))
            board.addPiece('white', 'Rook', int(line[2])-1, int(line[3])-1)
            # print('White rook added: ♖  at {}{}'.format(int(line[2]), printCol(int(line[3]-1))))
            board.addPiece('black', 'King', int(line[4])-1, int(line[5])-1)
            # print('Black king added: ♛  at {}{}'.format(int(line[4]), printCol(int(line[5]-1))))

        except ValueError:
            print()
            print('Your file is not formatted correctly, refer to documentation for more information')
            print('Program will now exit.')
            print()
            sys.exit()

        solve_game(board, turn)
        # sys.exit()      #run only once

# Takes column value and returns column letter
def printCol(colVal):
    cols = ("A", "B", "C", "D", "E", "F", "G", "H")
    return cols[colVal]

def solve_game(board, turn):

    # print(board)
    savedState = board.saveState()
    
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
    #Just used to check if all the moves were put in
    # print("White Rook Moves:")
    # print('Amount: {}'.format(len(wRookMoves)))
    # for j in wRookMoves:
    #     print(j)
    # print("White King Moves:")
    # print('Amount: {}'.format(len(wKingMoves)))
    # for j in wKingMoves:
    #     print(j)
    # print("Black King Moves:")
    # print('Amount: {}'.format(len(bKingMoves)))
    # for j in bKingMoves:
    #     print(j)

    move = minimax(board, turn)

    # Restore initial state of the board
    board.restoreState(savedState)
    
    # Display board state before move
    print('Board before move:')
    print(board)
    
    # Attach new configuration to board
    for loc, square in board.squares.items():
        '''populate object from board into move'''
        if square.isOccupied() and square == move[0]:
            move[0].assignPiece(square.getPiece())
        if square.isOccupied() and square == move[1]:
            move[1].assignPiece(square.getPiece())

    # Display what the move is
    print('Moving from {} to {} '.format(move[0], move[1]))
    board.movePiece(move[0], move[1])

    # Announce check! if black in check
    if board.inCheck('black'):
        print('Black in Check!')

    # Display board state after move
    print('Board after move:')
    print(board)
    outputBoard(board)

def main():
    global _filehandle
    global GAME_STATES

    print('Welcome to Art and Adam\'s minimax chess AI!')
    print()
    
    side = input('Which player would you like to go first (x - white or y - black)? ')
    if side == 'x':
        turn = 0
    else:
        turn = 1
    
    numberOfMoves = input('How many moves do you want to simulate? ')
    numberOfMoves = int(numberOfMoves)
    moveNumber = 1
    
    # _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
    print('...running testcase.txt')
    _filehandle = 'testcase.txt'
    
    
    if _filehandle != 'quit':
        while numberOfMoves != 0:
            if turn == 1:
                print('------------------------BLACK MOVE------------------------')
                turn = 0
            elif turn == 0:
                print('------------------------WHITE MOVE------------------------')
                turn = 1
            GAME_STATES = []
            importBoard()
            playCase(turn)
            print('move number {}'.format(moveNumber))
            numberOfMoves -= 1
            moveNumber += 1
    else:
        print('Goodbye!')
        quit()

if __name__ == '__main__':
    main()
