import pygame
import sys
from engine.minion import Minion
from engine.player import Player

class GameController:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hearthstone Battlegrounds Simulator")
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.player1 = Player("Mani")
        m1 = Minion("Murloc", 2 , 1 ,1)
        m2 = Minion("Dragon", 3 , 4 , 1)

        self.player1.add_minion(m1)
        self.player1.add_minion(m2)

        #self.game_state = "RECRUIT"
        #self.debug_status = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
        #this is for test if user click space button then the first minion get 2 damage (health - 2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i,minion in enumerate(self.player1.board):
                    minion_rect = pygame.Rect(50 + (i * 120), 250, 100 , 140)
                    if minion_rect.collidepoint(mouse_pos):
                        minion.take_damage(1)
                        print(f"card{minion.name}fucked")


               # if event.key == pygame.K_SPACE:
                #    if len(self.player1.board) > 0 :
                 #       self.player1.board[0].take_damage(2)
                  #      print(f"Health of first minion: {self.player1.board[0].health}")


                    #self.debug_status = not self.debug_status
    def update(self):
        pass
    def draw(self):
        self.screen.fill((30,30,30))
        info_text = self.font.render(f"Gold {self.player1.gold} | HP: {self.player1.hp}" , True , (255,255,255))
        self.screen.blit(info_text, (20,20))
        for i, minion in enumerate(self.player1.board):
            x_pos = 50 + (i * 120)
            y_pos = 250


            color = (0,255,0)if minion.is_alive else (255,0,0)

            pygame.draw.rect(self.screen , color , (x_pos , y_pos , 100 , 140))
            name_text = self.font.render(minion.name , True , (0 , 0 , 0))
            self.screen.blit(name_text, (x_pos + 5 , y_pos + 5))
            stats_text = self.font.render(f"{minion.attack} / {minion.health}", True, (0, 0, 0))
            self.screen.blit(stats_text, (x_pos + 20, y_pos + 100))

            info_text = self.font.render(f"HP: {self.player1.hp} | Gold: {self.player1.gold}", True, (255, 255, 255))
        self.screen.blit(info_text, (20, 20))

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

game = GameController()
game.run()