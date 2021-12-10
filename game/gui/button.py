from pygame.transform import rotate, scale

from utils.sheet import assets
from utils.constants import transparent


button = {
    "play":     (0,    0),
    "pause":    (40,   0),
    "reset":    (120, 40),
    "player":   (0,   40),
    "arrow":    (80,   0),
    "blank":    (100, 80),
    "settings": (100,120)
}

btn_h = 40


class Button:
    def __init__(self, btn, pos, w, frames=1, name=None):
        x,y = button[btn]
        self.frames = assets.load_strip((x,y,w,btn_h), frames, transparent)

        self.curr_frame = 0
        self.n_frames = len(self.frames)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

        self.name = name if name is not None else btn


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, angle):
        frames = []
        for f in self.frames:
            frames.append(rotate(f, angle))
        self.frames = frames
        self.set_frame(0)

    def stretch(self, x, y):
        frames = []
        for f in self.frames:
            frames.append(scale(f, (x,y)))
        self.frames = frames
        self.set_frame(0)

    def collide_point(self, pos):
        return self.rect.collidepoint(pos)

    def set_frame(self, frame):
        self.curr_frame = frame
        self.image = self.frames[self.curr_frame]

    def clicked(self):
        self.set_frame((self.curr_frame + 1) % self.n_frames)
