# services/economy.py

TAVERN_TABLE = {
    1: {"base": 5, "min": 2, "slots": 3, "odds": [1.0, 0.0, 0.0]},
    2: {"base": 7, "min": 4, "slots": 4, "odds": [0.7, 0.3, 0.0]},
    3: {"base": 8, "min": 5, "slots": 4, "odds": [0.55, 0.33, 0.12]},
    4: {"base": 9, "min": 6, "slots": 5, "odds": [0.45, 0.35, 0.20]},
}

class Tavern:
    def __init__(self):
        self.tier = 1
        self.discount = 0

    def upgrade_cost(self):
        data = TAVERN_TABLE[self.tier]
        return max(data["base"] - self.discount, data["min"])

    def end_turn(self):
        data = TAVERN_TABLE[self.tier]
        if data["base"] - self.discount > data["min"]:
            self.discount += 1

    def upgrade(self):
        if self.tier < 4:
            self.tier += 1
            self.discount = 0

class Economy:
    MAX_GOLD = 10

    def __init__(self):
        self.turn = 1
        self.gold = 3
        self.full_gold_warning = False
        self.tavern = Tavern()

    def start_turn(self):
        self.turn += 1
        if self.gold < self.MAX_GOLD:
            self.gold = min(self.gold + 1, self.MAX_GOLD)
        self.full_gold_warning = (self.gold == self.MAX_GOLD)
        self.tavern.end_turn()

    def can_spend(self, amount):
        return self.gold >= amount

    def spend(self, amount):
        if self.can_spend(amount):
            self.gold -= amount
            return True
        return False

    def gain(self, amount):
        self.gold = min(self.gold + amount, self.MAX_GOLD)

    def upgrade_tavern(self):
        cost = self.tavern.upgrade_cost()
        if self.spend(cost):
            self.tavern.upgrade()
            return True
        return False
