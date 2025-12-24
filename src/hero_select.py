import pygame
from src.button import Button

class HeroSelect:
    def __init__(self, screen, change_scr):
        self.screen = screen
        self.change_scr = change_scr

        self.heroes = ["Mage", "Warrior", "Hunter", "Rogue"]
        self.selected_hero = None

        self.hero_buttons = []
        button_width, button_height = 150, 50
        start_y = 200
        gap = 70
        for i, hero in enumerate(self.heroes):
            btn = Button(
                x = screen.get_width()//2 - button_width//2,
                y = start_y + i * gap,
                width = button_width,
                height = button_height,
                text = hero,
                on_click = lambda h=hero: self.select_hero(h)
            )
            self.hero_buttons.append(btn)

        self.confirm_button = Button(
            x = screen.get_width()//2 - 100,
            y = start_y + len(self.heroes) * gap + 20,
            width = 200,
            height = 60,
            text = "Confirm",
            on_click = self.confirm_selection
        )

        self.title_font = pygame.font.Font(None, 60)
        self.title_text = self.title_font.render("Select Your Hero", True, (255, 255, 0))

    def select_hero(self, hero):
        self.selected_hero = hero
        print(f"Selected Hero: {hero}") 

    def confirm_selection(self):
        if self.selected_hero:
            self.change_scr("gameplay", hero=self.selected_hero)
        else:
            print("No hero selected!")


    def handle_events(self, events):
        for event in events:
            for btn in self.hero_buttons:
                btn.handle_event(event)
            self.confirm_button.handle_event(event)

    def updates(self):
        pass

    def render(self, surface):
        surface.fill((50, 0, 80))
        title_rect = self.title_text.get_rect(center=(surface.get_width()//2, 100))
        surface.blit(self.title_text, title_rect)

        for btn in self.hero_buttons:
            if btn.text == self.selected_hero:
                btn.current_color = (255, 215, 0) 
            else:
                btn.current_color = btn.color
            btn.draw(surface)

        self.confirm_button.draw(surface)
