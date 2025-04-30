import random as rand

class Strategy:
    """Stategy will be an inheritable class that 
    contains the algorithms controlling the player's moves.
    """
    def __init__(self, strat=''):
        self.strat = strat

class RandomStrategy(Strategy):
    # TODO
    def __init__(self, strat='rand'):
        super().__init__(strat)

class GreedyStrategy(Strategy):
    # TODO
    def __init__(self, strat='greedy'):
        super().__init__(strat)

class LocalBeamSearchStrategy(Strategy):
    # TODO
    def __init__(self, strat='lbs'):
        super().__init__(strat)