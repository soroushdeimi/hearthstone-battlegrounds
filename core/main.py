import pygame
import sys


class GameController:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hearthstone Battlegrounds Simulator")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.game_state = "RECRUIT"
        self.debug_status = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.debug_status = not self.debug_status
    def update(self):
        pass
    def draw(self):
        self.screen.fill((30,30,30))
        color = (0,255,0)
        if self.debug_status:
            color
        else:
            (255,0,0)

        pygame.draw.rect(self.screen , color , (500, 350, 100, 140))

        font = pygame.font.SysFont(None, 24)
        img = font.render("PRESS SPACE TO TOGGLE DEBUG STATUS (GREEN/RED)" , True, (255,255,255))
        self.screen.blit(img , (20,20))

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

game = GameController()
game.run()