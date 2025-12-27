import pygame
from button import Button

class Title:
    def __init__(self, screen, change_scr):
        self.screen = screen
        self.change_scr = change_scr

        self.start_button = Button(
            x = screen.get_width()//2 - 100,
            y = 300,
            width = 200,
            height = 60,
            text = "Start Game",
            on_click = lambda: self.change_scr("hero_select")
        )
        self.quit_button = Button( 
            x = screen.get_width()//2 - 100,
            y = 380,
            width = 200,
            height = 60,
            text = "Exist",
            on_click = lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        )

        self.title_font = pygame.font.Font(None, 72)
        self.title_text = self.title_font.render("Hearthstone Battlegrounds", True, (250, 250, 55))

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)
            self.quit_button.handle_event(event)
    def updates(self):
        pass
    def render(self, surface):
        surface.fill((75, 0, 130))
        title_rect = self.title_text.get_rect(center = (surface.get_width()// 2, 150))
        surface.blit(self.title_text, title_rect)
        self.start_button.draw(surface)
        self.quit_button.draw(surface)