import pygame

# Abstract class of all objects in the game
class Object:
    # initializer
    def __init__(self , w = 64 , h = 64 , c = pygame.Color("white") , x = 0 , y = 0):

        # size attributes
        self.width = w
        self.height = h

        # hit box
        self.rect = pygame.Rect(x,y,w,h)

        # color
        self.color = c

        # possition attributes
        self.x_axis = x
        self.y_axis = y

    # draw function for rendering the initialized object
    def draw(self , surface):
        pygame.draw.rect(surface,self.color,self.rect)

# Abstract class of all characters in the game
class Character(Object):
    # initializer
    def __init__(self , w , h , c , x , y):
        super().__init__(w,h,c,x,y)

    # movement method // Note: not needed for npc class yet!
    def move(self):
        pass

# Class of playable characters derived from "Character" class
class PlayableCharacter(Character):
    # initializer
    def __init__(self):
        super().__init__(50,60,pygame.Color("blue"),20,490)

    # jump method
    def jump(self):
        pass

    # shoot method
    def shoot(self):
        pass

# Class of non playable characters derived from the "Character" class
class NonPlatableCharecter(Character):
    # initializer
    def __init__(self):
        super().__init__(50,60,pygame.Color("red"),730,490)

class Surface(Object):
    # initializer
    def __init__(self):
        super().__init__(800,50,pygame.Color("green"),0,550)

class Platform(Object):
    # initializer
    def __init__(self , x , y , w , h , color):
        super().__init__(w,h,color,x,y)
 
    # move method
    def move(self):
        pass