from game import *

class Player:
    def __init__(self, num, name):
        self.playerName = name
        self.playerNumber = num
        self.playerColour = None
        self.cards = []
