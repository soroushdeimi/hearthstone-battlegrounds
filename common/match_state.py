from common.player import PlayerState
import random

class MatchState:
    def __init__(self, rng_seed=123):
        self.players = {}
        self.current_player_id = None

        # RNG برای تست‌های deterministic (هم‌تیمی UI هم خروجی ثابت می‌بیند)
        self.rng = random.Random(rng_seed)

        # Pool خیلی ساده برای Pre-UI
        # فقط چند نمونه کافی است؛ بعداً کاملش می‌کنید یا از data می‌خوانید.
        self.minion_pool_by_tier = {
            1: ["BEETLE_TOKEN", "BUZZING_VERMIN", "HARMLESS_BONEHEAD", "WRATH_WEAVER"],
            2: ["FOREST_ROVER", "NEST_SWARMER", "HANDLESS_FORSAKEN", "NERUBIAN_DEATHSWARMER"],
            3: ["TURQUOISE_SKITTERER", "MONSTROUS_MACAW"],
            4: [],
        }

    def add_player(self, player_id, hero):
        player = PlayerState(player_id, hero)

        # Passive effects هنگام اضافه شدن بازیکن اعمال می‌شوند
        if hero.hero_id == "MILLHOUSE":
            player.minion_buy_cost = 2
            player.refresh_cost = 2
            player.tavern_upgrade_extra_cost = 1
            player.gold = 3

        self.players[player_id] = player

        if self.current_player_id is None:
            self.current_player_id = player_id

    def get_player(self, player_id):
        return self.players[player_id]

    def start_turn(self, player_id):
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

    # Hand helpers (برای UI و Yogg)

    def add_to_hand(self, player_id, card_id):
        player = self.get_player(player_id)

        if len(player.hand) >= 10:
            return False, "HandFull"

        player.hand.append(card_id)
        return True, "AddedToHand"

    def get_random_minion_from_tier(self, tier):
        pool = self.minion_pool_by_tier.get(tier, [])
        if not pool:
            return None
        return self.rng.choice(pool)



