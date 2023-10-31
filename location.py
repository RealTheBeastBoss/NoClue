import os

class Location:
    def __init__(self, name, image_ref, topleft, *shape_corners):
        self.displayName = name
        self.imagePath = os.path.join("Assets", "Board", image_ref)
        self.topLeft = topleft
        self.edges = []
        for x in range(len(shape_corners) - 1):
            self.edges.append((shape_corners[x][0], shape_corners[x][1], shape_corners[x + 1][0], shape_corners[x + 1][1]))
