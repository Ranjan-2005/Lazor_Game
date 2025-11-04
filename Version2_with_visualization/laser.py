class Laser:
    """
    Class modeling the behavior of a laser beam.
    """
    def __init__(self, start, direction):
        self.start = start
        self.x = start[0]
        self.y = start[1]
        self.dx = direction[0]
        self.dy = direction[1]
        self.coordinates = [start]
        self.refract = False
        self.edge = 0

    def movelaser(self):
        self.x += self.dx
        self.y += self.dy
        self.coordinates.append((self.x, self.y))

    def OutsideBoundary(self, shape):
        height, width = shape
        x_OB = not (0 <= self.x < height)
        y_OB = not (0 <= self.y < width)
        if x_OB or y_OB:
            return True
        if (self.x == height - 1 and self.dx == 1) or (self.x == 0 and self.dx == -1):
            return True
        if (self.y == width - 1 and self.dy == 1) or (self.y == 0 and self.dy == -1):
            return True
        return False
