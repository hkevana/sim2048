from pygame import Rect, draw, font, transform
from game.gui.button import Button

from utils.colors import get_color
from utils.constants import t_hud_bg, t_fb, t_fw, up, down,left,right,play,plyr,reset,stgs_btn

class HUD:
    def __init__(self, stgs):
        # setup HUD background
        self.bg_color = get_color(t_hud_bg)
        self.rect = Rect(0, stgs.height - stgs.hud_h, stgs.width, stgs.hud_h)

        # create hud buttons
        """
            Set up positional variables for buttons:
            x,y - topleft corner of first button relative to hud background
            pad - distance between borders and buttons
            sp - used to center player button below the play and reset button
        """
        x,y = self.rect.topleft
        w = stgs.btn_size_sm
        pad = stgs.hud_pad

        self.pad = pad
        self.btn_size = stgs.btn_size_sm

        # track all buttons in one list
        self.buttons = [
            # used to start and stop AI automatic play
            Button(play, (x + pad, y + pad), stgs.btn_size_sm, 2),
            # used to restart the game from the beginning
            Button(reset, (x + (pad * 2) + w, y + pad), stgs.btn_size_sm, 1),
            # used to identify if the player or the AI is playing
            Button(plyr, (x + pad, y + pad * 3), stgs.btn_size_lg, 2),
            Button(stgs_btn, (x + pad, y + pad * 5), stgs.btn_size_sm, 1)
        ]

        # arrow buttons used to swipe
        self.arrows = []    # order: up, left, down, right
        self.init_arrows(int(stgs.width/2) - int(stgs.btn_size_sm/2), self.rect.centery - int(stgs.btn_size_sm/2), stgs.btn_size_sm)

        # add arrows into buttons list
        self.buttons.extend(self.arrows)

        # score boxes
        self.blk_btn = Button("blank", (0,0), stgs.btn_size_lg, 1)
        self.blk_btn.image = transform.scale(self.blk_btn.image, (int(stgs.btn_size_lg*2), stgs.btn_size_sm))
        self.blk_btn.rect = self.blk_btn.image.get_rect()
        self.blk_btn.rect.topleft = (self.rect.right-125, self.rect.top+pad)

        # fonts
        self.text_font = font.SysFont("", 24)
        self.text_color = get_color(t_fw)

        self.num_font = font.SysFont("", 32)
        self.number_color = get_color(t_fb)

    def init_arrows(self, cx, cy, btn_size):
        # pos elements: x,y coordinates with angle to rotate and arrow id
        pos = [(0,-btn_size,0, up), (-btn_size,0,90, left), (0,btn_size,180, down), (btn_size,0,-90, right)]
        for x,y,a,name in pos:
            arrow = Button("arrow", (cx+x, cy+y), btn_size, 2, name)
            arrow.rotate(a)
            self.arrows.append(arrow)



    def draw(self, screen, score, hScore, moves):
        # draw hud background
        draw.rect(screen, self.bg_color, self.rect)
        draw.line(screen, self.number_color, self.rect.topleft, self.rect.topright, 5)

        # draw all the buttons
        for b in self.buttons:
            screen.blit(b.image, b.rect)

        # draw the info boxes
        self.draw_info_boxes(screen, score, hScore, moves)

    def draw_info_boxes(self, screen, score, hScore, moves):
        # draw the info boxes
        x,y,w,h = self.blk_btn.rect
        self.draw_info_box(screen, self.blk_btn.image, Rect(x,y,w,h), "Score", str(score))
        self.draw_info_box(screen, self.blk_btn.image, Rect(x, y+self.pad+self.btn_size, w, h), "Moves", str(moves))
        self.draw_info_box(screen, self.blk_btn.image, Rect(x, y + (self.pad + self.btn_size) * 2, w, h), "High Score", str(hScore))

    def draw_info_box(self, screen, image, rect, header, txt):
        screen.blit(image, rect)

        hdr = self.text_font.render(header, True, self.text_color)
        hdr_rect = hdr.get_rect()
        hdr_rect.center = rect.midtop
        hdr_rect.y -= 10

        screen.blit(hdr, hdr_rect)

        txt = self.num_font.render(txt, True, self.number_color)
        txt_rect = txt.get_rect()
        txt_rect.center = rect.center

        screen.blit(txt, txt_rect)

    def collide_point(self, pos):
        return self.rect.collidepoint(pos)

    def process_click(self, pos):
        for b in self.buttons:
            if b.collide_point(pos):
                b.clicked()
                return b, b in self.arrows
        return None

    def clear_buttons(self):
        for b in self.buttons:
            b.set_frame(0)

    def clear_arrows(self):
        for a in self.arrows:
            a.set_frame(0)



