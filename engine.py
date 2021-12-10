import pygame
import gc
from utils.constants import ai_playing

from game import *

class GameEngine:
    def __init__(self, scores_fp):
        self.scores_filepath = scores_fp

        pygame.init()
        pygame.mixer.init()

        self.stgs = Settings()

        self.screen = pygame.display.set_mode(self.stgs.size)
        self.clock = pygame.time.Clock()

        high_scores = self.load_scores()
        self.game = Game(self.stgs, high_scores)

        self.swipe_flag = False
        self.swipe_start = 0, 0

        self.running = False

    def process_input(self,):
        # TODO: Stop all swipes from moving board when paused
        # TODO: Add keyboard shortcuts to buttons: play/pause, restart, stgs, and player/AI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.game.state != ai_playing:
                    if event.key == pygame.K_UP:
                        self.game.swipe_up()

                    elif event.key == pygame.K_RIGHT:
                        self.game.swipe_right()

                    elif event.key == pygame.K_LEFT:
                        self.game.swipe_left()

                    elif event.key == pygame.K_DOWN:
                        self.game.swipe_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game.process_click(event.pos)
                self.swipe_flag = True
                self.swipe_start = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                self.swipe_flag = False

            elif event.type == pygame.MOUSEMOTION:
                if self.swipe_flag:
                    self.swipe_flag = not self.game.process_swipe(self.swipe_start, event.pos)

    def draw(self,):
        self.game.draw(self.screen)

    def update(self,):
        self.game.update()

    def start_mainloop(self):
        self.running = True

        while self.running:
            gc.collect()

            self.screen.fill(self.stgs.bg_color)

            self.process_input()
            self.draw()
            self.update()

            pygame.display.flip()
            self.clock.tick(25)

        pygame.quit()

        # write high scores to file
        self.save_scores()


    def load_scores(self):
        scores = []
        with open(self.scores_filepath, 'r') as file:
            for line in file.readlines():
                s, m, t, w, l = line.split()
                if s.isdigit():
                    scores.append((int(s),int(m), int(t), int(w), int(l)))

        return scores

    def save_scores(self):
        with open(self.scores_filepath, 'w') as file:
            self.game.h_scores.sort(reverse=True)
            file.write("{:10s} {:10s} {:10s} {:10s} {:10s}\n".format("Score", "Moves", "Max-Tile", "Weights", "Look-Ahead"))
            for i,t in enumerate(self.game.h_scores):
                s,m,h,w,l = t
                file.write("{:<10d} {:<10d} {:<10d} {:<10d} {:<10d}\n".format(s, m, h, w, l))
                # only write the top 10 scores

if __name__ == '__main__':

    # load high scores from file
    scores_filepath = "scores.txt"
    engine = GameEngine(scores_filepath)

    engine.start_mainloop()

