from pygame.sprite import Sprite
from pygame import font
from pygame.transform import scale

from utils.colors import get_color
from utils.constants import t_fb, t_fw, transparent
from utils.sheet import assets

border_w = 5
norm_size = 100
max_size = 120

class Tile(Sprite):
    def __init__(self, num=0, fw=True):
        super(Tile, self).__init__()

        self.image = assets.image_at((0,80,100,100), transparent)
        self.rect = self.image.get_rect()

        c = t_fw if fw else t_fb
        self.font_color = get_color(c)
        self.bg_color = get_color(num)

        self.number = num

        self.font = font.SysFont("", 40)

        self.merged_flag = False

        if num > 0:
            self.color_square()

    def color_square(self):
        w,h = self.image.get_size()
        border_color = self.image.get_at((0,5))
        for y in range(border_w, h - border_w):
            for x in range(border_w, w - border_w):
                if self.image.get_at((y,x)) != border_color:
                    self.image.set_at((y,x), self.bg_color)

    def position(self, screenPos):
        self.rect.center = screenPos

    def draw(self, screen, anim=False):
        # draw square
        screen.blit(self.image, self.rect)

        # draw the number if it has one
        if self.number > 0 and not anim:
            text = self.font.render(str(self.number), True, self.font_color)
            rect = text.get_rect()
            rect.center = self.rect.center
            screen.blit(text, rect)

# TODO: combine this class into the Tile class
class Square:
    def __init__(self, pos):
        self.pos = pos
        self.center = pos

        self.number = 0
        self.merged_flag = False

        self.merging = False
        self.growing = False

        self.size = 100

    def init_tile(self):
        self.number = 0
        self.merged_flag = False

        self.merging = False
        self.growing = False

        self.size = 100

    def init_grow(self):
        self.growing = True
        self.size = 0

    def anim_grow(self):
        self.size += 25
        if norm_size <= self.size:
            self.growing = False
            self.pos = self.center
        x,y = self.center
        self.pos = x + int((norm_size - self.size)/2), y + int((norm_size - self.size)/2)
        return Tile(self.number, False)

    def init_merge(self):
        self.merged_flag = True
        self.growing = True
        self.merging = True
        self.size = 100

    def anim_merge(self):
        if self.growing:
            self.size += 10
            if max_size <= self.size:
                self.growing = False
        else:
            self.size -= 10
            if norm_size >= self.size:
                self.merging = False
                self.pos = self.center

        dxy = int((self.size - norm_size)/2)
        x,y = self.center
        self.pos = x - dxy, y-dxy

        clr = True if self.number > 4 else False
        return Tile(self.number, clr)
# END SQUARE CLASS