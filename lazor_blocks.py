class Block:
    def interact(self, pos, direction):
        raise NotImplementedError

class ReflectBlock(Block):
    def interact(self, pos, direction):
        dx, dy = direction
        return [(-dx, -dy)]

class OpaqueBlock(Block):
    def interact(self, pos, direction):
        return []

class RefractBlock(Block):
    def interact(self, pos, direction):
        return [direction, (-direction[0], -direction[1])]