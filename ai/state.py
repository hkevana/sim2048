import numpy as np

class Square:
    def __init__(self, num=0):
        self.number = num
        self.merged_flag = False


class State:

    def __init__(self, tiles, depth, direction):
        self.tiles = tiles
        self.depth = depth
        self.parent_dir = direction

    def get_tile(self, pos):
        x,y = pos
        return self.tiles[y,x]

    def set_tile(self, n, pos):
        x,y = pos
        self.tiles[y,x] = n

    def copy(self):
        return State(np.copy(self.tiles), self.depth, self.parent_dir)

    def __str__(self):
        out = "State:"
        for row in self.tiles:
            out += "\n\t"
            for item in row:
                out += "{:4d} ".format(item)
        return out



