from .MovementModule import MovementModule

class EnPassantModule(MovementModule):

    def __init__(self):
    
        super().__init__([])

    def get_legal_moves(self, square, colour, board, piece):

        if not board.previous_move_enpassantable:

            return []

        legal_moves = []

        for enp_square in board.enpassant_squares.keys():

            new_board = board

            for enp_piece in board.enpassant_squares[enp_square]:

                new_board = new_board.from_simulated_position_update(enp_piece, enp_square)

            new_board.previous_move_enpassantable = False

            new_legal_moves = piece.get_legal_moves(square, new_board)

            fixed_legal_moves = []

            for move in new_legal_moves:

                new_funcs = []

                for func in move[2]:

                    new_func = func

                    if new_func[0] == new_board.capture_piece and new_func[2] == enp_square:

                        # Is an en-passant capture!
                        new_func = (board.capture_piece, *new_func[1:], False)

                    new_funcs.append(new_func)

                fixed_legal_moves.append((move[0], move[1], tuple(new_funcs)))

            legal_moves.extend(fixed_legal_moves)

        return legal_moves
