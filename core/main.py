import pygame
import sys
from engine.minion import Minion
from engine.player import Player
from engine.taveren import Tavern

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
        self.tavern = Tavern(shop_size = 4)

        self.state = "MENU"
        self.player1 = None

    def start_new_game(self):
        self.player1 = Player("Sattar")
        self.player1.add_minion(Minion("Murloc", 2 , 1 , 1))
        self.player1.add_minion(Minion("Dragon", 3 , 4 , 1))
        self.state = "PLAYING"


        self.player1.tier = 1
        self.player1.board = []
        m1 = Minion("Murloc", 2 , 1 ,1)
        m2 = Minion("Dragon", 3 , 4 , 1)
        m3 = Minion("Dragon", 3 , 4 , 1)
        m4 = Minion("Dragon", 3 , 4 , 1)
        m5 = Minion("Dragon", 3 , 4 , 1)
        m6 = Minion("Dragon", 3 , 4 , 1)
        m7 = Minion("Dragon", 3 , 4 , 1)
        m8 = Minion("Dragon", 3 , 4 , 1)

        self.player1.add_minion(m1)
        self.player1.add_minion(m2)
        self.player1.add_minion(m3)
        self.player1.add_minion(m4)
        self.player1.add_minion(m5)
        self.player1.add_minion(m6)
        self.player1.add_minion(m7)
        self.player1.add_minion(m8)

        #self.game_state = "RECRUIT"
        #self.debug_status = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if self.state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_new_game()

        #this is for test if user click space button then the first minion get 2 damage (health - 2)
            elif self.state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i,minion in enumerate(self.player1.board):
                        minion_rect = pygame.Rect(50 + (i * 120), 250, 100 , 140)
                        if minion_rect.collidepoint(mouse_pos):
                            minion.take_damage(1)
                            print(f"card{minion.name}fucked")
                    player_ui_rect = pygame.Rect(20,20,200,30)
                    if player_ui_rect.collidepoint(mouse_pos):
                        self.player1.take_damage(2)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        new_minions = self.tavern.roll(self.player1.tier)
                        self.player1.board = new_minions
                        print(f"Rolled {len(new_minions)} new minions from Tavern!")

                        print(f"Player HP reduced to : {self.player1.hp}")
                if self.player1.hp <= 0 :
                    self.state = "GAMEOVER"

            elif self.state == "GAMEOVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = "MENU"

               # if event.key == pygame.K_SPACE:
                #    if len(self.player1.board) > 0 :
                 #       self.player1.board[0].take_damage(2)
                  #      print(f"Health of first minion: {self.player1.board[0].health}")


                    #self.debug_status = not self.debug_status
    def update(self):
        pass
    def draw(self):
        self.screen.fill((30,30,30))
        if self.state == "MENU":
            title_font = pygame.font.SysFont("Arial", 80, bold=True)
            title_surface = title_font.render("HEARTHSTONE BG", True , (255 , 215 , 0))
            self.screen.blit(title_surface, title_surface.get_rect(center=(600,300)))
            start_surface = self.font.render("Press Enter to Start Game", True , (255,255,255))
            self.screen.blit(start_surface, start_surface.get_rect(center=(600, 450)))
        elif self.state == "PLAYING":
            info_text = self.font.render(f"Gold : {self.player1.gold} | HP : {self.player1.hp}", True , (255, 255, 255))
            self.screen.blit(info_text, (20,20))
            for i, minion in enumerate(self.player1.board):
                x_pos = 50 + (i * 120)
                y_pos = 250

                color = (0, 255, 0) if minion.is_alive else (255, 0, 0)

                pygame.draw.rect(self.screen, color, (x_pos, y_pos, 100, 140))
                name_text = self.font.render(minion.name, True, (0, 0, 0))
                self.screen.blit(name_text, (x_pos + 5, y_pos + 5))
                stats_text = self.font.render(f"{minion.attack} / {minion.health}", True, (0, 0, 0))
                self.screen.blit(stats_text, (x_pos + 20, y_pos + 100))
                shop_lable = self.font.render("SHOP(Press space)", True, (255,215,0))
                self.screen.blit(shop_lable, (50,60))

            for i , minion in enumerate(self.player1.shop):
                x_pos = 50 + (i * 120)
                y_pos = 100

                pygame.draw.rect(self.screen,(50,50,150), (x_pos, y_pos , 100, 140))
                pygame.draw.rect(self.screen, (200,200,200),(x_pos, y_pos , 100 , 140), 2)
                name_text = self.font.render(minion.name[:10], True, (255, 255, 255))
                self.screen.blit(name_text, (x_pos + 5, y_pos + 5))
                stats_text = self.font.render(f"{minion.attack} / {minion.health}", True, (255, 255, 255))
                self.screen.blit(stats_text, (x_pos + 25, y_pos + 110))



            pygame.display.flip()
        elif self.state == "GAMEOVER":
            lost_font = pygame.font.SysFont("Arial", 100 , bold = True)
            lost_surface = lost_font.render("You Dead", True , (255,0,0))
            self.screen.blit(lost_surface, lost_surface.get_rect(center=(600, 350)))
            retry_surface = self.font.render("Press R to return to Menu", True, (200,200,200))
            self.screen.blit(retry_surface, retry_surface.get_rect(center=(600,500)))

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