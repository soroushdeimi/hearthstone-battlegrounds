class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 30
        self.gold = 0
        self.board  = []
        self.tavern_tier = 1
        self.shop = []

    def add_minion(self , minion):
        if len(self.board) < 7:
            self.board.append(minion)
        else:
            print("Board Full!!!!")
    def remove_minion(self , n):
        if 0 <= n < len(self.board):
           return self.board.pop(n)
        return None
    def take_damage(self , amount):
            self.hp -= amount
    def rest_gold(self):
        self.gold = 0
    def roll_shop(self, tavern):
        pass
    def buy(self ,shop_index):
        pass
    def upgrade_tier(self):
        self.tavern_tier += 1
    def is_alive(self):
        return self.hp > 0



