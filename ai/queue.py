from ai.state import State
import numpy as np

class PriorityQueue:

    def __init__(self):
        self.states = []
        self.length = 0

    def reinit(self, board):
        self.states.clear()
        self.length = 0

        tiles = np.array([[n.number for n in row] for row in board])

        return State(tiles, 0, -1)

    def push(self, board):
        self.states.append(board)
        self.length += 1

    def pop(self):
        index = 0
        min_dist = self.states[index].depth

        for i, state in enumerate(self.states):
            if state.depth < min_dist:
                index = i
                min_dist = state.depth

        return self.states.pop(index)





