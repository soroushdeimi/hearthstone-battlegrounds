# Mock Payloads & Schema Definitions

این فایل شامل تمام **Payload**های **JSON** مورد نیاز برای شبیه‌سازی وضعیت‌های مختلف کلاینت (**Recruit**, **Combat**, **Errors**) و تست آفلاین می‌باشد.

## 1. `data/mock_state.json`

**Snapshot کامل وضعیت Recruit**: شامل فروشگاه، برد، دست، تایمرها و فلگ‌ها.

```json
{
  "match_id": "mock-001",
  "players": [
    {
      "player_id": "p1",
      "hero": "Ragnaros",
      "health": 40,
      "armor": 0,
      "tavern_tier": 2,
      "gold": 7,
      "timer_ms": 30000,
      "shop": [
        {"slot": 0, "card_id": "BG_FRONT_001", "frozen": false, "sim_tier": 1},
        {"slot": 1, "card_id": "BG_FRONT_006", "frozen": true, "sim_tier": 3},
        {"slot": 2, "card_id": "BG_FRONT_009", "frozen": false, "sim_tier": 2}
      ],
      "board": [
        {"slot": 0, "instance_id": "inst-100", "card_id": "BG_FRONT_009",
         "attack": 2, "health": 4, "keywords": ["Taunt"], "has_divine_shield": false, "reborn_used": false},
        {"slot": 3, "instance_id": "inst-102", "card_id": "BG_FRONT_015",
         "attack": 3, "health": 4, "keywords": [], "has_divine_shield": false, "reborn_used": false}
      ],
      "hand": [
        {"hand_index": 0, "instance_id": "inst-200", "card_id": "BG_FRONT_014", "attack": 3, "health": 2}
      ],
      "flags": {"shop_frozen": true, "ready": false}
    },
    {
      "player_id": "p2",
      "hero": "Sylvanas",
      "health": 37,
      "armor": 2,
      "tavern_tier": 2,
      "gold": 7,
      "timer_ms": 30000,
      "shop": [],
      "board": [],
      "hand": [],
      "flags": {"shop_frozen": false, "ready": true}
    }
  ]
}
```

## 2. Recruit Phase Deltas (`state_delta_01.json`, `state_delta_02.json`)

اعمال تغییرات سمت سرور بدون ریلود کامل (ساختار `events[]` مطابق با بک‌اند واقعی).

```json
{
  "type": "state_delta",
  "match_id": "mock-001",
  "events": [
    {"op": "gold", "player_id": "p1", "value": 6},
    {"op": "shop_update", "player_id": "p1", "slots": [
      {"index": 1, "card_id": "BG_FRONT_020", "frozen": false, "sim_tier": 2}
    ]},
    {"op": "hand_add", "player_id": "p1",
     "card": {"hand_index": 1, "instance_id": "inst-201", "card_id": "BG_FRONT_020", "attack": 2, "health": 2}},
    {"op": "board_insert", "player_id": "p1", "slot": 4,
     "instance_id": "inst-300", "card_id": "BG_FRONT_003", "attack": 1, "health": 3, "keywords": ["Deathrattle"]},
    {"op": "log", "level": "info", "message": "Bought BG_FRONT_020"},
    {"op": "timer_tick", "player_id": "p1", "value": 25000}
  ],
  "server_time_ms": 1697045234123,
  "request_id": "uuid-123"
}
```

> **نکته:** از همین ساختار برای عملیات `board_update`, `board_remove`, `freeze_state`, `hero_health`, `armor` و غیره استفاده می‌شود.

## 3. `combat_start.json`

اولین پیلود نبرد (شامل بردهای نهایی، **Seed** تصادفی و مشخص کردن شروع‌کننده).

```json
{
  "type": "combat_start",
  "match_id": "mock-001",
  "pairing": ["p1", "p2"],
  "combat_seed": 834752,
  "first_attacker": "p2",
  "boards": {
    "p1": [
      {"slot": 0, "instance_id": "inst-100", "card_id": "BG_FRONT_009", "attack": 3, "health": 2, "keywords": ["Taunt"]},
      {"slot": 2, "instance_id": "inst-102", "card_id": "BG_FRONT_015", "attack": 5, "health": 4, "keywords": []}
    ],
    "p2": [
      {"slot": 1, "instance_id": "inst-500", "card_id": "BG_FRONT_050", "attack": 4, "health": 4, "keywords": ["Deathrattle"]}
    ]
  }
}
```

