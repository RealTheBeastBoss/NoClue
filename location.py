class Location:
    def __init__(self, name, *shape_corners):
        self.displayName = name
        self.card = None
        self.corners = shape_corners
        self.edges = []
        for x in range(len(shape_corners) - 1):
            self.edges.append((shape_corners[x][0], shape_corners[x][1], shape_corners[x + 1][0], shape_corners[x + 1][1]))
