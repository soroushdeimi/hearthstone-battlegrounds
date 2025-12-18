import pygame
class Minion:
    def __init__(self, name,  attack , health , tier):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.is_alive = True;
    def take_damage(self , dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
#
# minion2 = Minion("Ali", 5,2,1);
#
# minion2.take_damage(3)
# if not minion2.is_alive():
#     print("Dead")
# else:
#     print("alive")

