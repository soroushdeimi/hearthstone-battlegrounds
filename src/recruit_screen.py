# screens/recruit_screen.py

import pygame
import random
from button import Button
from minion import Minion
from minion_db import MINIONS_DB

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

        # Buttons
        self.end_turn_button = Button(
            x=screen.get_width() - 150, y=screen.get_height() - 80,
            width=120, height=50, text="End Turn", on_click=self.end_turn
        )
        self.refresh_button = Button(
            x=screen.get_width() - 280, y=screen.get_height() - 80,
            width=120, height=50, text="Refresh (1)", on_click=self.refresh_shop
        )

        # Slots
        self.shop_slots = self.create_slots(5, 100, 100, 100, 140, 20)
        self.board_slots = self.create_slots(7, 100, 350, 80, 110, 15)
        self.hand_slots = self.create_slots(10, 100, 500, 70, 95, 10)

        self.refresh_shop(initial=True)

    def create_slots(self, count, start_x, start_y, w, h, gap):
        return [pygame.Rect(start_x + i * (w + gap), start_y, w, h) for i in range(count)]

    def refresh_shop(self, initial=False):
        if not initial and self.gold < 1:
            print("Not enough gold to refresh!")
            return
        if not initial:
            self.gold -= 1

        available = [data for data in MINIONS_DB.values() if data["tier"] <= self.tavern_tier]
        self.available_minions = available

        self.shop = [Minion(random.choice(available)) for _ in range(5)]
        print(f"Shop refreshed. Gold left: {self.gold}")

    def end_turn(self):
        print("Turn ended! Starting combat phase...")

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

                # Buy from shop
                if source == "shop" and minion:
                    if self.gold >= minion.cost and len(self.hand) < 10:
                        self.hand.append(minion)
                        del self.shop[idx]
                        if self.available_minions:
                            self.shop.append(Minion(random.choice(self.available_minions)))
                        self.gold -= minion.cost
                        print(f"Purchased: {minion.name} ({minion.cost} gold). Gold left: {self.gold}")
                    else:
                        if self.gold < minion.cost:
                            print("Not enough gold!")
                        if len(self.hand) >= 10:
                            print("Hand is full!")

                # Start drag
                elif source in ["hand", "board"] and minion:
                    rect = self.hand_slots[idx] if source == "hand" else self.board_slots[idx]
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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click = Sell
                pos = pygame.mouse.get_pos()
                source, idx, minion = self.get_minion_at_pos(pos)
                if source in ["hand", "board"] and minion:
                    if source == "hand":
                        del self.hand[idx]
                    elif source == "board":
                        del self.board[idx]
                    self.gold += 1
                    print(f"Sold: {minion.name} (+1 gold). Gold now: {self.gold}")

    def updates(self):
        pass

    def render(self, surface):
        surface.fill((20, 25, 35))

        # Header info
        surface.blit(self.info_font.render(f"Hero: {self.hero_name}", True, (255, 255, 255)), (30, 20))
        surface.blit(self.info_font.render(f"Gold: {self.gold}", True, (255, 215, 0)), (200, 20))
        surface.blit(self.info_font.render(f"Tier: {self.tavern_tier}", True, (180, 150, 255)), (350, 20))
        surface.blit(self.info_font.render(f"Health: {self.health}", True, (255, 100, 100)), (550, 20))

        # Titles
        surface.blit(self.info_font.render("Tavern (Shop)", True, (180, 220, 255)), (30, 60))
        surface.blit(self.info_font.render("Your Board", True, (180, 220, 255)), (30, 310))
        surface.blit(self.info_font.render("Hand", True, (180, 220, 255)), (30, 460))

        # Draw minions
        for i, m in enumerate(self.shop):
            m.draw(surface, self.shop_slots[i])
        for i, m in enumerate(self.board):
            m.draw(surface, self.board_slots[i])
        for i, m in enumerate(self.hand):
            m.draw(surface, self.hand_slots[i])

        # Dragging
        if self.dragging:
            _, _, m = self.dragging
            pos = pygame.mouse.get_pos()
            drag_rect = pygame.Rect(0, 0, 100, 140)
            drag_rect.center = pos
            drag_rect.move_ip(self.drag_offset)
            m.draw(surface, drag_rect)

        # Buttons
        self.end_turn_button.draw(surface)
        self.refresh_button.draw(surface)