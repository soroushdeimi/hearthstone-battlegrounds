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
        return max (data["base"]-self.discount,data["min"])
    

    def end_turn(self):
        data = TAVERN_TABLE[self.tier]
        if data["base"] - self.discount > data["min"]:
            self.discount += 1

    def upgrade(self):
        self.tier += 1
        self.discount = 0