import pygame

class DragManager:
    def __init__(self):
        self.dragging = False
        self.card = None
        self.start_pos = (0,0)
        self.current_pos = (0,0)

    def handle_event(self, event, hand, board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, card in enumerate(hand.cards):
                card_rect = pygame.Rect(100 + i*120, 300, 100, 100)
                if card_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.card = card
                    self.start_pos = event.pos
                    hand.remove(i)
                    break

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.current_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            for i, slot in enumerate(board.slots):
                slot_rect = pygame.Rect(100 + i*120, 400, 100, 100)
                if slot_rect.collidepoint(event.pos) and board.is_free(i):
                    board.place(i, self.card)
                    self.dragging = False
                    self.card = None
                    return
            hand.add(self.card)
            self.dragging = False
            self.card = None

    def render(self, surface, font):
        if self.dragging and self.card:
            rect = pygame.Rect(self.current_pos[0]-50, self.current_pos[1]-50, 100, 100)
            pygame.draw.rect(surface, (255,255,255), rect)
            text = font.render(str(self.card), True, (0,0,0))
            surface.blit(text, (rect.x+5, rect.y+5))
