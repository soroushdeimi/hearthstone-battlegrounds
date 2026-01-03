class ShopSlot:
    def __init__(self, minion=None):
        self.minion = minion
        self.frozen = False

class Shop:
    def __init__(self):
        self.slots = []

    def refresh(self, minion_pool):
        for slot in self.slots:
            if not slot.frozen:
                slot.minion = minion_pool.random()

    def freeze(self, index):
        self.slots[index].frozen = True

    def unfreeze_all(self):
        for slot in self.slots:
            slot.frozen = False
