class Heuristic:

    king = [
        [-50,-40,-30,-20,-20,-30,-40,-50,],
        [-30,-20,-10,  0,  0,-10,-20,-30,],
        [-30,-10, 20, 30, 30, 20,-10,-30,],
        [-30,-10, 30, 40, 40, 30,-10,-30,],
        [-30,-10, 30, 40, 40, 30,-10,-30,],
        [-30,-10, 20, 30, 30, 20,-10,-30,],
        [-30,-30,  0,  0,  0,  0,-30,-30,],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]

    rook = [
        [0,  0,  0,  0,  0,  0,  0,  0,],
        [5, 10, 10, 10, 10, 10, 10,  5,],
        [-5,  0,  0,  0,  0,  0,  0, -5,],
        [-5,  0,  0,  0,  0,  0,  0, -5,],
        [-5,  0,  0,  0,  0,  0,  0, -5,],
        [-5,  0,  0,  0,  0,  0,  0, -5,],
        [-5,  0,  0,  0,  0,  0,  0, -5,],
        [0,  0,  0,  5,  5,  0,  0,  0]
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