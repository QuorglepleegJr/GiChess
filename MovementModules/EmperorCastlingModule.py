from .MovementModule import MovementModule

class EmperorCastlingModule(MovementModule):

    def __init__(self):

        super().__init__([])

    def get_legal_moves(self, square, colour, board, piece):

        if piece.moves != 0 or not True in piece.get_attribute_values("castling") or colour in board.banned_castling:

            return []

        legal_moves = []

        for checking_square in board.pieces.keys():

            if checking_square[1] == square[1] and checking_square[0] != square[0]:

                for checking_piece_pair in board.pieces[checking_square]:

                    checking_piece = checking_piece_pair[1]

                    if not (True in checking_piece.get_attribute_values("castling")) or "E" in checking_piece.get_attribute_values("tier") \
                        or checking_piece.colour != piece.colour or checking_piece.moves != 0:

                        continue

                    # Valid piece so far

                    if checking_square[0] < square[0]:

                        # a-side castling
                        emperor_square = (2, square[1])
                        other_square = (3, square[1])

                    else:

                        # h-side castling
                        emperor_square = (6, square[1])
                        other_square = (5, square[1])


                    cleared_board = board.copy()
                    cleared_board.remove_piece(checking_piece)
                    cleared_board.remove_piece(piece)
                    # cleared_board is used for checking empty squares
                    new_board = board.copy()
                    new_board.banned_castling.append(colour)
                    # new_board is used for checking check

                    valid_castle = True

                    emperor_square_contents = cleared_board.get_square_contents(emperor_square)
                    emperor_pieces_fail = False in [p.check_condition("standable", 
                        emperor_square, cleared_board, piece) for p in emperor_square_contents]

                    if emperor_pieces_fail or not cleared_board.square_usable(emperor_square):

                        valid_castle = False
                        continue

                    other_square_contents = cleared_board.get_square_contents(other_square)
                    other_pieces_fail = False in [p.check_condition("standable", 
                        other_square, cleared_board, checking_piece) for p in other_square_contents]

                    if other_pieces_fail or not cleared_board.square_usable(other_square):

                        valid_castle = False
                        continue

                    direction = 2 * int(square[0] <= emperor_square[0]) - 1

                    for i in range(square[0] + direction, emperor_square[0], direction):

                        new_square = (i, square[1])
                        new_board = new_board.from_simulated_position_update(piece, new_square, True)

                        new_square_contents = cleared_board.get_square_contents(new_square)
                        pieces_fail = True in [p.check_condition("blocksmovement", 
                            new_square, cleared_board, piece) for p in new_square_contents]
                        

                        if pieces_fail or cleared_board.square_blocks_movement(new_square):

                            valid_castle = False
                            break

                    if not valid_castle or new_board.check_check(piece.colour, [piece]):

                        valid_castle = False
                        continue

                    direction = (2 * int(checking_square[0] <= other_square[0]) - 1)

                    for i in range(checking_square[0] + direction, other_square[0], direction):

                        new_square = (i, square[1])

                        new_square_contents = cleared_board.get_square_contents(new_square)
                        pieces_fail = True in [p.check_condition("blocksmovement", 
                            new_square, cleared_board, checking_piece) for p in new_square_contents]

                        if pieces_fail or cleared_board.square_blocks_movement(new_square):
                        
                            valid_castle = False
                            break

                    if valid_castle:

                        legal_moves.append((emperor_square[0], emperor_square[1], ((board.relocate_piece, checking_piece, other_square),)))

        return legal_moves

                    