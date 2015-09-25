import numpy
import sys

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
            board.addPiece('white', 'King', int(line[0])-1, int(line[1])-1)
            board.addPiece('white', 'Rook', int(line[2])-1, int(line[3])-1)
            board.addPiece('black', 'King', int(line[4])-1, int(line[5])-1)
        except ValueError:
            print()
            print('Your file is not formatted correctly, refer to documentation for more information')
            print('Program will now exit.')
            print()
            sys.exit()
            
        solve_game(board)


def solve_game(board):

    print(board)
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
    importBoard()
    playCase()

    # solve
    

if __name__ == '__main__':
    main()