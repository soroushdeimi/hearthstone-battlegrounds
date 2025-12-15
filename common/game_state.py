class GameState:
    def __init__(self):
        self.board = []
        self.max_board = 7

        # Buff دائمی مخصوص کارت خاص (مثل Beetle)
        self.global_card_buffs = {
            "BEETLE_TOKEN": {"attack": 0, "health": 0},
        }

        # Buff دائمی مخصوص Tribe (مثل Undead)
        self.global_tribe_buffs = {
            "Undead": {"attack": 0, "health": 0},
            "Beast": {"attack": 0, "health": 0},
            "Demon": {"attack": 0, "health": 0},
        }

        self.death_queue = []

    #BOARD

    def add_to_board(self, minion, position=None):
        if len(self.board) >= self.max_board:
            print("Board is full, cannot summon:", minion.name)
            return False

        if position is None or position >= len(self.board):
            self.board.append(minion)
        else:
            self.board.insert(position, minion)

        print("Summoned on board:", minion)
        return True

    def apply_global_buffs(self, minion):
        # 1) کارت-محور
        if minion.card_id in self.global_card_buffs:
            buff = self.global_card_buffs[minion.card_id]
            minion.buff(buff["attack"], buff["health"])

        # 2) تریبی (Tribe-محور)
        if minion.tribe in self.global_tribe_buffs:
            tb = self.global_tribe_buffs[minion.tribe]
            minion.buff(tb["attack"], tb["health"])

    def summon_minion(self, card_id, position=None):
        from common.minion import (
            BeetleToken, SkeletonToken, HandToken,
            BuzzingVermin, ForestRover, NestSwarmer, TurquoiseSkitterer, MonstrousMacaw,
            HarmlessBonehead, HandlessForsaken, NerubianDeathswarmer
        )

        mapping = {
            "BEETLE_TOKEN": BeetleToken,
            "SKELETON_TOKEN": SkeletonToken,
            "HAND_TOKEN": HandToken,

            "BUZZING_VERMIN": BuzzingVermin,
            "FOREST_ROVER": ForestRover,
            "NEST_SWARMER": NestSwarmer,
            "TURQUOISE_SKITTERER": TurquoiseSkitterer,
            "MONSTROUS_MACAW": MonstrousMacaw,

            "HARMLESS_BONEHEAD": HarmlessBonehead,
            "HANDLESS_FORSAKEN": HandlessForsaken,
            "NERUBIAN_DEATHSWARMER": NerubianDeathswarmer,
        }

        if card_id not in mapping:
            print("Unknown card_id:", card_id)
            return False

        minion = mapping[card_id]()

        # Battlecry فقط هنگام Play (فعلاً چون hand نداریم، اینجا اجرا می‌کنیم)
        if "Battlecry" in minion.keywords:
            minion.on_play(self)

        # اعمال buffهای دائمی (کارت-محور و تریبی)
        self.apply_global_buffs(minion)

        return self.add_to_board(minion, position)

    #  DEATHRATTLE TRIGGER (بدون مرگ) 

    def trigger_deathrattle(self, minion):
        if minion is None:
            return False
        if minion not in self.board:
            return False
        if "Deathrattle" not in minion.keywords:
            return False

        minion.on_deathrattle(self)
        return True

    def trigger_leftmost_friendly_deathrattle(self, exclude_minion=None):
        for m in self.board:
            if exclude_minion is not None and m is exclude_minion:
                continue
            if "Deathrattle" in m.keywords and m.is_alive():
                return self.trigger_deathrattle(m)
        print("No valid left-most Deathrattle minion found.")
        return False

    #DEATH PROCESSING

    def queue_death(self, minion):
        if minion in self.board and minion.dead and minion not in self.death_queue:
            self.death_queue.append(minion)

    def collect_deaths_left_to_right(self):
        for m in self.board:
            if m.dead:
                self.queue_death(m)

    def process_deaths(self):
        self.collect_deaths_left_to_right()

        while self.death_queue:
            dying = self.death_queue.pop(0)

            if dying not in self.board:
                continue

            # مثل بازی: اول حذف، بعد Deathrattle
            self.board.remove(dying)

            if "Deathrattle" in dying.keywords:
                dying.on_deathrattle(self)

            self.collect_deaths_left_to_right()

    #TEST HELPERS

    def deal_damage_to_slot(self, slot_index, damage):
        if slot_index < 0 or slot_index >= len(self.board):
            return
        target = self.board[slot_index]
        target.take_damage(damage)
        self.process_deaths()

    def debug_print_board(self):
        print("=== BOARD STATE ===")
        for i, m in enumerate(self.board):
            print(f"{i}: {m}")
        print("===================")


