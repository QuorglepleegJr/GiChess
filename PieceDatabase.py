import urllib.request

from AttributeModules.AttributeModule import AttributeModule

from ConditionCheckModules.ConditionCheckModule import ConditionCheckModule

from MovementModules.MovementModule import MovementModule
from MovementModules.EmperorCastlingModule import EmperorCastlingModule
from MovementModules.EnPassantModule import EnPassantModule
from MovementModules.FirstMoveModule import FirstMoveModule

from TriggerModules.TriggerModule import TriggerModule

class PieceDatabase:

    pieces = {
        # King
        1 : [
            MovementModule([
                (True, [(1, 0, 1, 1, True, lambda n: False)]),
                (True, [(1, 1, 1, 1, True, lambda n: False)]),
                (True, [(0, 1, 1, 1, True, lambda n: False)]),
                (True, [(-1, 1, 1, 1, True, lambda n: False)]),
                (True, [(-1, 0, 1, 1, True, lambda n: False)]),
                (True, [(-1, -1, 1, 1, True, lambda n: False)]),
                (True, [(0, -1, 1, 1, True, lambda n: False)]),
                (True, [(1, -1, 1, 1, True, lambda n: False)]),
            ]),
            EmperorCastlingModule(),
            AttributeModule(tier = "E", castling = True)
        ],
        # Queen
        2 : [
            MovementModule([
                (True, [(1, 0, -1, 1, True, lambda n: False)]),
                (True, [(1, 1, -1, 1, True, lambda n: False)]),
                (True, [(0, 1, -1, 1, True, lambda n: False)]),
                (True, [(-1, 1, -1, 1, True, lambda n: False)]),
                (True, [(-1, 0, -1, 1, True, lambda n: False)]),
                (True, [(-1, -1, -1, 1, True, lambda n: False)]),
                (True, [(0, -1, -1, 1, True, lambda n: False)]),
                (True, [(1, -1, -1, 1, True, lambda n: False)]),
            ]),
            AttributeModule(tier = "3", castling = True, promoption = True)
        ],
        # Rook
        3 : [
            MovementModule([
                (True, [(1, 0, -1, 1, True, lambda n: False)]),
                (True, [(0, 1, -1, 1, True, lambda n: False)]),
                (True, [(-1, 0, -1, 1, True, lambda n: False)]),
                (True, [(0, -1, -1, 1, True, lambda n: False)]),
            ]),
            AttributeModule(tier = "2", promoption = True)
        ],
        # Bishop
        4 : [
            MovementModule([
                (True, [(1, 1, -1, 1, True, lambda n: False)]),
                (True, [(-1, 1, -1, 1, True, lambda n: False)]),
                (True, [(-1, -1, -1, 1, True, lambda n: False)]),
                (True, [(1, -1, -1, 1, True, lambda n: False)]),
            ]),
            AttributeModule(tier = "2", promoption = True)
        ],
        # Knight
        5 : [
            MovementModule([
                (True, [(1, 0, 1, 1, True, lambda n: False), (1, 1, 1, 1, True, lambda n: False)]),
                (True, [(1, 0, 1, 1, True, lambda n: False), (1, -1, 1, 1, True, lambda n: False)]),
                (True, [(0, 1, 1, 1, True, lambda n: False), (1, 1, 1, 1, True, lambda n: False)]),
                (True, [(0, 1, 1, 1, True, lambda n: False), (-1, 1, 1, 1, True, lambda n: False)]),
                (True, [(-1, 0, 1, 1, True, lambda n: False), (-1, 1, 1, 1, True, lambda n: False)]),
                (True, [(-1, 0, 1, 1, True, lambda n: False), (-1, -1, 1, 1, True, lambda n: False)]),
                (True, [(0, -1, 1, 1, True, lambda n: False), (1, -1, 1, 1, True, lambda n: False)]),
                (True, [(0, -1, 1, 1, True, lambda n: False), (-1, -1, 1, 1, True, lambda n: False)]),
            ]),
            AttributeModule(tier = "2", horse = True, jumping = True, promoption = True)
        ],
        # Pawn
        6 : [
            MovementModule([
                (True, [(0, 1, 1, 0, True, lambda n: False)]),
                (True, [(1, 1, 1, 2, True, lambda n: False)]),
                (True, [(-1, 1, 1, 2, True, lambda n: False)]),
            ]),
            FirstMoveModule([
                (True, [(0, 1, 2, 0, True, lambda n: n != 2)]),
            ]),
            EnPassantModule(),
            AttributeModule(tier = "1", promotable = True)
        ],
    }

    piece_display = {}

    def generate_piece_display():

        with open("PieceTextDatabase.txt") as file:

            more_file = True
            
            while more_file:

                line = file.readline()

                while line[0:3] != "---":

                    line = file.readline()

                    if not line: 
                                        
                        more_file = False
                        break

                if not more_file:

                    break

                file.readline()
                number_line = file.readline()
                name_line = file.readline()
                tier_line = file.readline()
                cost_line = file.readline()

                line = file.readline()

                description = ""

                while line[0:3] != r"%%%":
                    
                    if line.strip() and line.strip()[0] == "-":

                        description += line

                    line = file.readline()

                file.readline()
                black_image_line = file.readline()
                white_image_line = file.readline()

                number = int(number_line[6:9])
                name = name_line.split("**")[1]

                if tier_line[0:4] == "Tier":

                    tier = tier_line[5]

                else:

                    tier = tier_line[0]

                cost = float(cost_line.strip()[5:])

                #with urllib.request.urlopen(black_image_line.strip()[3:]) as black_image:

                    #print("TEST")

                    #print(black_image.read())

                #white_image = urllib.request.urlopen(white_image_line.strip()[3:])

                black_image = "kingtemp.png"
                white_image = "Drunk-Rook-W.png"

                PieceDatabase.piece_display[number] = {
                    "name": name,
                    "tier": tier,
                    "cost": cost,
                    "images": [black_image, white_image]
                }
                

            