## 4. Combat Events (`combat_event_attack.json`, `combat_event_deathrattle.json`)

فرمت استاندارد انیمیشن‌ها (`type=combat_event`, `payload.kind=...`).

### Attack start

```json
{
  "type": "combat_event",
  "event_uuid": "evt-001",
  "step": 1,
  "payload": {
    "kind": "attack_start",
    "attacker": {"player_id": "p2", "slot": 1, "instance_id": "inst-500"},
    "defender": {"player_id": "p1", "slot": 0, "instance_id": "inst-100"}
  }
}
```

### Deathrattle + Summon

```json
{
  "type": "combat_event",
  "event_uuid": "evt-004",
  "step": 4,
  "payload": {
    "kind": "deathrattle_trigger",
    "source": {"player_id": "p2", "slot": 1, "instance_id": "inst-500"},
    "summons": [
      {"player_id": "p2", "card_id": "BG_TOKEN_SCARAB_22", "attack": 2, "health": 2, "slot": null}
    ],
    "log": "Buzzing Vermin summons a 2/2 Scarab."
  }
}
```

> **نکته:** نیاز به ایونت دیگری دارید؟ یک `payload.kind` جدید بسازید (مثلاً `stat_change`) با داده‌هایی که انیمیشن شما نیاز دارد.

## 5. `combat_result.json`

محاسبه دمیج هیرو و بازماندگان. نمایش صفحه نتیجه پس از لاگ کردن ایونت‌ها.

```json
{
  "type": "combat_result",
  "match_id": "mock-001",
  "pairing": ["p1", "p2"],
  "damage": {"p2": 6},
  "survivors": {
    "p1": [
      {"instance_id": "inst-102", "card_id": "BG_FRONT_015", "attack": 6, "health": 2}
    ],
    "p2": []
  },
  "digest": "sha256:0f3a..."
}
```

## 6. Discover & Choose-One

مکانیزم‌های انتخاب کارت (**Discover**) و افکت‌های انتخابی (**Choose One**).

### `discover_offer.json`

```json
{
  "type": "discover_offer",
  "request_id": "uuid-456",
  "player_id": "p1",
  "source": "BG_FRONT_006",
  "options": [
    {"card_id": "BG_FRONT_010", "sim_tier": 2},
    {"card_id": "BG_FRONT_013", "sim_tier": 3},
    {"card_id": "BG_FRONT_015", "sim_tier": 3}
  ]
}
```

### `discover_choice.json` (فرمانی که کلاینت می‌فرستد)

**نکته مهم:** این درخواست برای امنیت بیشتر به‌روزرسانی شد (استفاده از token به جای player_id).

```json
{
  "action": "DISCOVER_CHOICE",
  "token": "user-uuid-1234",
  "payload": {
    "request_id": "uuid-456",
    "card_id": "BG_FRONT_013"
  }
}
```

### `choose_one_resolve.json` (نتیجه انتخاب - مثال Sprightly Scarab)

```json
{
  "type": "state_delta",
  "events": [
    {"op": "board_update", "player_id": "p1", "slot": 1,
     "instance_id": "inst-447",
     "attack": 7,
     "health": 1,
     "keywords": ["Windfury"],
     "meta": {"choice": "aggressive"}}
  ],
  "request_id": "uuid-789"
}
```

## 7. Error & Session Samples

نمونه‌ها برای نمایش در پنل لاگ یا **Toast** ارورها.

### `error.json`

```json
{
  "type": "error",
  "code": "ERR_INVALID_SLOT",
  "message": "Board slot 5 is occupied",
  "request_id": "uuid-123",
  "retryable": false
}
```

### `session_closed.json`

```json
{
  "type": "session_closed",
  "reason": "timeout",
  "match_id": "mock-001"
}
```

## 8. Offline Server Mock Pack

مجموعه فایل‌ها برای اجرای کامل حالت آفلاین (**Lobby** / **Advanced Recruit** / **Combat** / **Errors**). قابل استفاده با فلگ: `--offline data/mock_combat_log_advanced.json`.

### `data/mock_lobby_wait.json`

```json
{
  "type": "server_message",
  "code": "WAITING_FOR_OPPONENT",
  "message": "Waiting for opponent..."
}
```

### `data/mock_recruit_state_advanced.json`

اسنپ‌شات اواسط بازی: **Sylvanas** vs **Lich King**، مینیون‌های **Golden**، اسلات‌های خالی فروشگاه و وضعیت **Hero Power**.

