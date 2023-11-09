from enum import Enum

class CardType(Enum):
    SUSPECT = 1
    WEAPON = 2
    LOCATION = 3

class GameCard:
    def __init__(self, card_type, name):
        self.displayName = name
        self.cardType = card_type

class ClueCard:
    def __init__(self, title, action, subtitle = None, card = None):
        self.title = title
        self.action = action
        self.subtitle = subtitle
        self.card = card
