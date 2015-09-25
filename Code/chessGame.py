import numpy
from Board import Board

GAME_STATES = []

def importBoard():
    """" testcase: x.K(5,6), x.R(8,5), y.K(6,8) """
    
    try:
        with open('testcase1.txt') as fh:
            if fh:
                print('reading file')
                for i in fh:
                    line = i
                    GAME_STATES.append(line)

    except FileNotFoundError:
        print()
        print('Your file was not found!')
        print()

def playCase():
    for line in GAME_STATES:
        board = Board()
        board.addPiece('white', 'King', int(line[4])-1, int(line[6])-1)
        board.addPiece('white', 'Rook', int(line[14])-1, int(line[16])-1)
        board.addPiece('black', 'King', int(line[24])-1, int(line[26])-1)
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