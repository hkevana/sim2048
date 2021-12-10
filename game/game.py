from pygame import Surface
from pygame.font import SysFont
from utils.colors import get_color, t_fw
from game.gui import *

from utils.constants import (
#   btns    states
    up,     ai_playing,
    down,   human_playing,
    left,   initializing,
    right,  game_over,
    plyr,   paused,
    play,   stgs_state,
    reset,
    stgs_btn
)

import ai

# globals
min_swipe_dist = 100

class Game:
    def __init__(self, stgs, hScores):
        self.state = initializing
        self.board = Board(stgs, hScores[0][0])

        self.h_scores = hScores

        self.hud = HUD(stgs)
        self.stgs_hud = SettingsHud(stgs)

        self.ai_agent = ai.Agent(bonus=(True,False,True))

        self.pause_color = Surface((stgs.width, stgs.height - stgs.hud_h))
        self.pause_color.set_alpha(128)
        self.pause_color.fill((0, 0, 0))

        self.font = SysFont("", 48)
        self.font_color = get_color(t_fw)

        # functions to call when a button gets clicked
        self.btn_func = {
            up: self.swipe_up,
            right: self.swipe_right,
            down: self.swipe_down,
            left: self.swipe_left,
            play: self.play_pause,
            plyr: self.toggle_player,
            reset: self.reset_game,
            stgs_btn: self.toggle_stgs
        }

        self.state = human_playing

    def draw(self, screen):
        # draw board
        self.board.draw(screen)

        # draw pause screen
        if self.state == paused:
            screen.blit(self.pause_color, (0,0))
            text = self.font.render("Paused", True, self.font_color)
            rect = text.get_rect()
            rect.center = self.pause_color.get_rect().center
            screen.blit(text, rect)

        # draw hud
        if self.state == stgs_state:
            self.stgs_hud.draw(screen)
        else:
            self.hud.draw(screen, self.board.score, self.board.h_score, self.board.n_moves)

    def process_click(self, pos):
        if self.hud.collide_point(pos) and self.state != stgs_state:
            btn_clicked, arrow = self.hud.process_click(pos)

            if btn_clicked is not None:
                if not arrow or (arrow and self.state != ai_playing):
                    func = self.btn_func[btn_clicked.name]
                    func()

    def swipe_up(self):
        if not (self.state == paused or self.state == stgs_state):
            self.hud.arrows[0].clicked()
            self.board.swipe_up()

    def swipe_right(self):
        if not (self.state == paused or self.state == stgs_state):
            self.hud.arrows[3].clicked()
            self.board.swipe_right()

    def swipe_left(self):
        if not (self.state == paused or self.state == stgs_state):
            self.hud.arrows[1].clicked()
            self.board.swipe_left()

    def swipe_down(self):
        if not (self.state == paused or self.state == stgs_state):
            self.hud.arrows[2].clicked()
            self.board.swipe_down()

    """
    Calculates in which direction a swipe is oriented
    
    :arguments
        swipe_start (int,int) : x,y coordinates of start of swipe
        swipe_end (int,int) : x,y coordinates of end of swipe
        
    :returns
        bool : whether swipe gesture was processed
            processed means the game took an action based on swipe:
                hud swipe       - no effect, player must swipe on board for swipe to take effect
                diagonal swipe  - no effect, tries to minimize ambiguous swipes (minimal resistance)
                cardinal swipe  - swipe board in that direction (up, down, left, or right)
    """
    def process_swipe(self, swipe_start, swipe_end):
        if self.hud.collide_point(swipe_start) or self.state == ai_playing:
            return True

        sx,sy = swipe_start
        ex,ey = swipe_end

        # calculate direction and magnitude of swipe
        dx,dy = ex-sx, ey-sy
        mx,my = abs(dx), abs(dy)

        # try to not process diagonal swipes
        half_swipe = int(min_swipe_dist/2)
        if mx > half_swipe and my > half_swipe:
            return True
        else:
            # determine if swipe was greater in the x direction or y direction
            if mx > my:
                # determine if swipe was left or right
                if dx > min_swipe_dist:
                    self.swipe_right()
                    return True
                elif dx < -min_swipe_dist:
                    self.swipe_left()
                    return True
            else:
                # determine if swipe was up or down
                if dy > min_swipe_dist:
                    self.swipe_down()
                    return True
                elif dy < -min_swipe_dist:
                    self.swipe_up()
                    return True
        return False

    def play_pause(self):
        play_btn = self.hud.buttons[0]
        if play_btn.curr_frame == 1:
            self.state = paused
        else:
            plyr_btn = self.hud.buttons[2]
            self.state = human_playing if plyr_btn.curr_frame == 0 else ai_playing

    def reset_game(self):
        self.state = initializing

        self.board.init_board()

        self.hud.clear_buttons()

        self.state = human_playing

    def toggle_stgs(self):
        if self.state == stgs_state:
            self.state = human_playing
        else:
            self.state = stgs_state

    def toggle_player(self):
        if self.state == human_playing:
            self.state = ai_playing
        elif self.state == ai_playing:
            self.state = human_playing

    def clear_buttons(self):
        self.hud.clear_arrows()

    def update(self):
        self.clear_buttons()

        # if we are currently swiping, update the board
        if self.board.swiping_flag is not None:
            self.board.update()
        elif self.state == ai_playing:
            action_performed = self.ai_agent.choose_next_action(self.board)

            if not action_performed:
                self.board.game_over_flag = True

        self.check_game_over_flag()

    def check_game_over_flag(self):
        if self.board.game_over_flag and self.state != game_over:
            self.state = game_over
            self.h_scores.append((self.board.score, self.board.n_moves, self.board.max_tile, self.ai_agent.w_i, self.ai_agent.look_ahead))

