class Heuristic:

    king = [
        [-100,-75,-75,-50,-50,-75,-75,-100,],
        [-75,-50,-25,-10,-10,-25,-50,-75,],
        [-75,-25, 20, 75, 75, 20,-25,-75,],
        [-75,-25, 75, 90, 90, 75,-25,-75,],
        [-75,-25, 75, 90, 90, 75,-25,-75,],
        [-75,-25, 20, 75, 75, 20,-25,-75,],
        [-75,-50,-25,-10,-10,-25,-50,-75,],
        [-100,-75,-75,-75,-75,-75,-75,-100]
    ]

    rook = [
        [-100,10,-10,-10,-10,-10,10,-100,],
        [10, 5, 2, 5, 5, 2, 5,  10,],
        [-10,  5,  0,  0, 0,  0,  5, -10,],
        [-10,  0,  0,-2,-2,  0,  0, -10,],
        [-10,  0,  0,-2,-2,  0,  0, -10,],
        [-10,  5,  0,  0, 0,  0,  5, -10,],
        [10, 5, 2,  0,  0, 2, 5, 10,],
        [-100,10,-10,-10,-10,-10,10,-100]
    ]

    @staticmethod
    def square_value(square, color, board):

        # Get index values
        piece = square.get_square_piece()
        row = square.get_square_row()
        column = square.get_square_column()

        # If evaluated position in check, award bonus/cost
        if board.evaluate_check(color):
            return 1000
        #
        # if piece.get_type() == 'Rook':
        #     return Heuristic.rook[row][column]
        # elif piece.get_type() == 'King':
        #     return Heuristic.king[row][column]

        # White heuristic awards bonus to objects position
        if color == 'white':
            if piece.get_type() == 'Rook':
                return Heuristic.rook[row][column]
            elif piece.get_type() == 'King':
                return Heuristic.king[row][column]

        # Black heuristic awards cost to objects position
        else:
            if piece.get_type() == 'Rook':
                return Heuristic.rook[row][column] * -1
            elif piece.get_type() == 'King':
                return Heuristic.king[row][column] * -1