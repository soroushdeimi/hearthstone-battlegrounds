import pygame
import sys

pygame.init()

V_WIDTH, V_HEIGHT = 900, 600
window = pygame.display.set_mode((V_WIDTH, V_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Responsive Hearthstone Menu")

screen = pygame.Surface((V_WIDTH, V_HEIGHT))
clock = pygame.time.Clock()

GOLD = (212, 175, 55)
DARK_GOLD = (160, 120, 30)
BLACK = (0, 0, 0)

title_font = pygame.font.SysFont("arial", 72, bold=True)
button_font = pygame.font.SysFont("arial", 36)

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        scale_x = V_WIDTH / window.get_width()
        scale_y = V_HEIGHT / window.get_height()
        mouse = (mouse[0] * scale_x, mouse[1] * scale_y)

        color = GOLD if self.rect.collidepoint(mouse) else DARK_GOLD
        pygame.draw.rect(surface, color, self.rect, border_radius=100)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=100)

        text_surf = button_font.render(self.text, True, BLACK)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            scale_x = V_WIDTH / window.get_width()
            scale_y = V_HEIGHT / window.get_height()
            pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
            return self.rect.collidepoint(pos)
        return False

play = Button("PLAY", 330, 260, 240, 60)
options = Button("OPTIONS", 330, 340, 240, 60)
exit_btn = Button("EXIT", 330, 420, 240, 60)

running = True
while running:
    screen.fill((40, 60, 90))

    title = title_font.render("HEARTHSTONE", True, GOLD)
    screen.blit(title, title.get_rect(center=(450, 150)))

    play.draw(screen)
    options.draw(screen)
    exit_btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if play.is_clicked(event):
            print("LOGIN")
        if options.is_clicked(event):
            print("OPTIONS")
        if exit_btn.is_clicked(event):
            running = False

    scaled = pygame.transform.smoothscale(screen, window.get_size())
    window.blit(scaled, (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
