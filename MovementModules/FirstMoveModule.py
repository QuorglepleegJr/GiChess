from .MovementModule import MovementModule

class FirstMoveModule(MovementModule):

    def __init__(self, vector_strings):

        super().__init__(vector_strings)
        # Added lines to vector_strings over normal:
        # enpassantable, square(s) enpassantable on
        
    def get_legal_moves(self, square, colour, board, piece):

        if piece.moves != 0:

            return []

        # I hate I need to copy paste this!

        legal_moves = []
        
        for vector_list in self.vector_lists:

            resolution_stack = [(0, square, 1)]
            # Format: index in vector list, square, current repetition

            while resolution_stack:

                current_resolution = resolution_stack.pop()

                if current_resolution[0] >= len(vector_list):

                    continue

                vector = vector_list[current_resolution[0]]

                if not vector[4]:

                    resolution_stack.append((current_resolution[0] + 1, current_resolution[1], 1))
                    # Add option of no movement for this vector

                new_square = (current_resolution[1][0] + vector[0], \
                    current_resolution[1][1] + vector[1] * (2 * int(colour == "W") - 1))
                
                if not board.is_valid_square(new_square)  or (current_resolution[2] > vector[2] and vector[2] != -1):

                    continue

                contents = board.get_square_contents(new_square)

                no_further = board.square_blocks_movement(new_square)
                can_move = board.square_usable(new_square) and (bool(contents) or vector[3] < 2)

                functions = []

                for other in contents:

                    if other.check_condition("blocksmovement", square, board, piece) and \
                        not True in piece.get_attribute_values("jumping"):

                        no_further = True

                    if other.check_condition("capturable", square, board, piece) and vector[3] > 0:

                        functions.append((board.capture_piece, other, new_square, piece))

                    elif not other.check_condition("standable", square, board, piece):

                        can_move = False

                valid_repetition_count = not vector[5](current_resolution[2])

                if valid_repetition_count and can_move and current_resolution[0] == len(vector_list) - 1:

                    if vector[6]:

                        en_passant_squares = [(square[0] + v[0], square[1] + v[1] * (2 * int(colour == "W") - 1)) for v in vector[7]]
                        functions.append((board.enable_enpassant, piece, tuple(en_passant_squares)))

                    legal_moves.append((new_square[0], new_square[1], tuple(functions)))

                if not no_further or True in piece.get_attribute_values("jumping"):

                    resolution_stack.append((current_resolution[0], new_square, current_resolution[2] + 1))
                    resolution_stack.append((current_resolution[0] + 1, new_square, 1))
                    
        return legal_moves