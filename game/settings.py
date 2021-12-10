from utils.constants import *
from utils.colors import get_color

class Settings:
    def __init__(self):
        # screen settings
        self.width = 500
        self.height = 700
        self.size = self.width, self.height

        # board settings
        self.tile_size = 100
        self.pad = 20
        self.bg_color = get_color(t_bg)

        # hud settings
        self.hud_h = self.height - 500
        self.hud_pad = 25
        self.btn_size_sm = 40
        self.btn_size_lg = 60
        self.sound_on = True


