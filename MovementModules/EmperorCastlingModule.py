from .MovementModule import MovementModule

class EmperorCastlingModule(MovementModule):

    def __init__(self):

        super().__init__([])

    def get_legal_moves(self, square, colour, board, piece):
    
        return []