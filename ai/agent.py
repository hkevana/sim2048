from time import time
from ai.state import State

from random import random,randint
import numpy as np

from ai.queue import PriorityQueue
from utils.weights import get_weights
from utils.constants import (
    up, up_tiles,
    down, down_tiles,
    right, right_tiles,
    left, left_tiles,
    n_rows, n_cols,
    max_tiles,
    prob_four_tile
)

debug = False


class Agent:

    def __init__(self, weights=3, bonus=(False,False,False), look=2, delay=0.0):
        self.delay = delay
        self.look_ahead = look
        self.last_action = 0
        self.w_i = weights
        self.weights = get_weights(weights)

        self.merge_bonus, self.align_bonus, self.corner_bonus = bonus

        self.queue = PriorityQueue()

        self.scores = [0,0,0,0] # score for swiping up, right, down, left
        self.flags = [[False for _ in range(4)] for _ in range(4)]
        self.curr_state = None
        self.save_state = None

    def choose_next_action(self, board):
        if time() - self.last_action > self.delay:

            self.init_descent(board)
            self.descend()

            self.last_action = time()
            return self.perform_action(board)
        return True


    def set_state(self):
        self.flags = [[False for _ in range(4)] for _ in range(4)]
        self.curr_state = self.save_state.copy()

    def get_score(self):
        m = np.multiply(self.curr_state.tiles, self.weights)

        if debug:
            print("\nScore matrix:")
            print(m)

        return int(np.sum(m))

    def init_descent(self, board):
        self.save_state = self.queue.reinit(board.tiles)
        if debug:
            print("\n\n----INITIAL STATE----")
            print(self.save_state)

        self.scores = [0,0,0,0]

        self.swipe_up(0)
        self.swipe_right(1)
        self.swipe_down(2)
        self.swipe_left(3)

    def descend(self):
        depth = 1
        while self.queue.length > 0:
            self.save_state = self.queue.pop()
            depth = self.save_state.depth

            if debug:
                print("-- {} -- {} --".format(depth, self.look_ahead))
                print("\n\n----INITIAL STATE----")
                print(self.save_state)

            if depth >= self.look_ahead:
                break

            swipe = self.save_state.parent_dir
            self.swipe_up(swipe)
            self.swipe_right(swipe)
            self.swipe_down(swipe)
            self.swipe_left(swipe)


    def pick_best_action(self):
        print("[{:8d} {:8d} {:8d} {:8d}] ---> ".format(*self.scores), end="")
        index = 0
        max_score = self.scores[index]

        for i in range(1, len(self.scores)):
            if self.scores[i] > max_score:
                index = i
                max_score = self.scores[i]

        if max_score == 0:
            return -1
        return index

    def perform_action(self, board):
        best = self.pick_best_action()

        # no action can be performed
        if best == -1:
            print("nop")
            return False

        # perform best action
        if best == 0:
            board.swipe_up()
            print("up")
        elif best == 1:
            board.swipe_right()
            print("right")
        elif best == 2:
            board.swipe_down()
            print("down")
        elif best == 3:
            board.swipe_left()
            print("left")
        return True

    def swipe_up(self, swipe):
        if debug:
            print("\n----UP----", end="")
        self.swipe(up, up_tiles, swipe)

    def swipe_right(self, swipe):
        if debug:
            print("\n----RIGHT----", end="")
        self.swipe(right, right_tiles, swipe)

    def swipe_left(self, swipe):
        if debug:
            print("\n----LEFT----", end="")
        self.swipe(left, left_tiles, swipe)

    def swipe_down(self, swipe):
        if debug:
            print("\n----DOWN----", end="")
        self.swipe(down, down_tiles, swipe)

    def swipe(self, direction, order, swipe):
        if debug:
            txt = "up" if swipe==0 else "right" if swipe==1 else "down" if swipe==2 else "left"
            print(" {}".format(txt))
        self.set_state()

        dx, dy = direction
        tile_moved = False
        tiles_merged = 0
        for pos in order:
            src_tile = self.get_tile(pos)
            if src_tile != 0:
                x, y = pos

                moved = True
                while moved:
                    moved, merged = self.move_tile((x, y), (x + dx, y + dy))
                    x += dx
                    y += dy

                    if moved:
                        tile_moved = True
                        if self.merge_bonus:
                            tiles_merged += merged

        if debug:
            print(self.curr_state)
        if tile_moved:
            # board was changed
            state = State(self.curr_state.tiles, self.curr_state.depth+1, swipe)
            self.queue.push(state)

            new_score = (self.get_score() + tiles_merged)
            if self.corner_bonus:
                bonus = self.calc_corner_bonus()
                new_score -= bonus

            old_score = self.scores[swipe]

            if new_score > old_score:
                self.scores[swipe] = new_score

    def get_tile(self, pos):
        return self.curr_state.get_tile(pos)

    def set_tile(self, pos, n):
        return self.curr_state.set_tile(n, pos)

    def set_tile_merge_flag(self, pos):
        x, y = pos
        self.flags[y][x] = True

    def tile_merged_already(self, pos):
        x, y = pos
        return self.flags[y][x]

    def move_tile(self, src, dest):
        dx, dy = dest
        # bounds check - is dest still on the board?
        if dx < 0 or dy < 0 or dx >= n_rows or dy >= n_cols:
            return False, 0

        dest_tile = self.get_tile(dest)

        # Try to merge is destination is occupied
        if dest_tile != 0:
            return self.merge_tiles(src, dest)

        # Otherwise simply move src tile to dest
        src_tile = self.get_tile(src)
        self.set_tile(dest, src_tile)

        self.set_tile(src, 0)

        return True, 0

    def merge_tiles(self, src, dest):
        src_tile = self.get_tile(src)
        dest_tile = self.get_tile(dest)

        if not self.tile_merged_already(src) and dest_tile == src_tile:
            new_val = dest_tile + src_tile
            self.set_tile(dest, new_val)
            self.set_tile(src, 0)

            return True, new_val * 2
        return False, 0

    def calc_corner_bonus(self):
        corner = self.curr_state.tiles[0,0]
        for y in range(0, len(self.curr_state.tiles)):
            for x in range(0, len(self.curr_state.tiles)):
                if self.curr_state.tiles[y,x] > corner:
                    return self.curr_state.tiles[y,x] * 2
        return 0



