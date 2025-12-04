import pygame

class Text:
    def __init__(self , text , font = "freesansbold.ttf" , t_color = "white" , b_color = None , size = 15 , x = 0 , y = 0):
        self.text = text
        self.font = font
        self.text_color = t_color
        self.background_color = b_color
        self.size = size
        self.font_obj = pygame.font.Font(font , size)
        self.text_obj = self.font_obj.render(text , True , pygame.Color(t_color) , b_color)
        self.rect = self.text_obj.get_rect()
        
        self.world_pos = pygame.Vector2(0, 0)
        self.rect = self.text_obj.get_rect(topleft=self.world_pos)
        self.updatePosition(x , y)

    def updatePosition(self , x , y):
        self.world_pos.x = x
        self.world_pos.y = y
        self.rect.topleft = (x, y)

    def updateText(self , text):
        self.text = text
        self.text_obj = self.font_obj.render(text, True, pygame.Color(self.text_color), self.background_color)
        self.rect = self.text_obj.get_rect(topleft=self.world_pos)

    def updateFont(self , font = "freesansbold.ttf" , size = 15):
        self.font = font
        self.size = size
        self.font_obj = pygame.font.Font(font , size)
        self.updateText(self.text)
        
    def draw(self, screen, camera_offset=None):
        if camera_offset:
            screen.blit(self.text_obj, (self.world_pos.x - camera_offset.x, self.world_pos.y - camera_offset.y))
        else:
            screen.blit(self.text_obj, self.world_pos)


class Button(Text):
    def __init__(self, x, y,width, height, text, color, hover_color, t_color="white", font="freesansbold.ttf", size = 25, b_color=None):
        super().__init__(text, font, t_color, b_color, size, x, y)

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.clicked = False
        self.text_rect = self.text_obj.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=int((self.rect.width + self.rect.height)/20))
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=int((self.rect.width + self.rect.height)/20))  
    
        self.text_rect.center = self.rect.center
        
        surface.blit(self.text_obj, self.text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def handle_event(self, event):
   
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.clicked = True
                return True
        return False
    
    def is_clicked(self):

        if self.clicked:
            self.clicked = False
            return True
        return False
    
    def updatePosition(self, x, y): 
    
        self.rect.x = x
        self.rect.y = y
    
    def updateText(self, text):
      
        super().updateText(text)
        self.text_rect = self.text_obj.get_rect(center=self.rect.center)
    
    def updateFont(self, font="freesansbold.ttf", size=32):
        
        super().updateFont(font, size)
        self.text_rect = self.text_obj.get_rect(center=self.rect.center)
        self.button_color = (0, 0, 0)


class InputText:
    def __init__(self, rect, font, is_password = False):
        self.rect = pygame.Rect(rect)
        self.text = ''
        self.font = font
        self.active = False
        self.is_password = is_password
        self.color = (200, 200, 200)
        self.hoverd_color = (100, 100, 100)
        self.hoverd = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode
    
    def draw(self, screen):
        color = self.hoverd_color if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, 2 if self.active else 1, border_radius=int((self.rect.width + self.rect.height)/10))
        display_text = '*' * len(self.text) if self.is_password else self.text
        text_surface = self.font.render(display_text, True, (25, 250, 250))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 3))