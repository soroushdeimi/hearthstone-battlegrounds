# common/minion.py

class Minion:
    """
    مدل پایه‌ی همه‌ی مینیون‌ها.
    اینجا فقط دیتا + رفتارهای عمومی (HP, Damage, Keywords, ...) را نگه می‌داریم.
    رفتارهای خاص هر کارت در subclass ها override می‌شود.
    """

    def __init__(self, card_id, name, tier, attack, health, tribe=None, keywords=None):
        self.card_id = card_id
        self.name = name
        self.tier = tier
        self.attack = attack
        self.health = health
        self.tribe = tribe

        # keywords را همیشه به set تبدیل می‌کنیم تا:
        # - چک کردن سریع باشد
        # - تکراری نشود
        self.keywords = set(keywords) if keywords else set()

        self.is_golden = False
        self.dead = False

    def is_alive(self):
        return self.health > 0 and not self.dead

    def has_keyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def take_damage(self, damage: int):
        """
        HP را کم می‌کند و اگر HP <= 0 شد dead=True می‌کند.
        توجه: اینجا Deathrattle اجرا نمی‌کنیم؛ اجرای مرگ و deathrattle کار GameState است.
        """
        if self.dead:
            return True  # اگر قبلاً مرده بود

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

    # ---- Hooks: در subclass ها override می‌شوند ----
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


# ---------------- Token Minions ----------------

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


# ---------------- Main Minions ----------------

class BuzzingVermin(Minion):
    """
    Taunt + Deathrattle: summon a 1/1 Beetle
    """
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



