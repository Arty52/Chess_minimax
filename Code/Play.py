import sys
from copy import deepcopy
from Minimax import minimax
from Board import Board

GAME_STATES = []
_filehandle = None

def import_board():    
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

def output_board(board):
    # Open file so that we can write to it. This will create a new file if DNE
    output_file_handle = open(_filehandle, 'w')
    output_board_file = open('gameResult.txt', 'w')

    white_king = None
    white_rook = None
    black_king = None

    # Get pieces
    for loc, square in board.squares.items():
        if square.square_occupied():
            if square.Piece.get_type() == 'King' and square.Piece.get_color() == 'white':
                white_king = ( int(square.get_square_row()) + 1, int(square.get_square_column()) + 1 )
            elif square.Piece.get_type() == 'King' and square.Piece.get_color() == 'black':
                black_king = ( int(square.get_square_row()) + 1, int(square.get_square_column()) + 1 )
            elif square.Piece.get_type() == 'Rook':
                white_rook = ( int(square.get_square_row()) + 1, int(square.get_square_column()) + 1 )

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
    
    print(board, file = output_board_file)
    print('\nBoard configuration: ', file = output_board_file)
    output_board_file.write(board_configuration)
    
    # print('The next board configuration has been stored to {} in the working directory.'.format(output_file_handle))
    # output_file_handle.close()

def assign_turn(turn):
    if turn == 1:
        print('------------------------BLACK MOVE------------------------')
        return 0
    elif turn == 0:
        print('------------------------WHITE MOVE------------------------')
        return 1

def play_case(turn):
    for line in GAME_STATES:
        board = Board()
        try:
            # Subtract 1 to accomidate indexing
            # print(line)
            board.add_piece('white', 'King', int(line[0])-1, int(line[1])-1)
            # print('White king added: ♕  at {}{}'.format(int(line[0]), print_column(int(line[1]-1))))
            board.add_piece('white', 'Rook', int(line[2])-1, int(line[3])-1)
            # print('White rook added: ♖  at {}{}'.format(int(line[2]), print_column(int(line[3]-1))))
            board.add_piece('black', 'King', int(line[4])-1, int(line[5])-1)
            # print('Black king added: ♛  at {}{}'.format(int(line[4]), print_column(int(line[5]-1))))
            # print('Loaded Board: ')
            # print(board)

        except ValueError:
            print()
            print('Your file is not formatted correctly, refer to documentation for more information')
            print('Program will now exit.')
            print()
            sys.exit()

        solve_game(board, turn)
        # sys.exit()      #run only once

# Takes column value and returns column letter
def print_column(column_value):
    cols = ("A", "B", "C", "D", "E", "F", "G", "H")
    return cols[column_value]

def solve_game(board, turn):

    # print(board)
    saved_state = board.save_board()
    
    ''' Print all moves possible '''
    # wMoves = board.get_possible_moves('white')
    # bMoves = board.get_possible_moves('black')
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
    #         wRookMoves.append( (i[1]+1,print_column(i[2])) )
    #     elif i[0] == 'King':
    #         wKingMoves.append( (i[1]+1,print_column(i[2])) )
    #
    # for i in bMoves:
    #     bKingMoves.append( (i[1]+1,print_column(i[2])) )
    # # Just used to check if all the moves were put in
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

    '''
    Call Minimax with alpha-beta pruning
    '''
    move = minimax(board, turn)

    # Restore initial state of the board
    board.restore_board(saved_state)
    
    # Display board state before move
    print('Board before move:')
    print(board)
    
    # Attach new configuration to board
    for loc, square in board.squares.items():
        '''populate object from board into move'''
        if square.square_occupied() and square == move[0]:
            move[0].assign_piece_to_square(square.get_square_piece())
        if square.square_occupied() and square == move[1]:
            move[1].assign_piece_to_square(square.get_square_piece())

    # Display what the move is
    print('Moving from {} to {} '.format(move[0], move[1]))
    board.move_piece(move[0], move[1])

    # Announce check! if black in check
    if board.evaluate_check('black'):
        print('Black in Check!')

    # Display board state after move
    print('Board after move:')
    print(board)
    output_board(board)
    
def test_case():
    global _filehandle
    turn = 0
    
    number_of_moves = input('How many moves do you want to simulate (moves are done as pairs)? ')
    number_of_moves = int(number_of_moves)
    move_number = 1

    # _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
    print('...running testcase.txt')
    _filehandle = 'testCase.txt'

    game_count = 1
    while number_of_moves != 0:
        GAME_STATES = []
        import_board()
    
        turn = assign_turn(turn)
        play_case(turn)
        print('move number {}'.format(move_number))
        game_count += 1
        if game_count % 2:
            number_of_moves -= 1
            move_number += 1
    print('File printed to gameResult.txt \nGoodbye.')
    sys.exit()

def play_opponent():
    global _filehandle
    side = input('Which player would you like to go first (x - white or y - black)? ')
    if side == 'x':
        turn = 0
    else:
        turn = 1

    number_of_moves = input('How many moves do you want to simulate? ')
    number_of_moves = int(number_of_moves)
    move_number = 1

    _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
    print('running {}'.format(_filehandle))

    if _filehandle != 'quit':
        while number_of_moves != 0:
            GAME_STATES = []
            import_board()
    
            turn = assign_turn(turn)
            play_case(turn)
            print('move number {}'.format(move_number))
            number_of_moves -= 1
            move_number += 1
    else:
        print('Until next time, Goodbye!')

    sys.exit()

def main():
    global _filehandle
    global GAME_STATES

    print('\nWelcome to Art and Adam\'s minimax chess AI!\n')
    
    # Question (a)
    while True:
        test = input('Is this a test (y/n)? ').lower()
        if test == 'y' or test == 'n':
            break
    
    if test == 'y':
        # set White/Player X to go first
        # test_case()

        turn = 0
        
        # Question (b)
        number_of_moves = input('How many moves do you want to simulate (moves are done as pairs)? ')
        number_of_moves = int(number_of_moves)
        move_number = 1

        # _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
        print('...running testcase.txt')
        _filehandle = 'testCase.txt'

        game_count = 1
        while number_of_moves != 0:
            GAME_STATES = []
            import_board()

            turn = assign_turn(turn)
            play_case(turn)
            print('move number {}'.format(move_number))
            game_count += 1
            if game_count % 2:
                number_of_moves -= 1
                move_number += 1
        print('File printed to gameResult.txt \nGoodbye.')
        sys.exit()
        
    else:
        # play_opponent()
        side = input('Which player would you like to go first (x - white or y - black)? ')
        if side == 'x':
            turn = 0
        else:
            turn = 1

        number_of_moves = input('How many moves do you want to simulate (moves are done as pairs)? ')
        number_of_moves = int(number_of_moves)
        move_number = 1

        _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
        print('running {}'.format(_filehandle))

        if _filehandle != 'quit':
            while number_of_moves != 0:
                GAME_STATES = []
                import_board()

                turn = assign_turn(turn)
                play_case(turn)
                print('move number {}'.format(move_number))
                number_of_moves -= 1
                move_number += 1
        else:
            print('Goodbye!')

if __name__ == '__main__':
    main()
