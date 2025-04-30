import random as rand

class Player:
    """Player stores player-specific data. 
    It stores and maintains a personal knowledgebase and
    calls upon its strategy when deciding on moves.
    """

    def __init__(self, p_name='0', strat='rand'):

        self.name = p_name
        self.strat = strat
        self.ownCards = []
        self.ownTasks = []
        self.winPile = []
        self.usedComm = False

    def __str__(self):
        return f"Player {self.name} uses the {self.strat} strategy."

    def selectcard(self):
        match self.strat:
            case 'rand':
                card = rand.choice(self.ownCards)
                self.ownCards.remove(card)
                print(f'Player {self.name} chooses card {card}.')
                return card
            case _:
                return None

    def selecttask(self, deck_tasks):
        match self.strat:
            case 'rand':
                task = rand.choice(deck_tasks)
                self.ownTasks.append(task)
                deck_tasks.remove(task)
                print(f'Player {self.name} chooses task {task}.')
            case _:
                pass

    # TODO:
    #   COMMUNICATIONS
    #   KNOWLEDGEBASE
    #   Inference engine