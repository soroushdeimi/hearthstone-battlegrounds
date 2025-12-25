import pygame
from src.title_screen import Title
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screens = {}
        self.current_screen = None

        self.screen = pygame.display.set_mode((900, 600))
        self.clock = pygame.time.Clock()
        self.f = 60
        self.r = True # game is runing

        self.screens["title"] = Title(self.screen, self.change_scr)
        self.change_scr("title")

    def run(self):
        while(self.r):
            self.clock.tick(self.f)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.r = False
            if self.current_screen is not None:
                self.current_screen.handle_events(events)
                self.current_screen.updates()
                self.current_screen.render(self.screen)
            else:
                self.screen.fill((0, 0, 0))

            pygame.display.flip()
        pygame.quit()

    def change_scr(self, name_scr):
        self.current_screen = self.screens[name_scr]


