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

    # hooks
    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
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


class SkeletonToken(Minion):
    def __init__(self):
        super().__init__(
            card_id="SKELETON_TOKEN",
            name="Skeleton",
            tier=1,
            attack=1,
            health=1,
            tribe="Undead",
            keywords=None
        )


class HandToken(Minion):
    def __init__(self):
        super().__init__(
            card_id="HAND_TOKEN",
            name="Hand",
            tier=1,
            attack=2,
            health=1,
            tribe="Undead",
            keywords={"Reborn"}
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
        print("Buzzing Vermin deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class ForestRover(Minion):
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
        print("Forest Rover deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class NestSwarmer(Minion):
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
        print("Nest Swarmer deathrattle triggers, summoning three Beetles...")
        for _ in range(3):
            game_state.summon_minion("BEETLE_TOKEN")


class TurquoiseSkitterer(Minion):
    def __init__(self):
        super().__init__(
            card_id="TURQUOISE_SKITTERER",
            name="Turquoise Skitterer",
            tier=3,
            attack=3,
            health=4,
            tribe="Beast",
            keywords={"Deathrattle"}
        )

    def on_deathrattle(self, game_state):
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 2
        print("Turquoise Skitterer deathrattle triggers: Beetles +1/+2, then summon a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class MonstrousMacaw(Minion):
    def __init__(self):
        super().__init__(
            card_id="MONSTROUS_MACAW",
            name="Monstrous Macaw",
            tier=3,
            attack=3,
            health=2,
            tribe="Beast",
            keywords=None
        )

    def after_attack(self, game_state):
        print("Monstrous Macaw after_attack: triggering left-most friendly Deathrattle...")
        game_state.trigger_leftmost_friendly_deathrattle(exclude_minion=self)


#UNDEAD

class HarmlessBonehead(Minion):
    def __init__(self):
        super().__init__(
            card_id="HARMLESS_BONEHEAD",
            name="Harmless Bonehead",
            tier=1,
            attack=2,
            health=2,
            tribe="Undead",
            keywords={"Deathrattle"}
        )

    def on_deathrattle(self, game_state):
        print("Harmless Bonehead died, summoning two Skeletons...")
        for _ in range(2):
            game_state.summon_minion("SKELETON_TOKEN")


class HandlessForsaken(Minion):
    def __init__(self):
        super().__init__(
            card_id="HANDLESS_FORSAKEN",
            name="Handless Forsaken",
            tier=2,
            attack=3,
            health=2,
            tribe="Undead",
            keywords={"Deathrattle"}
        )

    def on_deathrattle(self, game_state):
        print("Handless Forsaken died, summoning a Hand (2/1) with Reborn...")
        game_state.summon_minion("HAND_TOKEN")


class NerubianDeathswarmer(Minion):
    """
    Battlecry: All your Undead in this game get +1 Attack.
    """
    def __init__(self):
        super().__init__(
            card_id="NERUBIAN_DEATHSWARMER",
            name="Nerubian Deathswarmer",
            tier=2,
            attack=2,
            health=3,
            tribe="Undead",
            keywords={"Battlecry"}
        )

    def on_play(self, game_state):
        # 1) ثبت buff دائمی برای Undeadهای آینده
        game_state.global_tribe_buffs["Undead"]["attack"] += 1

        # 2) اعمال فوری روی Undeadهای فعلی روی برد
        for m in game_state.board:
            if m.tribe == "Undead" and m.is_alive():
                m.buff(attack=1, health=0)

        print("Nerubian Deathswarmer battlecry: all Undead get +1 Attack (permanent).")

