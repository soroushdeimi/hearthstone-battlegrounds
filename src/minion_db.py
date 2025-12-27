MINIONS_DB = {

    "buzzing_vermin": {
        "id": "buzzing_vermin",
        "name": "Buzzing Vermin",
        "tier": 1,
        "base_attack": 2,
        "base_health": 3,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["taunt", "deathrattle"],
        "deathrattle_effect": {"type": "summon", "minion_id": "beetle_token", "count": 1}
    },

    "forest_rover": {
        "id": "forest_rover",
        "name": "Forest Rover",
        "tier": 2,
        "base_attack": 3,
        "base_health": 3,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["battlecry", "deathrattle"],
        "battlecry_effect": {"type": "buff_all_tribe", "tribe": "beetle", "atk": 1, "hp": 1},
        "deathrattle_effect": {"type": "summon", "minion_id": "beetle_token", "count": 1}
    },

    "sprightly_scarab": {
        "id": "sprightly_scarab",
        "name": "Sprightly Scarab",
        "tier": 2,
        "base_attack": 2,
        "base_health": 2,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["battlecry"],
        "battlecry_effect": {
            "type": "choose_one",
            "options": [
                {"atk": 1, "hp": 1, "ability": "reborn"},
                {"atk": 4, "hp": 0, "ability": "windfury"}
            ]
        }
    },

    "turquoise_skitterer": {
        "id": "turquoise_skitterer",
        "name": "Turquoise Skitterer",
        "tier": 3,
        "base_attack": 4,
        "base_health": 4,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["deathrattle"],
        "deathrattle_effect": {"type": "buff_all_tribe_permanent", "tribe": "beetle", "atk": 1, "hp": 2}
    },

    "nest_swarmer": {
        "id": "nest_swarmer",
        "name": "Nest Swarmer",
        "tier": 3,
        "base_attack": 2,
        "base_health": 4,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["deathrattle"],
        "deathrattle_effect": {"type": "summon", "minion_id": "beetle_token", "count": 3}
    },

    "monstrous_macaw": {
        "id": "monstrous_macaw",
        "name": "Monstrous Macaw",
        "tier": 4,
        "base_attack": 4,
        "base_health": 3,
        "cost": 3,
        "tribe": "beetle",
        "abilities": ["deathrattle"],
        "on_attack_after": {"type": "trigger_leftmost_deathrattle"}
    },

    "wrath_weaver": {
        "id": "wrath_weaver",
        "name": "Wrath Weaver",
        "tier": 1,
        "base_attack": 1,
        "base_health": 3,
        "cost": 3,
        "tribe": "demon",
        "abilities": [],
        "on_play_demon": {"type": "self_buff", "atk": 2, "hp": 2, "hero_damage": 1}
    },

    "imp_mama": {
        "id": "imp_mama",
        "name": "Imp Mama",
        "tier": 4,
        "base_attack": 6,
        "base_health": 8,
        "cost": 3,
        "tribe": "demon",
        "abilities": ["taunt", "deathrattle"],
        "deathrattle_effect": {"type": "summon_random_demon", "count": 1}
    },

    "false_implicator": {
        "id": "false_implicator",
        "name": "False Implicator",
        "tier": 2,
        "base_attack": 3,
        "base_health": 3,
        "cost": 3,
        "tribe": "demon",
        "abilities": [],
        "end_of_turn_effect": {"type": "consume_shop", "multiplier": 1}
    },

    "furious_driver": {
        "id": "furious_driver",
        "name": "Furious Driver",
        "tier": 3,
        "base_attack": 4,
        "base_health": 4,
        "cost": 3,
        "tribe": "demon",
        "abilities": ["battlecry"],
        "battlecry_effect": {"type": "trigger_demon_consume", "multiplier": 1}
    },

    "famished_felbat": {
        "id": "famished_felbat",
        "name": "Famished Felbat",
        "tier": 5,
        "base_attack": 6,
        "base_health": 6,
        "cost": 3,
        "tribe": "demon",
        "abilities": [],
        "end_of_turn_effect": {"type": "trigger_demon_consume", "multiplier": 2}
    },

    "harmless_bonehead": {
        "id": "harmless_bonehead",
        "name": "Harmless Bonehead",
        "tier": 1,
        "base_attack": 1,
        "base_health": 2,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["deathrattle"],
        "deathrattle_effect": {"type": "summon", "minion_id": "skeleton_token", "count": 2}
    },

    "handless_forsaken": {
        "id": "handless_forsaken",
        "name": "Handless Forsaken",
        "tier": 2,
        "base_attack": 3,
        "base_health": 2,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["deathrattle"],
        "deathrattle_effect": {"type": "summon", "minion_id": "hand_token", "count": 1}
    },

    "nerubian_deathswarmer": {
        "id": "nerubian_deathswarmer",
        "name": "Nerubian Deathswarmer",
        "tier": 2,
        "base_attack": 3,
        "base_health": 2,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["battlecry"],
        "battlecry_effect": {"type": "buff_all_tribe_permanent", "tribe": "undead", "atk": 1, "hp": 0}
    },

    "eternal_knight": {
        "id": "eternal_knight",
        "name": "Eternal Knight",
        "tier": 3,
        "base_attack": 4,
        "base_health": 4,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["start_of_combat"],
        "start_of_combat_effect": {"type": "scale_with_deaths", "value": 1}
    },

    "eternal_summoner": {
        "id": "eternal_summoner",
        "name": "Eternal Summoner",
        "tier": 4,
        "base_attack": 5,
        "base_health": 3,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["reborn", "deathrattle"],
        "deathrattle_effect": {"type": "summon", "minion_id": "eternal_knight", "count": 2}
    },

    "catacomb_crasher": {
        "id": "catacomb_crasher",
        "name": "Catacomb Crasher",
        "tier": 4,
        "base_attack": 4,
        "base_health": 6,
        "cost": 3,
        "tribe": "undead",
        "abilities": [],
        "on_board_full_summon": {"type": "buff_board", "atk": 1, "hp": 1}
    },

    "titus_rivendare": {
        "id": "titus_rivendare",
        "name": "Titus Rivendare",
        "tier": 5,
        "base_attack": 4,
        "base_health": 4,
        "cost": 3,
        "tribe": "undead",
        "abilities": ["aura"],
        "aura_effect": {"type": "double_deathrattle"}
    },

    "beetle_token": {
        "id": "beetle_token",
        "name": "Beetle",
        "tier": 1,
        "base_attack": 1,
        "base_health": 1,
        "cost": 0,
        "tribe": "beetle",
        "abilities": [],
        "is_token": True
    },

    "skeleton_token": {
        "id": "skeleton_token",
        "name": "Skeleton",
        "tier": 1,
        "base_attack": 1,
        "base_health": 1,
        "cost": 0,
        "tribe": "undead",
        "abilities": [],
        "is_token": True
    },

    "hand_token": {
        "id": "hand_token",
        "name": "Hand",
        "tier": 2,
        "base_attack": 2,
        "base_health": 1,
        "cost": 0,
        "tribe": "undead",
        "abilities": ["reborn"],
        "is_token": True
    }
}
