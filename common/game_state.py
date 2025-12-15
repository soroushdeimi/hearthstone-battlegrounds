
class GameState:
    def __init__(self):
        self.board = []
        self.max_board = 7

        # Buff دائمی برای کارت‌های خاص (مثل Beetle)
        # کلیدش card_id است، نه tribe
        self.global_card_buffs = {
            "BEETLE_TOKEN": {"attack": 0, "health": 0},
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
        # فقط اگر card_id این مینیون buff دائمی داشته باشد
        if minion.card_id in self.global_card_buffs:
            buff = self.global_card_buffs[minion.card_id]
            minion.buff(buff["attack"], buff["health"])

    def summon_minion(self, card_id, position=None):
        from common.minion import BeetleToken, BuzzingVermin, ForestRover

        if card_id == "BEETLE_TOKEN":
            minion = BeetleToken()
        elif card_id == "BUZZING_VERMIN":
            minion = BuzzingVermin()
        elif card_id == "FOREST_ROVER":
            minion = ForestRover()
        else:
            print("Unknown card_id:", card_id)
            return False

        # Battlecry فقط هنگام Play (فعلاً چون hand نداریم، در summon اجرا می‌کنیم)
        if "Battlecry" in minion.keywords:
            minion.on_play(self)

        # Buffهای دائمی کارت-محور قبل از رفتن روی برد اعمال می‌شود
        self.apply_global_buffs(minion)

        return self.add_to_board(minion, position)

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

            if "Deathrattle" in dying.keywords:
                dying.on_deathrattle(self)

            self.board.remove(dying)
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



