class ConditionCheckModule:

    def __init__(self, function_conditions, funcs):

        # funcs are each of signature (piece, square, board, culprit?) -> bool?
        # True = condition met, false = condition not met, none = default
        
        # Current possible conditions:
        # capturable, standable, blocksmovement
        
        self.conditions = {
            function_conditions[i] : funcs[i] 
            for i in range(len(function_conditions))
        }

    def checks_condition(self, condition):

        return condition in self.conditions.keys