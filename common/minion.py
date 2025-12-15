
class Minion:
    def __init__(self, card_id, name, tier, attack, health, tribe=None, keywords=None):
        self.card_id = card_id
        self.name = name
        self.tier = tier
        self.attack = attack
        self.health = health
        self.tribe = tribe

        self.keywords = set(keywords) if keywords else set()
        self.is_golden = False
        self.dead = False

    def is_alive(self):
        return self.health > 0 and not self.dead

    def take_damage(self, damage):
        if self.dead:
            return True
        self.health -= damage
        if self.health <= 0:
            self.dead = True
        return self.dead

    def buff(self, attack=0, health=0):
        self.attack += attack
        self.health += health

    def add_keyword(self, keyword):
        self.keywords.add(keyword)

    def remove_keyword(self, keyword):
        self.keywords.discard(keyword)

    # hooks
    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass

    def on_start_of_combat(self, game_state):
        pass

    def on_end_of_turn(self, game_state):
        pass

    def after_attack(self, game_state):
        pass

    def __repr__(self):
        return f"<Minion {self.name} {self.attack}/{self.health} keywords={self.keywords}>"


#TOKENS

class BeetleToken(Minion):
    def __init__(self):
        super().__init__(
            card_id="BEETLE_TOKEN",
            name="Beetle",
            tier=1,
            attack=1,
            health=1,
            tribe="Beast",
            keywords=None
        )


#BEETLE BUILD

class BuzzingVermin(Minion):
    def __init__(self):
        super().__init__(
            card_id="BUZZING_VERMIN",
            name="Buzzing Vermin",
            tier=1,
            attack=2,
            health=3,
            tribe="Beast",
            keywords={"Taunt", "Deathrattle"}
        )

    def on_deathrattle(self, game_state):
        print("Buzzing Vermin died, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class ForestRover(Minion):
    """
    Battlecry: All Beetles in this game get +1/+1
    Deathrattle: Summon a 1/1 Beetle
    """
    def __init__(self):
        super().__init__(
            card_id="FOREST_ROVER",
            name="Forest Rover",
            tier=2,
            attack=3,
            health=3,
            tribe="Beast",
            keywords={"Battlecry", "Deathrattle"}
        )

    def on_play(self, game_state):
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 1

    def on_deathrattle(self, game_state):
        print("Forest Rover died, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class NestSwarmer(Minion):
    """
    Deathrattle: Summon three 1/1 Beetles.
    """
    def __init__(self):
        super().__init__(
            card_id="NEST_SWARMER",
            name="Nest Swarmer",
            tier=2,
            attack=2,
            health=2,
            tribe="Beast",
            keywords={"Deathrattle"}
        )

    def on_deathrattle(self, game_state):
        print("Nest Swarmer died, summoning three Beetles...")
        for _ in range(3):
            game_state.summon_minion("BEETLE_TOKEN")







