from Piece import Piece
from PieceDatabase import PieceDatabase

class Board:

    basic_setup = "P3P5P4P2P1P4P5P3/P6x8/////p6x8/p3p5p4p2p1p4p5p3"

    def from_simulated_position_update(self, piece, new_position, duplicate = False):

        new_board = Board()

        new_board.pieces = {square: [x for x in self.pieces[square]] for square in self.pieces.keys()}
        new_board.previous_move = self.previous_move
        new_board.previous_move_enpassantable = self.previous_move_enpassantable
        new_board.enpassant_squares = self.enpassant_squares
        new_board.square_usable_funcs = self.square_usable_funcs
        new_board.square_blocks_movement_funcs = self.square_blocks_movement_funcs
        new_board.game_lose_functions = self.game_lose_functions
        new_board.game_win_functions = self.game_win_functions
        new_board.to_move = self.to_move
        new_board.game_ended = self.game_ended
        new_board.game_state_hashes = self.game_state_hashes

        old_square, piece_pair = self.locate_piece(piece)

        if not old_square is None and not duplicate:

            new_board.pieces[old_square].remove(piece_pair)

        if not new_position in new_board.pieces.keys():

            new_board.pieces[new_position] = []

        new_board.pieces[new_position].append(piece_pair)

        return new_board

    def __init__(self, setup = "///////"):

        self.pieces = Board.parse_setup_string(setup)
        # Format is (x, y) : [list of (piece no, pieces)]
        # String formatting is based upon FEN strings
        # Pn is white piece n, pn is black piece n, _n is n blanks, xn after a piece is n in a row
        # / means move to new line
        # Starts at A0 i.e. (0, 0)

        self.previous_move = None
        # Format is list of (Piece, [squares moved from/through/to in order])
        self.previous_move_enpassantable = False
        self.enpassant_squares = {}
        # Format is square: list of pieces

        self.square_usable_funcs = []
        self.square_blocks_movement_funcs = []
        self.game_lose_functions = []
        self.game_win_functions = []
        # Both game lose and game win functions return a list of colours (possibly empty)
        # And take input of the board only

        self.to_move = "W"
        self.game_ended = None

        self.game_state_hashes = {hash(self): 1}

    def parse_setup_string(setup):

        pieces = {}

        current_coord = (0, 0)
        coord_locked = False
        i = 0
        reached_end = False

        while not reached_end:

            match setup[i].lower():

                case "(":

                    coord_locked = True
                    i += 1

                case ")":

                    coord_locked = False
                    i += 1

                case "p":

                    # Piece
                    number = ""
                    multiple = ""
                    j = i + 1

                    while setup[j] in "0123456789":

                        number += setup[j]
                        j += 1

                        if j >= len(setup):

                            reached_end = True
                            break

                    if not reached_end and setup[j] == "x":

                        j += 1

                        while setup[j] in "0123456789":

                            multiple += setup[j]
                            j += 1

                            if j >= len(setup):

                                reached_end = True
                                break
                                
                    piece_no = int(number)
                    piece_multiple = 1

                    if multiple != "":

                        piece_multiple = int(multiple)

                    colour_string = "B"

                    if setup[i].isupper():

                        colour_string = "W"

                    for _ in range(piece_multiple):

                        new_piece = Piece(PieceDatabase.pieces[piece_no], colour_string)

                        if not current_coord in pieces.keys():
                    
                            pieces[current_coord] = []

                        pieces[current_coord].append((piece_no, new_piece))

                        if not coord_locked:
                        
                            current_coord = (current_coord[0] + 1, current_coord[1])

                    i = j

                case "_":

                    multiple = ""

                    while setup[j] in "0123456789":

                        multiple += setup[j]
                        j += 1

                        if j >= len(setup):

                            reached_end = True
                            break

                    current_coord = (current_coord[0] + int(multiple), current_coord[1])

                case "/":

                    current_coord = (0, current_coord[1] + 1)
                    i += 1

            if i >= len(setup):

                reached_end = True

        return pieces

    def get_square_contents(self, square):

        return [number_piece_pair[1] for number_piece_pair in self.pieces.get(square, [])]

    def is_valid_square(self, square):

        return square[0] >= 0 and square[0] < 8 and square[1] >= 0 and square[1] < 8

    def capture_piece(self, piece, square, culprit, piece_on_square = True):

        # On capture format: (piece capturing, square, board) -> is the piece captured
        # If multiple, one non-capture overrides all captures

        is_captured = True

        for result in piece.run_trigger("oncapture", square, self, culprit):

            is_captured &= result

        if is_captured:

            if not piece_on_square:

                new_square, piece_pair = [(s, p) for s in self.pieces.keys() for p in self.pieces[s] if p[1] == piece][0]

                self.pieces[new_square].remove(piece_pair)

            else:

                piece_pair = [p for p in self.pieces[square] if p[1] == piece][0]
                self.pieces[square].remove(piece_pair)

    def square_usable(self, square):

        usable = True

        for func in self.square_usable_funcs:

            result = func(square)

            if not result is None:

                usable = result

        return usable

    def square_blocks_movement(self, square):
    
        blocks = False

        for func in self.square_blocks_movement_funcs:

            result = func(square)

            if not result is None:

                blocks = result

        return blocks

    def move_made(self, piece, starting_square, move):

        self.previous_move_enpassantable = False
        self.enpassant_squares = {}

        piece_pair = [p for p in self.pieces[starting_square] if p[1] == piece][0]

        self.pieces[starting_square].remove(piece_pair)

        if self.pieces.get((move[0], move[1])) is None:

            self.pieces[(move[0], move[1])] = []

        self.pieces[(move[0], move[1])].append(piece_pair)

        for func in move[2]:

            func[0](*func[1:])

        self.previous_move = move
        piece.moves += 1

        h = hash(self)

        if not h in self.game_state_hashes.keys():

            self.game_state_hashes[h] = 0

        self.game_state_hashes[h] += 1

        self.check_game_end()

        if self.to_move == "W":

            self.to_move = "B"

        else:

            self.to_move = "W"

    def check_game_end(self):

        for h in self.game_state_hashes.keys():

            if self.game_state_hashes[h] > 2:

                self.game_over(("N", ["repetition"]))

        wins = {}

        for func in self.game_win_functions:

            for result in func():

                if not result[0] in wins:

                    wins[result[0]] = []

                wins[result[0]].append[result[1]]

        losses = {s : ["checkmate"] for s in self.check_for_importance()}

        for func in self.game_lose_functions:

            for result in func():

                if not result[0] in losses:

                    losses[result[0]] = []

                losses[result[0]].append[result[1]]

        has_won = len(wins.keys())
        has_lost = len(losses.keys())

        if has_won == 2 or has_lost == 2:

            string_list = ["simultaneous wins or losses:"]

            string_list.extend([s for s in wins.get("B", [])])
            string_list.extend([s for s in wins.get("W", [])])
            string_list.extend([s for s in losses.get("B", [])])
            string_list.extend([s for s in losses.get("W", [])])

            # Both players lost or won simultaneously
            self.game_over(("N", string_list))
            return

        if len(set(wins.keys()).intersection(set(losses.keys()))) != 0:

            string_list = ["simultaneous wins or losses:"]

            string_list.extend([s for s in wins["B"]])
            string_list.extend([s for s in wins["W"]])
            string_list.extend([s for s in losses["B"]])
            string_list.extend([s for s in losses["W"]])

            # One player both won and lost simultaneously
            self.game_over(("N", string_list))

            winner = list(wins.keys())[0]
            loser = list(losses.keys())[0]

            return

        if has_won == 1:

            winner = list(wins.keys())[0]
            self.game_over((winner, wins[winner]))
            return

        if has_lost == 1:

            loser = list(losses.keys())[0]

            if loser == "W":

                self.game_over(("B", losses[loser]))

            else:

                self.game_over(("W", losses[loser]))

            return

    def game_over(self, win_info):

        self.game_ended = win_info

        if self.game_ended is None:

            self.game_ended = ("N", "")

    def check_for_importance(self):

        no_important = ["B", "W"]

        for square in self.pieces.keys():

            for piece_pair in self.pieces[square]:

                if not piece_pair[1].colour in no_important:

                    continue

                if "E" in piece_pair[1].get_attribute_values("tier") \
                    or True in piece_pair[1].get_attribute_values("important"):

                    no_important.remove(piece_pair[1].colour)

        return no_important

    def broadcast_trigger(self, trigger, culprit=None):

        for square in self.pieces.keys():

            for piece_pair in self.pieces[square]:

                piece_pair[1].run_trigger(trigger, square, self, culprit)

    def enable_enpassant(self, piece, squares):

        self.previous_move_enpassantable = True

        for square in squares:

            if not square in self.enpassant_squares.keys():

                self.enpassant_squares[square] = []

            self.enpassant_squares[square].append(piece)

    def locate_piece(self, piece):

        for square in self.pieces.keys():

            for piece_pair in self.pieces[square]:

                if piece_pair[1] == piece:

                    return square, piece_pair

        return None, None

    def __hash__(self):

        hashables = []

        pieces = []

        for square in self.pieces.keys():

            pieces.extend([(self.pieces[square][i][0], (square[0], square[1], i), hash(self.pieces[square][i][1]), 
                hash(frozenset(self.pieces[square][i][1].get_legal_moves(square, self)))) for i in range(len(self.pieces[square]))])

        hashables.append(frozenset(pieces))

        for l in (self.square_usable_funcs, self.square_blocks_movement_funcs, self.game_win_functions, self.game_lose_functions):

            hashables.append(frozenset(l))

        return hash(frozenset(hashables))
