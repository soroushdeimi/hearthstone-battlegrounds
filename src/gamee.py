

import pygame

from title_screen import Title
from hero_select import HeroSelect  
from gameplay import Gameplay
from recruit_screen import RecruitScreen

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("Hearthstone Battlegrounds")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        self.screens = {}
        self.current_screen = None

        self.screens["title"] = Title(self.screen, self.change_screen)
        self.screens["hero_select"] = HeroSelect(self.screen, self.change_screen)

        self.change_screen("title")
        self.screen = pygame.display.set_mode((900, 600))
        self.clock = pygame.time.Clock()
        self.f = 60
        self.r = True 

        self.hero_selected = None 
        self.screens["title"] = Title(self.screen, self.change_scr)
        self.screens["hero_select"] = HeroSelect(self.screen, self.change_scr)

    def change_screen(self, name, **kwargs):
        if name == "recruit" and "hero" in kwargs:
            self.screens["recruit"] = RecruitScreen(
                self.screen,
                self.change_screen,
                kwargs["hero"]
            )

        self.current_screen = self.screens.get(name)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.current_screen:
                self.current_screen.handle_events(events)
                self.current_screen.updates()
                self.current_screen.render(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
