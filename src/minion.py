
from typing import Dict, Any, Optional #to make the code more readable in line 5
from enum import Enum

class Ability(Enum):
    TAUNT = "taunt"
    DIVINE_SHIELD = "divine_shield"
    REBORN = "reborn"
    WINDFURY = "windfury"
    DEATHRATTLE = "deathrattle"
    BATTLECRY = "battlecry"
    START_OF_COMBAT = "start_of_combat"
    END_OF_TURN = "end_of_turn"
    AURA = "aura"

class Minion:
    def __init__(self, minion_data : Dict[str, Any]): #can be any type of data
        self.id : str = minion_data["id"]
        self.name : str = minion_data["name"]
        self.tier : int = int(minion_data["tier"]) #sath ghodrat minion 
        self.base_attack : int = int(minion_data["base_attack"])
        self.base_health : int = int(minion_data["base_health"])
        self.cost : int = int(minion_data.get("cost", 3)) #age kelid vazhe cost nabod meghdar ro 3 dar nazar migire
        self.tribe: str = minion_data["tribe"]
        self.abilities = minion_data.get("abilities", []) #bad az sakhtan minion dorost mishavan
        # yek khat ke be ui bazi ekhtesas darad
        self.is_token : bool = bool(minion_data.get("is_token", False)) # serfan jahat etminan age to data base ja oftade bod badbakht nashim
        self.c_attack : int = self.base_attack
        self.c_health : int = self.base_health
        self.is_golden : bool = bool(minion_data.get("is_golden", False))
        self.o_id : Optional[str] = None
        self.on_board : bool = False
        self.board_position : Optional[int] = None
        self.zone : str = "shop" # alan minion kojast
        self.alive : bool = True
        self.has_attacked : bool = False
        self.divine_shield = "divine_shield" in self.abilities #separ hanoz saleme?
        self.reborn_used : bool = False #vazeiat masraf reborn
        self.reborn_active = "reborn" in self.abilities #aya ejaze reborn darad


        self.battlecry_effect = minion_data.get("battlecry_effect") #vaghti  bazish mikoni in kar anjam mishe hand->board
        self.deathrattle_effect = minion_data.get("deathrattle_effect") #vaghti minion mimirad


    def to_dict(self) -> Dict[str, Any]:
        return{
            "id": self.id,
            "name": self.name,
            "tier": self.tier,
            "base_attack": self.base_attack,
            "base_health": self.base_health,
            "cost": self.cost,
            "tribe": self.tribe,
            "abilities": list(self.abilities),
            "is_token": self.is_token,
            "is_golden": self.is_golden,
            "battlecry_effect": self.battlecry_effect,
            "deathrattle_effect": self.deathrattle_effect,
        }

    def are_you_still_alive(self) -> bool:
        if self.alive and self.c_health > 0 : return True
        else : return False
    def has_ability(self, a : Ability): #vorodi tabe yek ability hast
        if a.value not in self.abilities: return False
        else : return True
    def add_ability(self, a : Ability):
        if a.value not in self.abilities:
            self.abilities.append(a.value)
        if a == Ability.DIVINE_SHIELD:
            self.divine_shield = True
        if a == Ability.REBORN:
            self.reborn_active = True
    def remove_ability(self, a : Ability):
        self.abilities = [ab for ab in self.abilities if ab != a.value]
        if a == Ability.DIVINE_SHIELD:
            self.divine_shield = False
        if a == Ability.REBORN:
            self.reborn_active = False
    def buff(self, health : int = 0, atack : int = 0): #ghodratmand kardan dadasham minion
        self.c_health += health
        self.c_attack += atack
    def damage_khor(self, d : int) -> str:
        damage = int(d)
        if damage <= 0 : return "NO Damage!!!"
        if self.divine_shield :
            self.divine_shield = False
            return "Divine_shield broken"
        self.c_health -= damage
        if self.c_health <= damage:
            self.alive = False
            return "Killed!"
        return "Damaged!"
    def mark_dead(self) -> None:
        self.c_health = 0
        self.alive = False
        self.zone = "grave"
        self.on_board = False
        self.board_position = None
    def can_reborn(self) -> bool:
        if self.reborn_active and (self.reborn_used is False) : return True
        else : return False
    def reborn(self) -> "Minion":
        self.reborn_used = True
        last_data = self.to_dict()
        reborn_minion = Minion({
            "id": self.id,
            "name": self.name,
            "tier": self.tier,
            "base_attack": self.base_attack,
            "base_health": self.base_health,
            "cost": self.cost,
            "tribe": self.tribe,
            "abilities": list(self.abilities),
            "is_token": self.is_token,
            "is_golden": self.is_golden,
            "battlecry_effect": self.battlecry_effect,
            "deathrattle_effect": self.deathrattle_effect,
        })
        reborn_minion.c_attack = self.c_attack
        reborn_minion.c_health = 1
        reborn_minion.o_id = self.o_id
        reborn_minion.zone = "board"
        reborn_minion.on_board = True
        reborn_minion.alive = True
        reborn_minion.reborn_active = False
        reborn_minion.reborn_used = True
        reborn_minion.divine_shield = False
        return reborn_minion
    def __repr__(self):
        return f"<Minion {self.name} {self.c_attack}/{self.c_health} abilities={self.abilities}>" #for debugging
    
    
            







