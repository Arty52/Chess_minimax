import sys
from copy import deepcopy
from Minimax import minimax
from Board import Board

GAME_STATES = []
_filehandle = None

#Input: N/A
#Output: A message telling the user if the board was imported
#Purpose: To import the board from a text file
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

#Input: a board object
#Output: The board with the pieces on it, outputs both the configuration and the board to a file
#Purpose: To Print the board and board configuratin to the terminal and a file
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

#Input: A single bit variable, either a 1 or a 0
#Output: Tells user whoevers turn it is, and returns a number according to whoever's turn it is
#Purpose: Allows the program to change between who gets to move their piece
def assign_turn(turn):
    if turn == 1:
        print('------------------------PLAYER Y MOVE------------------------')
        return 0
    elif turn == 0:
        print('------------------------PLAYER X MOVE------------------------')
        return 1

#Input: A single bit variable, either a 1 or a 0
#Output: The board configuration, with the piece next to its position on the board
#Purpose: To initialize the board object, and the pieces contained on the board
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

#Input: A number relative to the column on a chess board
#Output: Returns a letter relative to the column on a chess board
#Purpose: So the program can print real chess board locations, e.g. A5
def print_column(column_value):
    cols = ("A", "B", "C", "D", "E", "F", "G", "H")
    return cols[column_value]

#Input: A board object
#Output: Prints the board before and after moving a piece
#Purpose: Calls the minimax algorithm to help decide on a move, then moves the piece
def solve_game(board, turn):

    # Save current state of the board before preceding to computation
    saved_state = board.save_board()

    # Call Minimax with alpha-beta pruning
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

#Input: User inputs if they are running a test case or not, the number of moves to simulate, which player goes first, and the file to read from
#Output: Prints how many moves have been done
#Purpose: Prepares the program to run either a test case or general case, if requested to
def main():
    global _filehandle
    global GAME_STATES

    print('\nWelcome to Art and Adam\'s minimax chess AI!\n')
    
    # Question (a)
    while True:
        test = input('Is this a test (y/n)? ').lower()
        if test == 'y' or test == 'n':
            break
    
    # Is a test
    if test == 'y':
        # Set White/Player X to go first
        turn = 0
        
        # Question (b)
        number_of_moves = input('How many moves do you want to simulate (moves are done as pairs)? ')
        number_of_moves = int(number_of_moves)
        move_number = 1

        # _filehandle = input('Enter file you would like to open (type "quit" to exit): ')
        print('...running testCase.txt')
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
    
    # Play Opponent
    else:
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
            print('Goodbye!')

if __name__ == '__main__':
    main()
