from game import *

PLAYER_TO_START = {
    0: SCARLETT_START,
    1: MUSTARD_START,
    2: ORCHID_START,
    3: GREEN_START,
    4: PEACOCK_START,
    5: PLUM_START
}

PLAYER_TO_NAME = {
    0: "Miss Scarlett",
    1: "Col. Mustard",
    2: "Dr Orchid",
    3: "Rev. Green",
    4: "Mrs Peacock",
    5: "Prof. Plum"
}

class Player:
    def __init__(self, num):
        self.playerNumber = num
        self.playerIndex = None
        self.playerName = PLAYER_TO_NAME[num]
        self.location = PLAYER_TO_START[num]
        self.playerColour = PLAYER_TO_COLOUR[num]
        self.playerDied = False
        self.cards = []
