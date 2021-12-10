from game.gui.square import Tile,Square
from random import random, randint
from pygame.transform import scale
from pygame.mixer import Sound
from utils.colors import colors
from utils.constants import (
    up, up_tiles,
    down, down_tiles,
    right, right_tiles,
    left, left_tiles,
    norm_size,
    max_size,
    n_rows, n_cols,
    max_tiles,
    prob_four_tile
)

# board globals and hyper parameters
all_tiles = {}

def init_tiles():

    for k in colors:
        if isinstance(k, int):
            if k == 2 or k == 4:
                all_tiles[k] = Tile(k, False)
            else:
                all_tiles[k] = Tile(k)

class Board:

    def __init__(self, stgs, hScore, enable_sd=True):
        # initialize all tiles
        init_tiles()

        # set up spacing reqs
        self.pad = stgs.pad

        self.tiles = [[Square(self.pos_to_screen(x,y)) for x in range(4)] for y in range(4)]
        self.n_tiles = 0

        # hud numbers
        self.n_moves = 0
        self.score = 0
        self.h_score = hScore

        self.max_tile = 0

        self.init_board()
        self.game_over_flag = False

        self.enable_sd = enable_sd
        self.swipe_sd = Sound("assets/sounds/swipe.wav")
        self.swipe_sd.set_volume(.1)
        self.merge_sd = Sound("assets/sounds/merge.wav")
        self.merge_sd.set_volume(.05)

        self.swipe_tile_move_flag = False
        self.swiping_flag = None
        self.swipe_order = None

    def init_board(self):
        # track all tiles and their positions
        for row in self.tiles:
            for tile in row:
                tile.init_tile()

        self.n_tiles = 0    # track number of tiles currently on board
        self.n_moves = 0    # track number of moves
        self.score = 0

        # start game with two tiles
        self.gen_random_new_tile()
        self.gen_random_new_tile()

    """
    Draw the board to the screen
    
    :argument
        screen (pygame.Surface) : surface on which to draw the board
    """
    def draw(self, screen):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                tile = self.tiles[y][x]
                anim = False
                t = all_tiles[tile.number]
                if tile.merging:
                    t = tile.anim_merge()
                    t.image = scale(t.image, (tile.size, tile.size))
                    anim = True
                elif tile.growing:
                    # blit the background tile
                    t = all_tiles[0]
                    t.position(tile.center)
                    t.draw(screen)

                    # animate the growing tile
                    t = tile.anim_grow()
                    t.image = scale(t.image, (tile.size, tile.size))
                    anim = True

                t.position(tile.pos)
                t.draw(screen, anim)

    def update(self):
        self.swipe()

    def swipe_up(self):
        if self.swiping_flag is None:
            self.init_swipe(up, up_tiles)

    def swipe_right(self):
        if self.swiping_flag is None:
            self.init_swipe(right, right_tiles)

    def swipe_left(self):
        if self.swiping_flag is None:
            self.init_swipe(left, left_tiles)

    def swipe_down(self):
        if self.swiping_flag is None:
            self.init_swipe(down, down_tiles)

    def init_swipe(self, flag, order):
        self.swiping_flag = flag
        self.swipe_order = order
        self.swipe_tile_move_flag = False
        self.unset_merged_flags()

    def swipe(self):
        order = self.swipe_order
        direction = self.swiping_flag
        dx,dy = direction
        tile_moved = False
        for pos in order:
            src_tile = self.get_tile(pos)
            if src_tile.number != 0:
                x, y = pos
                moved = self.move_tile((x,y), (x+dx,y+dy))

                if moved:
                    tile_moved = True
                    self.swipe_tile_move_flag = True

        if not tile_moved:
            if self.swipe_tile_move_flag:
                if self.enable_sd:
                    Sound.play(self.swipe_sd)
                self.n_moves += 1
                self.gen_random_new_tile()
            self.swiping_flag = None
            self.swipe_order = None
            self.check_gameover()


    def get_tile(self, pos):
        x,y = pos
        return self.tiles[y][x]

    def set_tile(self, n, pos):
        x,y = pos
        self.tiles[y][x].number = n

    def set_tile_merge_flag(self, pos):
        x,y = pos
        self.tiles[y][x].merged_flag = True

    def tile_merged_already(self, pos):
        x,y = pos
        return self.tiles[y][x].merged_flag

    def unset_merged_flags(self):
        for row in self.tiles:
            for t in row:
                if t is not None:
                    t.merged_flag = False


    def move_tile(self, src, dest):
        dx,dy = dest
        # bounds check - is dest still on the board?
        if dx < 0 or dy < 0 or dx >= n_rows or dy >= n_cols:
            return False

        dest_tile = self.get_tile(dest)

        if dest_tile.number == 0:
            src_tile = self.get_tile(src)
            self.set_tile(src_tile.number, dest)

            self.set_tile(0, src)

            return True
        else:
            return self.merge_tiles(src, dest)

    def merge_tiles(self, src, dest):
        src_tile = self.get_tile(src)
        dest_tile = self.get_tile(dest)

        if not self.tile_merged_already(src) and dest_tile.number == src_tile.number:
            # TODO: find better merging sound
            # if self.enable_sd:
            #     Sound.play(self.merge_sd)
            new_val = dest_tile.number+src_tile.number
            self.set_tile(new_val, dest)
            dest_tile.init_merge()

            self.set_tile(0, src)

            self.n_tiles -= 1
            self.score += new_val

            if new_val > self.max_tile:
                self.max_tile = new_val
            if self.score > self.h_score:
                self.h_score = self.score

            return True
        return False

    def check_gameover(self):
        if self.n_tiles < max_tiles:
            self.game_over_flag = False
        else:
            # TODO: check if game is over
            pass


    """
    Generates a new tile to be randomly placed on board
    Generation Probability:
        2 - 90%
        4 - 10%
        
    :returns    
        bool : whether a new tile was placed
    """
    def gen_random_new_tile(self):
        if self.n_tiles < max_tiles:
            num = 2
            if random() < prob_four_tile:
                num = 4

            pos = self.find_unoccupied_square()
            self.set_tile(num, pos)
            tile = self.get_tile(pos)
            tile.init_grow()

            self.n_tiles += 1
            return True
        return False

    """
    Ensure new tile is placed on an unoccupied square
    """
    def find_unoccupied_square(self):
        x,y = randint(0, n_rows - 1), randint(0, n_cols - 1)
        while self.tiles[y][x].number != 0:
            x, y = randint(0, n_rows - 1), randint(0, n_cols - 1)

        return x,y

    """
    Convert pos (x,y) to actual screen coordinate (pixels)
    
    :arguments
        x (int) : x position to convert
        y (int) : y position to convert
    """
    def pos_to_screen(self, x, y):
        px = (self.pad + ((x % 4) * (self.pad + norm_size))) + int(norm_size/2)
        py = (self.pad + ((y % 4) * (self.pad + norm_size))) + int(norm_size/2)
        return px, py