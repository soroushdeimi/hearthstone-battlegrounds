import pygame

class Button:
    def __init__(self, x, y, width, height, text, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.color = (70, 130, 180)
        self.hover_color = (100, 160, 210)
        self.current_color = self.color
        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.current_color = self.hover_color if self.rect.collidepoint(event.pos) else self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (250, 250, 250), self.rect, 3 ,border_radius=10) # kadr

        text_surf = self.font.render(self.text, True, (250, 250, 250)) # text daron
        text_rect = text_surf.get_rect(center = self.rect.center)
        surface.blit(text_surf, text_rect)
