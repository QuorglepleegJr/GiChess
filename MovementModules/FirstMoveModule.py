from .MovementModule import MovementModule

class FirstMoveModule(MovementModule):

    def __init__(self, vector_strings):

        super().__init__(vector_strings)
        
    def get_legal_moves(self, square, colour, board, piece):

        if piece.moves == 0:

            return super().get_legal_moves(square, colour, board, piece)

        return []