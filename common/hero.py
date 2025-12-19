class Hero:
    def __init__(
        self,
        hero_id,
        name,
        power_name,
        power_cost,
        power_type,          # "active" یا "passive"
        requires_target=False,
        uses_per_turn=0
    ):
        self.hero_id = hero_id
        self.name = name
        self.power_name = power_name
        self.power_cost = power_cost
        self.power_type = power_type
        self.requires_target = requires_target
        self.uses_per_turn = uses_per_turn

    def can_use_power(self, player_state):
        if self.power_type != "active":
            return False
        if player_state.hero_power_uses_left <= 0:
            return False
        if player_state.gold < self.power_cost:
            return False
        return True

    def use_power(self, match_state, player_id, target=None):
        player = match_state.get_player(player_id)

        if not self.can_use_power(player):
            return False, "Cannot use hero power"

        if self.requires_target and target is None:
            return False, "Target required"

        if not match_state.spend_gold(player_id, self.power_cost):
            return False, "Not enough gold"

        player.hero_power_uses_left -= 1

        #Hero power logic (pre-UI)

        # Yogg-Saron: Add random minion from current tier to hand
        if self.hero_id == "YOGG":
            card_id = match_state.get_random_minion_from_tier(player.tavern_tier)
            if card_id is None:
                return False, "NoMinionsInTierPool"

            ok, msg = match_state.add_to_hand(player_id, card_id)
            if not ok:
                return False, msg

            return True, f"Yogg added {card_id} to hand"

        # Lich King: Give a friendly minion Reborn for next combat only
        if self.hero_id == "LICH_KING":
            if target not in player.board:
                return False, "Invalid target"

            target.reborn_next_combat = True
            return True, f"Lich King gave Reborn to {target.name} (next combat)"

        # Sylvanas: Give +2/+1 to your minions that died last combat
        if self.hero_id == "SYLVANAS":
            buffed = 0
            for m in player.board:
                if m.card_id in player.dead_last_combat_card_ids and m.is_alive():
                    m.buff(attack=2, health=1)
                    buffed += 1
            return True, f"Sylvanas buffed {buffed} minion(s) (+2/+1) from last combat deaths"

        return True, "Hero power used (logic not implemented yet)"

    def __repr__(self):
        return f"<Hero {self.name} | Power: {self.power_name}>"



