import pygame

class Gameplay:
    def __init__(self, screen, change_scr, hero):
        self.screen = screen
        self.change_scr = change_scr
        self.hero = hero  
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render(f"Gameplay: {self.hero}", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def updates(self):
        pass

    def render(self, surface):
        surface.fill((0, 100, 50))
        rect = self.text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
        surface.blit(self.text, rect)
