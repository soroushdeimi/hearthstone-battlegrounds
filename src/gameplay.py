import pygame
from src.models.hand import Hand
from src.models.board import Board
from src.services.economy import Economy
from src.services.shop import Shop, ShopSlot
from src.services.drag_manager import DragManager


class Gameplay:
    def __init__(self, screen, change_scr, hero):
        self.screen = screen
        self.change_scr = change_scr
        self.hero = hero

        self.economy = Economy()

        self.shop = Shop()
        self.drag_manager = DragManager()
        self.hand = Hand()
        self.board = Board()

        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 32)

        for i in range(3):
            self.shop.slots.append(ShopSlot(minion=f"Minion {i+1}"))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                # مدیریت Drag & Drop
                self.drag_manager.handle_event(event, self.hand, self.board)

                # خرید فروشگاه
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, slot in enumerate(self.shop.slots):
                        rect = pygame.Rect(100 + i*120, 100, 100, 100)
                        if rect.collidepoint(x, y):
                            self.buy_shop_slot(i)
                    # فروش Board
                    for i, slot in enumerate(self.board.slots):
                        board_rect = pygame.Rect(100 + i*120, 400, 100, 100)
                        if board_rect.collidepoint(x, y) and slot is not None:
                            self.sell_from_board(i)
                    # Upgrade Tavern
                    tavern_rect = pygame.Rect(400, 20, 120, 40)
                    if tavern_rect.collidepoint(x, y):
                        if self.economy.upgrade_tavern():
                            print(f"Tavern upgraded to Tier {self.economy.tavern.tier}")

    def start_turn(self):
        self.economy.start_turn()
        print(f"Turn {self.economy.turn}, Gold: {self.economy.gold}, Tavern Tier: {self.economy.tavern.tier}")

    def buy_shop_slot(self, index):
        slot = self.shop.slots[index]
        if slot.minion and self.economy.spend(3):
            if self.hand.add(slot.minion):
                print(f"Bought {slot.minion}! Gold left: {self.economy.gold}")
                slot.minion = None
            else:
                print("Hand full! Cannot buy more minions.")
        else:
            print("Cannot buy! Not enough gold or slot empty.")

    def sell_from_board(self, board_index):
        if self.board.is_occupied(board_index):
            minion = self.board.remove(board_index)
            self.economy.gain(1)
            print(f"Sold {minion}, gained 1 gold. Gold now: {self.economy.gold}")

    def play_from_hand(self, hand_index, board_index):
        if self.board.is_free(board_index):
            minion = self.hand.remove(hand_index)
            self.board.place(board_index, minion)
            print(f"Played {minion} to Board slot {board_index}")
        else:
            print("Board slot full! Cannot play this minion.")

    def updates(self):
        pass

    def render(self, surface):
        surface.fill((0, 100, 50))

        hero_text = self.font.render(f"Gameplay: {self.hero}", True, (255, 255, 255))
        surface.blit(hero_text, (surface.get_width()//2 - hero_text.get_width()//2, 50))

        gold_text = self.small_font.render(f"Gold: {self.economy.gold}", True, (255, 215, 0))
        surface.blit(gold_text, (20, 20))

        tavern_text = self.small_font.render(f"Tavern Tier: {self.economy.tavern.tier}", True, (255, 255, 0))
        surface.blit(tavern_text, (400, 20))

        # فروشگاه
        for i, slot in enumerate(self.shop.slots):
            x, y, w, h = 100 + i*120, 100, 100, 100
            color = (200, 200, 200) if slot.minion else (100, 100, 100)
            pygame.draw.rect(surface, color, (x, y, w, h))
            if slot.minion:
                minion_text = self.small_font.render(str(slot.minion), True, (0,0,0))
                surface.blit(minion_text, (x+5, y+5))

        # Hand
        hand_text = self.small_font.render(f"Hand: {', '.join(self.hand.cards)}", True, (255, 255, 255))
        surface.blit(hand_text, (20, 300))

        # Board
        board_text = self.small_font.render(f"Board: {', '.join([str(m) for m in self.board.slots])}", True, (255, 255, 255))
        surface.blit(board_text, (20, 400))

        # کارت‌های Drag & Drop روی Hand/Board
        self.drag_manager.render(surface, self.small_font)
