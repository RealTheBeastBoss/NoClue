import pygame

class Location:
    def __init__(self, name, center, *shape_corners):
        self.displayName = name
        self.card = None
        self.canReach = False
        self.enterSquares = None
        self.center = center
        self.corners = shape_corners[:-1]
        self.edges = []
        for x in range(len(shape_corners) - 1):
            self.edges.append((shape_corners[x][0], shape_corners[x][1], shape_corners[x + 1][0], shape_corners[x + 1][1]))

class Square:
    def __init__(self, x, y):
        self.square = (x, y)
        self.topLeft = (55 + (x * 43), 3 + (y * 43))
        self.canReach = False
        self.currentRect = pygame.Rect(self.topLeft, (42, 42))
