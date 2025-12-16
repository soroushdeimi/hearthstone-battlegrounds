from common.player import PlayerState

class MatchState:
    def __init__(self):
        self.players = {}
        self.current_player_id = None

    def add_player(self, player_id, hero):
        player = PlayerState(player_id, hero)

        # Passive effects هنگام اضافه شدن بازیکن اعمال می‌شوند
        if hero.hero_id == "MILLHOUSE":
            # Millhouse Passive طبق داک:
            # Minions cost 2, Refresh cost 2, Tavern upgrades +1 cost, Start with 3 gold
            player.minion_buy_cost = 2
            player.refresh_cost = 2
            player.tavern_upgrade_extra_cost = 1
            player.gold = 3  # همچنان 3 است، فقط تاکید

        self.players[player_id] = player

        if self.current_player_id is None:
            self.current_player_id = player_id

    def get_player(self, player_id):
        return self.players[player_id]

    def start_turn(self, player_id):
        """
        شروع نوبت:
        - طلا +1 تا سقف 10
        - ریست تعداد استفاده Hero Power در این نوبت
        """
        player = self.get_player(player_id)

        if player.gold < 10:
            player.gold += 1
            if player.gold > 10:
                player.gold = 10

        player.hero_power_uses_left = player.hero.uses_per_turn
        self.current_player_id = player_id

    def spend_gold(self, player_id, amount):
        player = self.get_player(player_id)
        if player.gold < amount:
            return False
        player.gold -= amount
        return True


