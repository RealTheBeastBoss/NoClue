from game import *

PLAYER_TO_START = {
    0: SCARLETT_START,
    1: MUSTARD_START,
    2: ORCHID_START,
    3: GREEN_START,
    4: PEACOCK_START,
    5: PLUM_START
}

class Player:
    def __init__(self, num):
        self.playerNumber = num
        self.playerIndex = None
        self.location = PLAYER_TO_START[num]
        self.playerColour = PLAYER_TO_COLOUR[num]
        self.cards = []
