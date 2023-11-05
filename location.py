import pygame

class Location:
    def __init__(self, card, center, squares, stands, *corners):
        self.displayName = card.displayName
        self.card = None
        self.ref = card
        self.enterSquares = squares
        self.player_to_point = stands
        self.center = center
        self.passage = None
        self.corners = corners[:-1]
        self.edges = []
        for x in range(len(corners) - 1):
            self.edges.append((corners[x][0], corners[x][1], corners[x + 1][0], corners[x + 1][1]))

class Square:
    def __init__(self, x, y):
        self.square = (x, y)
        self.topLeft = (55 + (x * 43), 3 + (y * 43))
        self.currentRect = pygame.Rect(self.topLeft, (42, 42))
