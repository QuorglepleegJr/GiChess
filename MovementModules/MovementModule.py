import Utility

class MovementModule:

    def __init__(self, vector_strings):

        self.vector_lists = MovementModule.expand_vector_strings(vector_strings)
        # Vector string format:
        # (ordered, List of vectors of the below form)
        # Individual vector format:
        # (x component, y component (positive is forward), number of potential repeats (-1=inf), 
        #    capture state (0=no, 1=yes, 2=only), required, restrictions on number of repeats (lambda int: bool where true = not allowed))

    def get_legal_moves(self, square, colour, board, piece):

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

                    legal_moves.append((new_square[0], new_square[1], (f for f in functions)))

                if not no_further or True in piece.get_attribute_values("jumping"):

                    resolution_stack.append((current_resolution[0], new_square, current_resolution[2] + 1))
                    resolution_stack.append((current_resolution[0] + 1, new_square, 1))
                    
        
        return legal_moves
                    
    def get_illegal_moves(self, square, colour, board, piece):
    
        return []

    def expand_vector_strings(vector_strings):

        vector_lists = []
        
        for vector_string in vector_strings:

            if vector_string[0]:

                vector_lists.append(vector_string[1])

            else:

                vector_lists.extend(Utility.permutations(vector_string[1]))

        return vector_lists

    