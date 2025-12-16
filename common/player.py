class PlayerState:
    def __init__(self, player_id, hero):
        self.player_id = player_id
        self.hero = hero

        self.hp = 30
        self.gold = 3          # طبق داک: شروع بازی 3 طلا
        self.tavern_tier = 1

        self.board = []
        self.hand = []

        self.hero_power_uses_left = 0

        # برای Sylvanas (بعداً توسط combat پر می‌شود)
        self.dead_last_combat_card_ids = set()

        # ---- Economy modifiers (برای Millhouse و آینده) ----
        self.minion_buy_cost = 3
        self.refresh_cost = 1
        self.tavern_upgrade_extra_cost = 0

    def __repr__(self):
        return (
            f"<Player {self.player_id} | Hero={self.hero.name} "
            f"| HP={self.hp} Gold={self.gold} PowerUsesLeft={self.hero_power_uses_left}>"
        )


      
