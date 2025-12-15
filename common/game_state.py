# common/game_state.py

class GameState:
    """
    نسخه‌ی مینیمال GameState برای یک Board.
    هدف این فاز:
    - اضافه کردن مینیون به برد
    - وارد کردن دمیج
    - جمع‌کردن مرده‌ها (Death Queue)
    - اجرای Deathrattle ها به ترتیب چپ->راست
    - حذف مرده‌ها از برد
    """

    def __init__(self):
        self.board = []
        self.max_board = 7

        # صف مرگ: به ترتیب چپ->راست پر می‌شود، بعد پردازش می‌شود
        self.death_queue = []

    def add_to_board(self, minion, position=None):
        """اضافه کردن مینیون به برد (Summon/Play)."""
        if len(self.board) >= self.max_board:
            print("Board is full, cannot summon:", minion.name)
            return False

        if position is None or position >= len(self.board):
            self.board.append(minion)
        else:
            self.board.insert(position, minion)

        print("Summoned on board:", minion)
        return True

    def summon_minion(self, card_id, position=None):
        """
        یک minion جدید از روی card_id می‌سازد و به برد اضافه می‌کند.
        فعلاً ساده: فقط کارت‌هایی که تا این لحظه داریم.
        """
        from common.minion import BeetleToken, BuzzingVermin

        if card_id == "BEETLE_TOKEN":
            minion = BeetleToken()
        elif card_id == "BUZZING_VERMIN":
            minion = BuzzingVermin()
        else:
            print("Unknown card_id:", card_id)
            return False

        return self.add_to_board(minion, position)

    # ---------------- Death Processing ----------------

    def queue_death(self, minion):
        """
        یک مینیون را وارد صف مرگ می‌کند (فقط اگر:
        - روی برد باشد
        - dead باشد
        - و قبلاً در صف نبوده باشد)
        """
        if minion in self.board and minion.dead and minion not in self.death_queue:
            self.death_queue.append(minion)

    def collect_deaths_left_to_right(self):
        """
        هر بار که می‌خواهیم death ها را پردازش کنیم،
        اول از چپ به راست کل برد را می‌گردیم و dead ها را وارد صف می‌کنیم.
        """
        for m in self.board:
            if m.dead:
                self.queue_death(m)

    def process_deaths(self):
        """
        منطق اصلی:
        1) dead ها را چپ->راست وارد صف می‌کنیم
        2) از صف یکی یکی برمی‌داریم:
           - اگر Deathrattle دارد: اجرا
           - سپس از برد حذف می‌کنیم
        3) چون Deathrattle ممکن است summon کند، ممکن است در حین کار دوباره مرگ رخ دهد
           پس هر بار بعد از اجرای یک Deathrattle دوباره collect انجام می‌دهیم.
        """
        # مرحله 1: جمع‌کردن مرده‌ها
        self.collect_deaths_left_to_right()

        # مرحله 2: پردازش صف
        while self.death_queue:
            dying = self.death_queue.pop(0)  # FIFO

            # ممکن است قبلاً از برد حذف شده باشد (در chain ها)
            if dying not in self.board:
                continue

            # اجرای Deathrattle اگر keyword داشته باشد
            if "Deathrattle" in dying.keywords:
                dying.on_deathrattle(self)

            # حذف از برد
            self.board.remove(dying)

            # بعد از هر تغییر (deathrattle/summon)، دوباره مرگ‌ها را جمع می‌کنیم
            self.collect_deaths_left_to_right()

    # ---------------- Utility / Debug ----------------

    def deal_damage_to_slot(self, slot_index, damage):
        """
        یک helper برای تست:
        به مینیون اسلات مشخص damage می‌زند و بعد process_deaths را اجرا می‌کند.
        """
        if slot_index < 0 or slot_index >= len(self.board):
            print("Invalid slot:", slot_index)
            return

        target = self.board[slot_index]
        target.take_damage(damage)

        # بعد از damage، مرگ‌ها و deathrattle ها را پردازش می‌کنیم
        self.process_deaths()

    def debug_print_board(self):
        print("=== BOARD STATE ===")
        if not self.board:
            print("Board is empty.")
        else:
            for i, m in enumerate(self.board):
                print(f"{i}: {m}")
        print("===================")