```json
{
  "match_id": "mock-adv-001",
  "phase": "recruit",
  "turn": 5,
  "players": [
    {
      "player_id": "p1",
      "hero": {
        "card_id": "BG23_HERO_306",
        "name": "Sylvanas Windrunner",
        "health": 30,
        "armor": 0,
        "hero_power_cost": 1,
        "hero_power_used": false
      },
      "gold": 7,
      "max_gold": 7,
      "tavern_tier": 3,
      "upgrade_cost": 5,
      "refresh_cost": 1,
      "timer_ms": 18000,
      "flags": {
        "shop_frozen": false,
        "ready": false
      },
      "board": [
        {
          "slot": 0,
          "instance_id": "inst-p1-001",
          "card_id": "OG_256",
          "name": "Spawn of N'Zoth",
          "base_attack": 2,
          "base_health": 2,
          "attack": 3,
          "health": 3,
          "tier": 2,
          "is_golden": false,
          "keywords": ["Deathrattle", "Taunt"],
          "has_divine_shield": false,
          "reborn_used": false
        },
        {
          "slot": 2,
          "instance_id": "inst-p1-002",
          "card_id": "GVG_102",
          "name": "Micro Machine",
          "base_attack": 1,
          "base_health": 2,
          "attack": 4,
          "health": 2,
          "tier": 1,
          "is_golden": true,
          "keywords": [],
          "has_divine_shield": false,
          "reborn_used": false
        }
      ],
      "hand": [
        {
          "hand_index": 0,
          "instance_id": "hand-p1-001",
          "card_id": "CFM_315",
          "name": "Alleycat",
          "attack": 1,
          "health": 1,
          "tier": 1,
          "is_golden": false,
          "keywords": []
        }
      ],
      "shop": [
        {
          "slot": 0,
          "card_id": "KAR_004",
          "name": "Kindly Grandmother",
          "attack": 1,
          "health": 1,
          "tier": 1,
          "sim_tier": 1,
          "cost": 3,
          "is_golden": false,
          "keywords": ["Deathrattle", "Taunt"]
        },
        null,
        {
          "slot": 2,
          "card_id": "KAR_005",
          "name": "Rat Pack",
          "attack": 2,
          "health": 2,
          "tier": 2,
          "sim_tier": 2,
          "cost": 3,
          "is_golden": false,
          "keywords": ["Deathrattle"]
        },
        {
          "slot": 3,
          "card_id": "GIL_681",
          "name": "Nightmare Amalgam",
          "attack": 3,
          "health": 4,
          "tier": 3,
          "sim_tier": 3,
          "cost": 3,
          "is_golden": false,
          "keywords": ["Taunt", "Divine Shield"]
        },
        null
      ]
    },
    {
      "player_id": "p2",
      "hero": {
        "card_id": "TB_BaconShop_HERO_22",
        "name": "The Lich King",
        "health": 35,
        "armor": 5,
        "hero_power_cost": 0,
        "hero_power_used": true
      },
      "gold": 7,
      "max_gold": 7,
      "tavern_tier": 3,
      "upgrade_cost": 5,
      "refresh_cost": 1,
      "timer_ms": 19000,
      "flags": {
        "shop_frozen": true,
        "ready": true
    },
      "board": [
        {
          "slot": 1,
          "instance_id": "inst-p2-001",
          "card_id": "BGS_082",
          "name": "Bronze Warden",
          "base_attack": 2,
          "base_health": 1,
          "attack": 2,
          "health": 1,
          "tier": 3,
          "is_golden": false,
          "keywords": ["Divine Shield", "Reborn"],
          "has_divine_shield": true,
          "reborn_used": false
        }
      ],
      "hand": [],
      "shop": []
    }
  ]
}
```

### `data/mock_combat_log_advanced.json`

اسکریپت نبرد کامل: **Divine Shield**, **Deathrattle**, **Summon**, **Reborn**, **Combat End**.

