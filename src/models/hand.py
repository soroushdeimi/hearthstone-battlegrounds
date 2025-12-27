class Hand:
    def __init__(self):
        self.cards = [] 

    def add(self, card):
        if len(self.cards) < 10: 
            self.cards.append(card)
            return True
        return False

    def remove(self, index):
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        return None
