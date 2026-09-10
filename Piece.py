from AttributeModules.AttributeModule import AttributeModule
from AttributeModules.InternalAttributeModule import InternalAttributeModule
from ConditionCheckModules.ConditionCheckModule import ConditionCheckModule
from MovementModules.MovementModule import MovementModule
from TriggerModules.TriggerModule import TriggerModule

class Piece:

    condition_check_defaults = {
        "capturable": lambda p, s, b, c=None : not "T" in p.get_attribute_values("tier") and \
            (c is None or p.colour != c.colour),
        "standable": lambda p, s, b, c=None : "T" in p.get_attribute_values("tier"),
        "blocksmovement": lambda p, s, b, c=None: not "T" in p.get_attribute_values("tier"),
        "ismovable": lambda p, s, b, c=None: b.to_move == p.colour,
    }

    def __init__(self, modules, colour):

        # Colour is "B" for Black, "W" for White

        self.colour = colour
        self.modules = modules
        self.moves = 0
        self.damaged = 0

    def get_legal_moves(self, square, board):

        valid_moves = []
        # Move format is (square x, square y, (functions to run as part of move & arguments))
        invalid_moves = []
        # Invalid moves are formatted (square x, square y, condition to check (argument of the move))

        for module in self.modules:

            if issubclass(type(module), MovementModule):

                valid_moves.extend(module.get_legal_moves(square, self.colour, board, self))
                invalid_moves.extend(module.get_illegal_moves(square, self.colour, board, self))

        for invalid_move in invalid_moves:

            for move in valid_moves:

                if invalid_move[0] == move[0] and invalid_move[1] == move[1] and not invalid_move[2](move):

                    valid_moves.remove(move)

        return list(set(valid_moves))

    def get_attribute_values(self, attribute):

        found_values = []

        for module in self.modules:

            if issubclass(type(module), AttributeModule):

                value = module.get_attribute(attribute)

                if not value is None:

                    found_values.append(value)

        return found_values

    def check_condition(self, condition, square, board, culprit = None):

        condition_met = Piece.condition_check_defaults.get(condition, lambda p, s, b, c=None: False)(self, square, board, culprit)

        for module in self.modules:

            if issubclass(type(module), ConditionCheckModule) and module.checks_condition(condition):

                result = module.conditions.get(condition, lambda p, s, b, c=None: None)(self, square, board, culprit)

                if result is not None:

                    condition_met = result

        return condition_met

    def run_trigger(self, trigger, square, board, culprit = None):

        results = []

        for module in self.modules:

            if issubclass(type(module), TriggerModule):

                if module.can_trigger(trigger):

                    results.append(module.ability(self, square, board, culprit))

        return results

    def __hash__(self):

        hashables = []

        for module in self.modules:

            if issubclass(type(module), AttributeModule) \
                and not issubclass(type(module), InternalAttributeModule):

                hashables.append(frozenset([(att, module.attributes[att]) for att in module.attributes.keys()]))

        return hash(frozenset(hashables))
        