```json
[
  {
    "type": "combat_start",
    "match_id": "mock-adv-001",
    "combat_seed": 112233,
    "first_attacker": "player",
    "boards": {
      "player": [
        {"slot": 0, "instance_id": "inst-p1-002", "card_id": "GVG_102", "name": "Micro Machine", "attack": 4, "health": 2, "keywords": ["Divine Shield"]},
        {"slot": 1, "instance_id": "inst-p1-003", "card_id": "KAR_005", "name": "Rat Pack", "attack": 2, "health": 2, "keywords": ["Deathrattle"]}
      ],
      "opponent": [
        {"slot": 0, "instance_id": "inst-p2-001", "card_id": "BGS_082", "name": "Bronze Warden", "attack": 2, "health": 1, "keywords": ["Divine Shield", "Reborn"]}
      ]
    }
  },
  {"type": "combat_event", "event_uuid": "evt-100", "step": 1, "payload": {"kind": "set_attacker", "player": "player", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-101", "step": 2, "payload": {"kind": "set_target", "player": "opponent", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-102", "step": 3, "payload": {"kind": "attack_start", "attacker": {"player": "player", "slot": 0}, "defender": {"player": "opponent", "slot": 0}}},
  {"type": "combat_event", "event_uuid": "evt-103", "step": 4, "payload": {"kind": "divine_shield_pop", "player": "opponent", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-104", "step": 5, "payload": {"kind": "divine_shield_pop", "player": "player", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-105", "step": 6, "payload": {"kind": "set_attacker", "player": "opponent", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-106", "step": 7, "payload": {"kind": "set_target", "player": "player", "slot": 1}},
  {"type": "combat_event", "event_uuid": "evt-107", "step": 8, "payload": {"kind": "attack_start", "attacker": {"player": "opponent", "slot": 0}, "defender": {"player": "player", "slot": 1}}},
  {"type": "combat_event", "event_uuid": "evt-108", "step": 9, "payload": {"kind": "damage_resolve", "entries": [
    {"player": "player", "slot": 1, "amount": 2, "new_health": 0},
    {"player": "opponent", "slot": 0, "amount": 2, "new_health": -1}
  ]}},
  {"type": "combat_event", "event_uuid": "evt-109", "step": 10, "payload": {"kind": "minion_died", "player": "player", "slot": 1}},
  {"type": "combat_event", "event_uuid": "evt-110", "step": 11, "payload": {"kind": "minion_died", "player": "opponent", "slot": 0}},
  {"type": "combat_event", "event_uuid": "evt-111", "step": 12, "payload": {"kind": "deathrattle_trigger", "player": "player", "slot": 1, "log": "Rat Pack summons two Rats"}},
  {"type": "combat_event", "event_uuid": "evt-112", "step": 13, "payload": {"kind": "summon", "player": "player", "card_id": "KAR_005t", "name": "Rat", "slot": 1, "attack": 1, "health": 1}},
  {"type": "combat_event", "event_uuid": "evt-113", "step": 14, "payload": {"kind": "summon", "player": "player", "card_id": "KAR_005t", "name": "Rat", "slot": 2, "attack": 1, "health": 1}},
  {"type": "combat_event", "event_uuid": "evt-114", "step": 15, "payload": {"kind": "reborn_spawn", "player": "opponent", "slot": 0, "card_id": "BGS_082", "name": "Bronze Warden", "attack": 2, "health": 1, "keywords": ["Divine Shield"], "reborn_used": true}},
  {"type": "combat_event", "event_uuid": "evt-115", "step": 16, "payload": {"kind": "combat_end", "winner": "player", "damage_to_hero": 5}}
]
```

### `data/mock_error_not_enough_coins.json`

```json
{
  "type": "error",
  "code": "NOT_ENOUGH_COINS",
  "message": "Not enough coins to buy this minion.",
  "request_id": "cmd-buy-001",
  "retryable": false
}
```

### `data/mock_error_board_full.json`

```json
{
  "type": "error",
  "code": "BOARD_IS_FULL",
  "message": "Board is full (max 7 minions).",
  "request_id": "cmd-play-004",
  "retryable": false
}
```

> **نکته:** برای تست در **UI**، سوییچ `--offline <path>` را در `app.py` اضافه کنید تا بتوانید این فایل‌ها را مستقیماً بارگذاری کنید.

## Usage Notes

- تمام فایل‌ها باید در مسیر `data/` با همین نام‌ها نگه داشته شوند—تست‌های خودکار به آنها وابسته‌اند.
- فایل‌ها را به صورت **UTF‑8** (بدون **BOM**) ذخیره کنید و قبل از merge یک بررسی سریع **JSON-schema** انجام دهید تا از خطاهای parsing غیرمنتظره جلوگیری شود.

> در صورت نیاز به اضافه کردن شمای **JSON Schema** دقیق (مانند `json-schema.org`) برای اعتبارسنجی خودکار این فایل‌ها، بفرمایید تا بخش `definitions` را نیز اضافه کنم.
