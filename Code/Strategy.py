class Strategy:

    ATTACK_KING_BONUS = 5000
    ATTACK_ROOK_BONUS = 1000

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
    def squareToValue(square, color, board):
        piece = square.getPiece()

        row = square.getRow()
        column = square.getColumn()
        o_color = 'black' if color == 'white' else 'white'

        # Pseudo-mirror array using Python's reverse list lookup
        if color == 'black':
            row *= -1
            column *= -1
        
        # bKingLoc = None
        # if piece.getType() == 'Rook':
        #     for loc, square2 in board.squares.items():
        #         if square2.isOccupied() and square2.getPiece().getColor() == 'black':
        #             bKingLoc = ((square2.getRow(),square2.getColumn()))
        # #print('bKingLoc\n',bKingLoc)
        #
        # if bKingLoc:
        #     if piece.getType() == 'Rook' and (row == bKingLoc[0] or column == bKingLoc[1]):
        #         # print('ROWS')
        #         #print('row\n',row)
        #         #print('col\n',column)
        #         # print(Strategy.rook[row][column]+1000)
        #         return Strategy.rook[row][column]+1000
        #         #return Strategy.rook[row][bKingLoc[1]+1]+100
        #         #return [x + 10 for x in Strategy.rook[bKingLoc[0]]]
                
        if board.inCheck(o_color):
            return 1000
        elif board.inCheck(color):
            return -1000
        if piece.getType() == 'Rook':
            # print(Strategy.rook[row][column])
            return Strategy.rook[row][column]
        elif piece.getType() == 'King':
            return Strategy.king[row][column]