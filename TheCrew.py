"""TheCrew
Class TheCrew represents the state of the game. It should include the following components::
- Playing Cards
- Tasks
- Communications
- Commander
- Missions

We EXCLUDE the following components:
- Task tokens
- Distress signal
- Special mission rules
"""
from Player import Player
import random as rnd

class TheCrew:
    """The Crew class contains a representation of a game in progress.
    Also controls the flow of the game.
    """

    allCards = []
    allTasks = []
    allMissions = []
    allPlayers = {}
    nPlayers = 3

    def __init__(self, strategies=None):
        """Initialize game components
        """
        if strategies is None:
            strategies = ['rand', 'rand', 'rand']
        """Create card and task decks
        """
        print('Preparing game components...')
        colors = ['blue', 'green', 'pink', 'yellow']
        numbers = range(1, 10)
        for c in colors:
            for n in numbers:
                card = Card(c, n)
                self.allCards.append(card)
                self.allTasks.append(Task(card))
        for n in range(1, 5):
            self.allCards.append(Card('black', n))

        """Create missions
        """
        self.allMissions = range(1, 10)

        """Create players
        """
        print('Seating players...')
        self.nPlayers = len(strategies)
        for n in range(self.nPlayers):
            self.allPlayers[str(n)] = Player(str(n), strategies[n])
    
    def sanity(self):
        """Debug Tool
        """
        print(self.allPlayers)
    
    def playtrick(self, active_p, tasks_in_play, num_cards_left):
        """Plays a single Trick.
        - Starting with starting player, communicate 1 card
        - Play 1 card
        - Determine winner
        - Add played cards to winner's wonCards
        - Resolve tasks
        """
        turn = int(active_p)
        # TODO: COMMUNICATIONS
        """
        print('Communicating...')
        
        comms = 0
        while comms < self.nPlayers:
            active_p = str(turn % self.nPlayers)
            comm_card = self.allPlayers[active_p].selectcomm()"""

        """Play 1 card each
        """
        played_cards = []
        winner_card = None
        winner_p = None
        while len(played_cards) < self.nPlayers:
            active_p = str(turn % self.nPlayers)
            played_cards.append(self.allPlayers[active_p].selectcard())
            num_cards_left -= 1
            turn += 1

            """Determine winner
            """
            if winner_card is None or played_cards[-1] > winner_card:
                winner_card = played_cards[-1]
                winner_p = active_p
        print(f'Player {winner_p} won the trick!')
        """Add played cards to winner's wonCards
        Resolve tasks
        """
        # TODO: EARLY CHECK FOR LOSS
        for card in played_cards:
            self.allPlayers[winner_p].winPile.append(card)
            if card in self.allPlayers[winner_p].ownTasks:
                print(f'Player {winner_p} completed task {card}!')
                self.allPlayers[winner_p].ownTasks.remove(card)
                tasks_in_play.remove(card)

        if len(tasks_in_play) == 0:
            return True
        elif num_cards_left < self.nPlayers:
            return False
        else:
            self.playtrick(winner_p, tasks_in_play, num_cards_left)
            return None
    
    def playmission(self, mission=1):
        """Plays a single Mission.
        - Deal all the cards
        - Determine commander
        - Offer sample of Tasks
        - Starting with commander, select tasks
        - Play Tricks until mission completes
        """
        print(f'Playing mission {mission}!')
        """Deal cards
        """
        print('Dealing cards...')
        deck_cards = self.allCards.copy()
        rnd.shuffle(deck_cards)
        id_commander = '0'
        n_commander = 0

        while len(deck_cards) > 0:
            for p in self.allPlayers.values():
                if len(deck_cards) > 0:
                    c = deck_cards.pop()
                    p.ownCards.append(c)
                    """Determine commander
                    """
                    if c == Card('black', 4):
                        id_commander = p.name
                        n_commander = int(p.name)
        print(f'Player {id_commander} is our commander this mission!')
        """Sample and select Tasks
        """
        print('Selecting tasks...')
        tasks_sample = rnd.sample(self.allTasks, mission)
        tasks_in_play = tasks_sample.copy()
        turn = n_commander
        while len(tasks_sample) > 0:
            active_p = str(turn%self.nPlayers)
            self.allPlayers[active_p].selecttask(tasks_sample)
            turn =+ 1

        """Play Tricks
        """
        num_cards_left = len(self.allCards)
        while mission < 10:
            if self.playtrick(id_commander, tasks_in_play, num_cards_left):
                print(f'Completed mission number {mission}! Proceeding...')
                mission += 1
                self.playmission(mission)
            elif mission == 10:
                print(f'Completed all missions!')
            else:
                print(f'Failed mission number {mission}!')
                break

    # TODO: History + data collection
    
class Card:
    """Represents the cards in The Crew.
    """

    def __init__(self, color='', value=0):
        self.color = color
        self.value = value
        
    def __str__(self):
        return f"{self.color} {self.value}"
    
    def __eq__(self, other):
        return (self.color == other.color) & (self.value == other.value)
    def __lt__(self, other):
        if self.color == other.color:
            return self.value < other.value
        return self.color != 'black'

    def __gt__(self, other):
        if self.color == other.color:
            return self.value > other.value
        return self.color == 'black'

class Task(Card):
    """Represents the Tasks in The Crew.
    """

    def __init__(self, card = Card()):
        super().__init__(card.color, card.value)
    
class Communication(Card):
    """Represents the Communications in The Crew.
    """

    def __init__(self, card = Card(), position = ''):
        super().__init__(card.color, card.value)
        self.card = card
        if position in ['top', 'middle', 'bottom']:
            self.position = position
        else:
            print('Invalid position for communication.')
    
    def __str__(self):
        match self.position:
            case 'top':
                return f'A {self.card} is their HIGHEST {self.color} card.'
            case 'middle':
                return f'A {self.card} is their ONLY {self.color} card.'
            case 'bottom':
                return f'A {self.card} is their LOWEST {self.color} card.'
            case _:
                return None
