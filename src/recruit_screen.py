import pygame
import random
from button import Button

# <<<--- مینیون موقت - فقط برای اینکه الان کار کنه ---<<<
# بعداً این بخش رو حذف می‌کنی و از minions.py استفاده می‌کنی

import random

class TempMinion:  # اسم موقت دادم که با کلاس اصلی تداخل نداشته باشه
    def __init__(self, name, attack, health):
        self.name = name
        self.attack = attack
        self.health = health
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)

    def draw(self, surface, rect):
        pygame.draw.rect(surface, (90, 70, 130), rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 200), rect, 3, border_radius=10)

        # نام
        name_surf = self.small_font.render(self.name, True, (255, 255, 255))
        surface.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.top + 20)))

        # حمله و سلامتی
        atk_surf = self.font.render(str(self.attack), True, (255, 100, 100))
        surface.blit(atk_surf, atk_surf.get_rect(bottomleft=(rect.left + 15, rect.bottom - 10)))

        hp_surf = self.font.render(str(self.health), True, (100, 255, 100))
        surface.blit(hp_surf, hp_surf.get_rect(bottomright=(rect.right - 15, rect.bottom - 10)))

        # هزینه
        cost_surf = self.small_font.render("3", True, (255, 215, 0))
        surface.blit(cost_surf, cost_surf.get_rect(center=(rect.centerx, rect.bottom - 15)))

# لیست مینیون‌های موقت
TEMP_MINIONS = [
    ("Murloc Scout", 1, 2),
    ("Alleycat", 1, 1),
    ("Rockpool Hunter", 2, 3),
    ("Dragon Whelp", 2, 1),
    ("Wrath Weaver", 1, 3),
    ("Deck Swabbie", 2, 2),
    ("Scallywag", 2, 1),
]
# >>>----------------------------------------------<<<

class RecruitScreen:
    def __init__(self, screen, change_scr, hero_name):
        self.screen = screen
        self.change_scr = change_scr
        self.hero_name = hero_name

        self.gold = 3
        self.tavern_tier = 1
        self.health = 40

        self.shop = []
        self.hand = []
        self.board = []

        self.dragging = None
        self.drag_offset = (0, 0)

        self.info_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # دکمه‌ها
        self.end_turn_button = Button(
            x=screen.get_width() - 150, y=screen.get_height() - 80,
            width=120, height=50, text="End Turn", on_click=self.end_turn
        )
        self.refresh_button = Button(
            x=screen.get_width() - 280, y=screen.get_height() - 80,
            width=120, height=50, text="Refresh (1)", on_click=self.refresh_shop
        )

        # اسلات‌ها
        self.shop_slots = self.create_slots(5, 100, 100, 100, 140, 20)
        self.board_slots = self.create_slots(7, 100, 350, 80, 110, 15)
        self.hand_slots = self.create_slots(10, 100, 500, 70, 95, 10)

        self.refresh_shop(initial=True)

    def create_slots(self, count, start_x, start_y, w, h, gap):
        return [pygame.Rect(start_x + i * (w + gap), start_y, w, h) for i in range(count)]

    def refresh_shop(self, initial=False):
        if not initial and self.gold < 1:
            print("Not enough gold!")
            return
        if not initial:
            self.gold -= 1

        # استفاده از مینیون موقت
        self.shop = []
        for _ in range(5):
            name, atk, hp = random.choice(TEMP_MINIONS)
            self.shop.append(TempMinion(name, atk, hp))

    def end_turn(self):
        print("Turn ended!")

    def get_minion_at_pos(self, pos):
        for i, m in enumerate(self.hand):
            if self.hand_slots[i].collidepoint(pos):
                return "hand", i, m
        for i, m in enumerate(self.board):
            if self.board_slots[i].collidepoint(pos):
                return "board", i, m
        for i, m in enumerate(self.shop):
            if self.shop_slots[i].collidepoint(pos):
                return "shop", i, m
        return None, None, None

    def handle_events(self, events):
        for event in events:
            self.end_turn_button.handle_event(event)
            self.refresh_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                source, idx, minion = self.get_minion_at_pos(pos)

                if source == "shop" and minion and self.gold >= 3 and len(self.hand) < 10:
                    self.hand.append(minion)
                    del self.shop[idx]
                    # اضافه کردن یک مینیون جدید به شاپ تا دوباره 5 تا بشه
                    name, atk, hp = random.choice(TEMP_MINIONS)
                    self.shop.append(TempMinion(name, atk, hp))
                    self.gold -= 3

                elif minion:
                    rect = self.shop_slots[idx] if source == "shop" else \
                           self.hand_slots[idx] if source == "hand" else self.board_slots[idx]
                    self.dragging = (source, idx, minion)
                    self.drag_offset = (rect.left - pos[0], rect.top - pos[1])

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging:
                    pos = pygame.mouse.get_pos()
                    source, idx, minion = self.dragging
                    target, target_idx, _ = self.get_minion_at_pos(pos)

                    if target == "board" and len(self.board) < 7 and source == "hand":
                        self.board.append(minion)
                        del self.hand[idx]
                    elif target == "hand" and len(self.hand) < 10 and source == "board":
                        self.hand.append(minion)
                        del self.board[idx]

                    self.dragging = None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # راست کلیک = فروش
                pos = pygame.mouse.get_pos()
                source, idx, minion = self.get_minion_at_pos(pos)
                if source in ["hand", "board"] and minion:
                    if source == "hand":
                        del self.hand[idx]
                    elif source == "board":
                        del self.board[idx]
                    self.gold += 1
                    print(f"Minion sold! +1 Gold (Now: {self.gold})")

    def updates(self):
        pass

    def render(self, surface):
        surface.fill((20, 25, 35))

        # اطلاعات بالا
        surface.blit(self.info_font.render(f"Hero: {self.hero_name}", True, (255, 255, 255)), (30, 20))
        surface.blit(self.info_font.render(f"Gold: {self.gold}", True, (255, 215, 0)), (200, 20))
        surface.blit(self.info_font.render(f"Tier: {self.tavern_tier}", True, (180, 150, 255)), (350, 20))
        surface.blit(self.info_font.render(f"Health: {self.health}", True, (255, 100, 100)), (550, 20))

        # عنوان‌ها
        surface.blit(self.info_font.render("Tavern (Shop)", True, (180, 220, 255)), (30, 60))
        surface.blit(self.info_font.render("Your Board", True, (180, 220, 255)), (30, 310))
        surface.blit(self.info_font.render("Hand", True, (180, 220, 255)), (30, 460))

        # رسم مینیون‌ها
        for i, m in enumerate(self.shop):
            m.draw(surface, self.shop_slots[i])
        for i, m in enumerate(self.board):
            m.draw(surface, self.board_slots[i])
        for i, m in enumerate(self.hand):
            m.draw(surface, self.hand_slots[i])

        # درگ - بهبود یافته
        if self.dragging:
            _, _, m = self.dragging
            pos = pygame.mouse.get_pos()
            drag_rect = pygame.Rect(0, 0, 100, 140)
            drag_rect.center = pos
            drag_rect.move_ip(self.drag_offset)  # دقیقاً همون جایی که کلیک کردی
            m.draw(surface, drag_rect)

        # دکمه‌ها
        self.end_turn_button.draw(surface)
        self.refresh_button.draw(surface)