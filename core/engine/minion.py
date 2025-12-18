import pygame
import minion
class Minion:
    def __init__(self, name,  attack , health , tier):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier


    def is_alive(self):
        return self.health > 0

    def take_damage(self , dmg):
        self.health -= dmg

minion2 = Minions("Ali", 5,2,1);

minion2.take_damage(3)
if not minion2.is_alive():
    print("Dead")
else:
    print("alive")

