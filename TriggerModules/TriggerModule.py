class TriggerModule:

    def __init__(self, condition_strings, func):

        self.ability = func
        # Ability is a procedure that takes arguments of piece, square, board, and culprit = None
        self.conditions = condition_strings
        # Current possible conditions:
        # captured, wascaptured, relocated
        # turnend, turnstart
        # gamestart, incheck, enemycheck

    def can_trigger(self, condition):

        return condition in self.conditions