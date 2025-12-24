import pygame
from src.title_screen import Title
from src.hero_select import HeroSelect  
from src.gameplay import Gameplay

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screens = {}
        self.current_screen = None
        self.screen = pygame.display.set_mode((900, 600))
        self.clock = pygame.time.Clock()
        self.f = 60
        self.r = True  # game is running

        self.hero_selected = None  # برای ذخیره هیرو انتخاب شده

        self.screens["title"] = Title(self.screen, self.change_scr)
        self.screens["hero_select"] = HeroSelect(self.screen, self.change_scr)

        self.change_scr("title")

    def run(self):
        while self.r:
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

    def change_scr(self, name_scr, **kwargs):
        
        if name_scr == "gameplay" and "hero" in kwargs:
            self.hero_selected = kwargs["hero"]
            self.screens["gameplay"] = Gameplay(self.screen, self.change_scr, self.hero_selected)

        self.current_screen = self.screens[name_scr]
