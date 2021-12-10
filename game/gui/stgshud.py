from pygame import Rect, draw

from utils.colors import get_color
from utils.constants import t_stg_bg, t_fb, t_fw

class SettingsHud:
    def __init__(self, stgs):
        self.bg_color = get_color(t_stg_bg)
        self.rect = Rect(0, stgs.height - stgs.hud_h, stgs.width, stgs.hud_h)

        self.line_color = get_color(t_fb)
        self.text_color = get_color(t_fw)

    def draw(self, screen):
        draw.rect(screen, self.bg_color, self.rect)
        draw.line(screen, self.line_color, self.rect.topleft, self.rect.topright, 5)
