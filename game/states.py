import pygame

class state:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.set_background("address")
    def set_background(self, image_path):
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def handle_events(self, screen):
        raise NotImplementedError   
    def draw(self, screen):
        raise NotImplementedError    
    def update(self):
        raise NotImplementedError
    def on_resize(self, new_width, new_height):
        self.screen_width = new_width
        self.screen_height = new_height
        if self.background == None:
            self.set_background("address")
        self.background = pygame.transform.scale(self.background, (new_width, new_height))
         