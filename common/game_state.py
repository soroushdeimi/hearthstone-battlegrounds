class GameState:
    def __init__(self):
        self.board = []
        self.max_board = 7

        # HP ساده‌ی بازیکن برای تست‌های بدون UI (مثلاً Wrath Weaver)
        self.player_hp = 30

        # Buff دائمی مخصوص کارت خاص (مثل Beetle-only)
        self.global_card_buffs = {
            "BEETLE_TOKEN": {"attack": 0, "health": 0},
        }

        # Buff دائمی مخصوص Tribe (مثل Undead +Attack)
        self.global_tribe_buffs = {
            "Undead": {"attack": 0, "health": 0},
            "Beast": {"attack": 0, "health": 0},
            "Demon": {"attack": 0, "health": 0},
        }

        self.death_queue = []

    #Utils

    def deal_hero_damage(self, amount):
        self.player_hp -= amount
        if self.player_hp < 0:
            self.player_hp = 0

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

        # 2) تریبی
        if minion.tribe in self.global_tribe_buffs:
            tb = self.global_tribe_buffs[minion.tribe]
            minion.buff(tb["attack"], tb["health"])

    def notify_friendly_minion_played(self, played_minion):
        # همه‌ی مینیون‌های برد می‌تونن به play شدن یک مینیون واکنش نشون بدن
        for m in self.board:
            m.on_friendly_minion_played(self, played_minion)

    def play_minion(self, minion, position=None):
        """
        این تابع “Play از دست به برد” را شبیه‌سازی می‌کند.
        بعداً UI دقیقاً همین را صدا می‌زند (به جای summon مستقیم).
        """
        # Battlecry فقط هنگام Play
        if "Battlecry" in minion.keywords:
            minion.on_play(self)

        # buffهای دائمی (کارت-محور و تریبی)
        self.apply_global_buffs(minion)

        # روی برد قرار می‌گیرد
        ok = self.add_to_board(minion, position)
        if not ok:
            return False

        # بعد از Play، سایر مینیون‌ها (مثل Wrath Weaver) تریگر می‌شوند
        self.notify_friendly_minion_played(minion)
        return True

    def summon_minion(self, card_id, position=None):
        """
        فعلاً (بدون UI) summon_minion هم Play حساب می‌شود
        تا بتوانیم منطق کارت‌ها را تست کنیم.
        """
        from common.minion import (
            BeetleToken, SkeletonToken, HandToken,
            BuzzingVermin, ForestRover, NestSwarmer, TurquoiseSkitterer, MonstrousMacaw,
            HarmlessBonehead, HandlessForsaken, NerubianDeathswarmer,
            WrathWeaver
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

            "WRATH_WEAVER": WrathWeaver,
        }

        if card_id not in mapping:
            print("Unknown card_id:", card_id)
            return False

        minion = mapping[card_id]()
        return self.play_minion(minion, position)

    #Deathrattle trigger (Macaw)

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

    #Death processing

    def collect_deaths_left_to_right(self):
        for m in self.board:
            if m.dead and m not in self.death_queue:
                self.death_queue.append(m)

    def process_deaths(self):
        self.collect_deaths_left_to_right()

        while self.death_queue:
            dying = self.death_queue.pop(0)

            if dying not in self.board:
                continue

            # مثل بازی: اول حذف، بعد deathrattle
            self.board.remove(dying)

            if "Deathrattle" in dying.keywords:
                dying.on_deathrattle(self)

            self.collect_deaths_left_to_right()

    #Test helpers

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
        print("Player HP:", self.player_hp)
        print("===================")



