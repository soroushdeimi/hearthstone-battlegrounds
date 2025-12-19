import random
from .minion import Minion

class Tavern:
    def __init__(self , shop_size = 3):
        self.shop_size = shop_size
        self.minion_pool = self._create_minion_pool()

    def _create_minion_pool(self):
        return [
            Minion("Catacomb Crasher", 1, 1, 1),
            Minion("Murloc Tidecaller", 1, 2, 1),
            Minion("Dragon Spawn", 2, 3, 1),
            Minion("Old Murk-Eye", 2, 4, 2)
        ]
    def get_available_minions(self, tier):
        return [m for m in self.minion_pool if m.tier <= tier]
    def roll(self, player_tier):
        available = self.get_available_minions(player_tier)
        if not available:
            return []
        return random.choices(available, k = self.shop_size)
