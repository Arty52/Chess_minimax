import numpy
import sys
from copy import deepcopy

from minimax import minimax
# from minimax import heuristicWhite
from Board import Board

GAME_STATES = []

def importBoard():
    try:
        with open('testcase1.txt') as fh:
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
        sys.exit()      #run only once

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
    
    # print(clone)
    
    
    
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
    board.restoreState(save)
    # print('Moving: ', move)
    # board.movePiece(move[0], move[1])
    print(board)
    # print(clone)
    # board.setup()
    # print(board)
    # pieces = board.saveState()
    # board.clearBoard()
    # print(board)
    # board.restoreState(pieces)
    # print(board)



def main():
    print('Welcome to Art and Adam\'s minimax chess AI!')
    print()
    
    '''
    Show what all three pieces look like
    '''
    
    importBoard()
    playCase()

    # solve
    

if __name__ == '__main__':
    main()
