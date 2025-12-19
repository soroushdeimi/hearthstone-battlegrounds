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

        # برای Hero Power Lich King:
        # فقط برای "کامبت بعدی" به یک مینیون داده می‌شود (UI-ready)
        self.reborn_next_combat = False

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

    # hooks (برای آینده: combat loop / end turn / ...)
    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass

    def after_attack(self, game_state):
        pass

    # رویداد عمومی: “یک مینیون خودی play شد”
    # (برای کارت‌هایی مثل Wrath Weaver که به play شدن بقیه واکنش می‌دهند)
    def on_friendly_minion_played(self, game_state, played_minion):
        pass

    def __repr__(self):
        return f"<Minion {self.name} {self.attack}/{self.health} keywords={self.keywords}>"


# TOKENS

class BeetleToken(Minion):
    def __init__(self):
        super().__init__("BEETLE_TOKEN", "Beetle", 1, 1, 1, tribe="Beast")


class SkeletonToken(Minion):
    def __init__(self):
        super().__init__("SKELETON_TOKEN", "Skeleton", 1, 1, 1, tribe="Undead")


class HandToken(Minion):
    def __init__(self):
        super().__init__("HAND_TOKEN", "Hand", 1, 2, 1, tribe="Undead", keywords={"Reborn"})


# BEETLE BUILD

class BuzzingVermin(Minion):
    def __init__(self):
        super().__init__("BUZZING_VERMIN", "Buzzing Vermin", 1, 2, 3, tribe="Beast", keywords={"Taunt", "Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Buzzing Vermin deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class ForestRover(Minion):
    def __init__(self):
        super().__init__("FOREST_ROVER", "Forest Rover", 2, 3, 3, tribe="Beast", keywords={"Battlecry", "Deathrattle"})

    def on_play(self, game_state):
        # فقط Beetle ها در کل بازی +1/+1 می‌گیرند
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 1

    def on_deathrattle(self, game_state):
        print("Forest Rover deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class NestSwarmer(Minion):
    def __init__(self):
        super().__init__("NEST_SWARMER", "Nest Swarmer", 2, 2, 2, tribe="Beast", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Nest Swarmer deathrattle triggers, summoning three Beetles...")
        for _ in range(3):
            game_state.summon_minion("BEETLE_TOKEN")


class TurquoiseSkitterer(Minion):
    def __init__(self):
        super().__init__("TURQUOISE_SKITTERER", "Turquoise Skitterer", 3, 3, 4, tribe="Beast", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 2
        print("Turquoise Skitterer deathrattle triggers: Beetles +1/+2, then summon a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class MonstrousMacaw(Minion):
    def __init__(self):
        super().__init__("MONSTROUS_MACAW", "Monstrous Macaw", 3, 3, 2, tribe="Beast")

    def after_attack(self, game_state):
        print("Monstrous Macaw after_attack: triggering left-most friendly Deathrattle...")
        game_state.trigger_leftmost_friendly_deathrattle(exclude_minion=self)


# UNDEAD

class HarmlessBonehead(Minion):
    def __init__(self):
        super().__init__("HARMLESS_BONEHEAD", "Harmless Bonehead", 1, 2, 2, tribe="Undead", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Harmless Bonehead died, summoning two Skeletons...")
        for _ in range(2):
            game_state.summon_minion("SKELETON_TOKEN")


class HandlessForsaken(Minion):
    def __init__(self):
        super().__init__("HANDLESS_FORSAKEN", "Handless Forsaken", 2, 3, 2, tribe="Undead", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Handless Forsaken died, summoning a Hand (2/1) with Reborn...")
        game_state.summon_minion("HAND_TOKEN")


class NerubianDeathswarmer(Minion):
    def __init__(self):
        super().__init__("NERUBIAN_DEATHSWARMER", "Nerubian Deathswarmer", 2, 2, 3, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        # buff دائمی برای Undead های آینده
        game_state.global_tribe_buffs["Undead"]["attack"] += 1

        # اعمال فوری روی Undead های فعلی
        for m in game_state.board:
            if m.tribe == "Undead" and m.is_alive():
                m.buff(attack=1, health=0)

        print("Nerubian Deathswarmer battlecry: all Undead get +1 Attack (permanent).")


# DEMON

class WrathWeaver(Minion):
    """
    After you play a Demon, gain +2/+2 and deal 1 damage to your hero.
    """
    def __init__(self):
        super().__init__("WRATH_WEAVER", "Wrath Weaver", 1, 1, 3, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
        # اگر یک Demon play شد (حتی خودِ Weaver)، تریگر می‌خورد
        if played_minion.tribe == "Demon":
            self.buff(attack=2, health=2)
            game_state.deal_hero_damage(1)
            print("Wrath Weaver triggers: +2/+2 and hero takes 1 damage.")
