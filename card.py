from enum import Enum
import os

class CardType(Enum):
    SUSPECT = 1
    WEAPON = 2
    LOCATION = 3

class GameCard:
    def __init__(self, card_type, name, image_ref):
        self.displayName = name
        self.cardType = card_type
        self.image_path = os.path.join("Assets", "Cards", image_ref)

class ClueCard:
    def __init__(self, title, action, subtitle = None):
        self.title = title
        self.action = action
        self.subtitle = subtitle
