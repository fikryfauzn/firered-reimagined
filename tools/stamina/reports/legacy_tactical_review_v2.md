# Stamina V2 — Legacy Review Batch 02

## Tactical Semantics

Moves in batch: **29**

These moves require human cost review because their tactical behavior changed in ways not captured by raw power alone.

## MOVE_SURF — Surf

- V1 cost: **4**
- V1 role: `damage`
- V1 tags: `direct_damage`, `spread`
- V1 rules: `standard_attempt`

### Migration differences

- `power_changed`
- `target_changed`

```json
{
  "power": {
    "v1": 95,
    "v2": 90,
    "delta": -5
  },
  "target": {
    "v1": "TARGET_BOTH",
    "v2": "TARGET_FOES_AND_ALLY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95`
- Accuracy: `100`
- Type: `TYPE_WATER`
- Category: `DAMAGE_CATEGORY_SPECIAL`
- Target: `B_UPDATED_MOVE_DATA >= GEN_4 ? TARGET_FOES_AND_ALLY : TARGET_BOTH`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "damagesUnderwater": "TRUE",
  "skyBattleBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **21**
- Egg species: **0**
- TM: **False**
- HM: **True**
- Explicit FRLG trainer usage: **7**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_TELEPORT — Teleport

- V1 cost: **1**
- V1 role: `utility`
- V1 tags: `switching`
- V1 rules: `standard_attempt`, `cost_tuning_only`

### Migration differences

- `priority_changed`

```json
{
  "priority": {
    "v1": 0,
    "v2": -6
  }
}
```

### Current mechanics

- Effect: `EFFECT_TELEPORT`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_PSYCHIC`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `B_UPDATED_MOVE_DATA >= GEN_8 ? -6 : 0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RECOVER_HP }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **19**
- Egg species: **1**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **3**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_HAZE — Haze

- V1 cost: **2**
- V1 role: `utility`
- V1 tags: `stat_reset`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HAZE`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_ICE`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RECOVER_HP }",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **29**
- Egg species: **32**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **4**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_BIDE — Bide

- V1 cost: **3**
- V1 role: `damage`
- V1 tags: `counterplay`, `direct_damage`, `reactive_damage`, `special_case`
- V1 rules: `standard_attempt`, `forced_multiturn_single_commit`

### Migration differences

- `accuracy_changed`
- `priority_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "priority": {
    "v1": 0,
    "v2": 1
  }
}
```

### Current mechanics

- Effect: `EFFECT_BIDE`
- Power: `1`
- Accuracy: `(B_UPDATED_MOVE_DATA >= GEN_4 || B_UPDATED_MOVE_DATA == GEN_1) ? 0 : 100`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_USER`
- Priority: `B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "makesContact": "TRUE",
  "sleepTalkBanned": "TRUE",
  "instructBanned": "TRUE",
  "mirrorMoveBanned": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **2**
- Egg species: **12**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **2**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_POISON_GAS — Poison Gas

- V1 cost: **2**
- V1 role: `control`
- V1 tags: `status_poison`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`
- `effect_representation_changed`

```json
{
  "accuracy": {
    "v1": 55,
    "v2": 90,
    "delta": 35
  },
  "target": {
    "v1": "TARGET_SELECTED",
    "v2": "TARGET_BOTH"
  },
  "effect": {
    "v1": "EFFECT_POISON",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### Current mechanics

- Effect: `EFFECT_NON_VOLATILE_STATUS`
- Power: `0`
- Accuracy: `90`
- Type: `TYPE_POISON`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_DATA >= GEN_5 ? TARGET_BOTH : TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "argument": "{ .nonVolatileStatus = MOVE_EFFECT_POISON }",
  "zMove": "{ .effect = Z_EFFECT_DEF_UP_1 }",
  "magicCoatAffected": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **21**
- Egg species: **0**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **8**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_CURSE — Curse

- V1 cost: **3**
- V1 role: `setup`
- V1 tags: `special_case`, `stat_boost_mixed`
- V1 rules: `standard_attempt`

### Migration differences

- `type_changed`
- `v2_additional_effects`

```json
{
  "type": {
    "v1": "TYPE_MYSTERY",
    "v2": "TYPE_GHOST"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "speed": "1"
    },
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "1",
      "defense": "1"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_CURSE`
- Power: `0`
- Accuracy: `0`
- Type: `B_UPDATED_MOVE_TYPES >= GEN_5 ? TYPE_GHOST : TYPE_MYSTERY`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
    "speed": "1"
  },
  {
    "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
    "attack": "1",
    "defense": "1"
  }
]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_CURSE }",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "B_UPDATED_MOVE_FLAGS >= GEN_5",
  "mirrorMoveBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **66**
- Egg species: **77**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **1**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_CONVERSION_2 — Conversion 2

- V1 cost: **1**
- V1 role: `utility`
- V1 tags: `type_change`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_SELECTED"
  }
}
```

### Current mechanics

- Effect: `EFFECT_CONVERSION_2`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_DATA >= GEN_5 ? TARGET_SELECTED : TARGET_USER`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RECOVER_HP }",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "B_UPDATED_MOVE_FLAGS >= GEN_5",
  "mirrorMoveBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **3**
- Egg species: **0**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_COTTON_SPORE — Cotton Spore

- V1 cost: **3**
- V1 role: `control`
- V1 tags: `stat_drop_speed`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "accuracy": {
    "v1": 85,
    "v2": 100,
    "delta": 15
  },
  "target": {
    "v1": "TARGET_SELECTED",
    "v2": "TARGET_BOTH"
  },
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "speed": "2"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_STAT_CHANGE`
- Power: `0`
- Accuracy: `B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 85`
- Type: `TYPE_GRASS`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_DATA >= GEN_6 ? TARGET_BOTH : TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
    "speed": "2"
  }
]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "magicCoatAffected": "TRUE",
  "powderMove": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **14**
- Egg species: **2**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_PROTECT — Protect

- V1 cost: **3**
- V1 role: `protection`
- V1 tags: `counterplay`, `priority`, `protect_like`
- V1 rules: `standard_attempt`

### Migration differences

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### Current mechanics

- Effect: `EFFECT_PROTECT`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `4`

Additional effects:

```json
[]
```

Properties:

```json
{
  "argument": "{ .protectMethod = PROTECT_NORMAL }",
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "TRUE",
  "copycatBanned": "TRUE",
  "assistBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **93**
- Egg species: **0**
- TM: **True**
- HM: **False**
- Explicit FRLG trainer usage: **3**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_SWEET_KISS — Sweet Kiss

- V1 cost: **3**
- V1 role: `control`
- V1 tags: `status_confusion`
- V1 rules: `standard_attempt`

### Migration differences

- `type_changed`

```json
{
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "TYPE_FAIRY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_CONFUSE`
- Power: `0`
- Accuracy: `75`
- Type: `B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPATK_UP_1 }",
  "magicCoatAffected": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **30**
- Egg species: **6**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_PERISH_SONG — Perish Song

- V1 cost: **4**
- V1 role: `control`
- V1 tags: `perish`, `special_case`
- V1 rules: `standard_attempt`, `delayed_resolution_free`

### Migration differences

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_ALL_BATTLERS"
  }
}
```

### Current mechanics

- Effect: `EFFECT_PERISH_SONG`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_ALL_BATTLERS`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "soundMove": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **16**
- Egg species: **9**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_DETECT — Detect

- V1 cost: **3**
- V1 role: `protection`
- V1 tags: `counterplay`, `priority`, `protect_like`
- V1 rules: `standard_attempt`

### Migration differences

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### Current mechanics

- Effect: `EFFECT_PROTECT`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_FIGHTING`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `4`

Additional effects:

```json
[]
```

Properties:

```json
{
  "argument": "{ .protectMethod = PROTECT_NORMAL }",
  "zMove": "{ .effect = Z_EFFECT_EVSN_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "TRUE",
  "copycatBanned": "TRUE",
  "assistBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **41**
- Egg species: **11**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_SANDSTORM — Sandstorm

- V1 cost: **2**
- V1 role: `field`
- V1 tags: `weather`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`
- `effect_representation_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  },
  "effect": {
    "v1": "EFFECT_SANDSTORM",
    "v2": "EFFECT_WEATHER"
  }
}
```

### Current mechanics

- Effect: `EFFECT_WEATHER`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_ROCK`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPD_UP_1 }",
  "ignoresProtect": "TRUE",
  "windMove": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "argument": "{ .weatherType = BATTLE_WEATHER_SANDSTORM }",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **43**
- Egg species: **0**
- TM: **True**
- HM: **False**
- Explicit FRLG trainer usage: **2**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_ENDURE — Endure

- V1 cost: **2**
- V1 role: `protection`
- V1 tags: `counterplay`, `priority`, `protect_like`
- V1 rules: `standard_attempt`

### Migration differences

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### Current mechanics

- Effect: `EFFECT_ENDURE`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `4`

Additional effects:

```json
[]
```

Properties:

```json
{
  "argument": "{ .protectMethod = PROTECT_NONE }",
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "TRUE",
  "copycatBanned": "TRUE",
  "assistBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **46**
- Egg species: **61**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **2**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_CHARM — Charm

- V1 cost: **3**
- V1 role: `control`
- V1 tags: `stat_drop_offense`
- V1 rules: `standard_attempt`

### Migration differences

- `type_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "TYPE_FAIRY"
  },
  "effect": {
    "v1": "EFFECT_ATTACK_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "attack": "2"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_STAT_CHANGE`
- Power: `0`
- Accuracy: `100`
- Type: `B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
    "attack": "2"
  }
]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_DEF_UP_1 }",
  "magicCoatAffected": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **93**
- Egg species: **25**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_HEAL_BELL — Heal Bell

- V1 cost: **4**
- V1 role: `recovery`
- V1 tags: `recovery_status`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_USER_AND_ALLY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HEAL_BELL`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER_AND_ALLY`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RECOVER_HP }",
  "snatchAffected": "TRUE",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "soundMove": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **5**
- Egg species: **4**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_MOONLIGHT — Moonlight

- V1 cost: **4**
- V1 role: `recovery`
- V1 tags: `recovery_hp`
- V1 rules: `standard_attempt`

### Migration differences

- `type_changed`

```json
{
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "TYPE_FAIRY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_MOONLIGHT`
- Power: `0`
- Accuracy: `0`
- Type: `B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "healingMove": "TRUE",
  "snatchAffected": "TRUE",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **20**
- Egg species: **2**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **4**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_RAIN_DANCE — Rain Dance

- V1 cost: **2**
- V1 role: `field`
- V1 tags: `weather`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`
- `effect_representation_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  },
  "effect": {
    "v1": "EFFECT_RAIN_DANCE",
    "v2": "EFFECT_WEATHER"
  }
}
```

### Current mechanics

- Effect: `EFFECT_WEATHER`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_WATER`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPD_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "argument": "{ .weatherType = BATTLE_WEATHER_RAIN }",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **62**
- Egg species: **0**
- TM: **True**
- HM: **False**
- Explicit FRLG trainer usage: **7**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_SUNNY_DAY — Sunny Day

- V1 cost: **2**
- V1 role: `field`
- V1 tags: `weather`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`
- `effect_representation_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  },
  "effect": {
    "v1": "EFFECT_SUNNY_DAY",
    "v2": "EFFECT_WEATHER"
  }
}
```

### Current mechanics

- Effect: `EFFECT_WEATHER`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_FIRE`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPD_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "argument": "{ .weatherType = BATTLE_WEATHER_SUN }",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **39**
- Egg species: **0**
- TM: **True**
- HM: **False**
- Explicit FRLG trainer usage: **2**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_EXTREME_SPEED — Extreme Speed

- V1 cost: **4**
- V1 role: `damage`
- V1 tags: `direct_damage`, `priority`
- V1 rules: `standard_attempt`

### Migration differences

- `priority_changed`
- `effect_representation_changed`

```json
{
  "priority": {
    "v1": 1,
    "v2": 2
  },
  "effect": {
    "v1": "EFFECT_QUICK_ATTACK",
    "v2": "EFFECT_HIT"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `80`
- Accuracy: `100`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `B_UPDATED_MOVE_DATA >= GEN_5 ? 2 : 1`

Additional effects:

```json
[]
```

Properties:

```json
{
  "makesContact": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **12**
- Egg species: **2**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **5**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_FAKE_OUT — Fake Out

- V1 cost: **2**
- V1 role: `damage`
- V1 tags: `direct_damage`, `flinch`, `priority`
- V1 rules: `standard_attempt`

### Migration differences

- `priority_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "priority": {
    "v1": 1,
    "v2": 3
  },
  "effect": {
    "v1": "EFFECT_FAKE_OUT",
    "v2": "EFFECT_FIRST_TURN_ONLY"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "100"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_FIRST_TURN_ONLY`
- Power: `40`
- Accuracy: `100`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `B_UPDATED_MOVE_DATA >= GEN_5 ? 3 : 1`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_FLINCH",
    "chance": "100"
  }
]
```

Properties:

```json
{
  "makesContact": "B_UPDATED_MOVE_DATA >= GEN_4",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **38**
- Egg species: **27**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **1**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_HAIL — Hail

- V1 cost: **2**
- V1 role: `field`
- V1 tags: `weather`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`
- `effect_representation_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  },
  "effect": {
    "v1": "EFFECT_HAIL",
    "v2": "EFFECT_WEATHER"
  }
}
```

### Current mechanics

- Effect: `EFFECT_WEATHER`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_ICE`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPD_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "argument": "{ .weatherType = (B_PREFERRED_ICE_WEATHER == B_ICE_WEATHER_SNOW) ? BATTLE_WEATHER_SNOW : BATTLE_WEATHER_HAIL }",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **9**
- Egg species: **0**
- TM: **True**
- HM: **False**
- Explicit FRLG trainer usage: **2**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_FOLLOW_ME — Follow Me

- V1 cost: **3**
- V1 role: `support`
- V1 tags: `doubles_support`, `priority`, `team_support`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `priority_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "priority": {
    "v1": 3,
    "v2": 2
  }
}
```

### Current mechanics

- Effect: `EFFECT_FOLLOW_ME`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `B_UPDATED_MOVE_DATA >= GEN_6 ? 2 : 3`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "TRUE",
  "copycatBanned": "TRUE",
  "assistBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **10**
- Egg species: **2**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_NATURE_POWER — Nature Power

- V1 cost: **3**
- V1 role: `utility`
- V1 tags: `move_call`, `random_outcome`, `special_case`
- V1 rules: `standard_attempt`, `called_move_caller_only`

### Migration differences

- `power_changed`
- `target_changed`

```json
{
  "power": {
    "v1": 0,
    "v2": 1,
    "delta": 1
  },
  "target": {
    "v1": "TARGET_DEPENDS",
    "v2": "TARGET_SELECTED"
  }
}
```

### Current mechanics

- Effect: `EFFECT_NATURE_POWER`
- Power: `1`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_FLAGS >= GEN_6 ? TARGET_SELECTED : TARGET_DEPENDS`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "B_UPDATED_MOVE_FLAGS >= GEN_5",
  "copycatBanned": "TRUE",
  "sleepTalkBanned": "TRUE",
  "instructBanned": "TRUE",
  "encoreBanned": "(B_UPDATED_MOVE_FLAGS >= GEN_7 || B_UPDATED_MOVE_FLAGS < GEN_3)",
  "assistBanned": "B_UPDATED_MOVE_FLAGS >= GEN_6",
  "mimicBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **3**
- Egg species: **12**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_HELPING_HAND — Helping Hand

- V1 cost: **2**
- V1 role: `support`
- V1 tags: `doubles_support`, `priority`, `team_support`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_ALLY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HELPING_HAND`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_DATA >= GEN_4 ? TARGET_ALLY : TARGET_USER`
- Priority: `5`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RESET_STATS }",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "metronomeBanned": "TRUE",
  "copycatBanned": "TRUE",
  "assistBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **85**
- Egg species: **20**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_MUD_SPORT — Mud Sport

- V1 cost: **1**
- V1 role: `field`
- V1 tags: `field_modifier`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### Current mechanics

- Effect: `EFFECT_MUD_SPORT`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_GROUND`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPDEF_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "skyBattleBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **0**
- Egg species: **22**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **10**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_AROMATHERAPY — Aromatherapy

- V1 cost: **4**
- V1 role: `recovery`
- V1 tags: `recovery_status`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_USER_AND_ALLY"
  }
}
```

### Current mechanics

- Effect: `EFFECT_HEAL_BELL`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_GRASS`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER_AND_ALLY`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_RECOVER_HP }",
  "snatchAffected": "TRUE",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "B_UPDATED_MOVE_FLAGS < GEN_6",
  "mirrorMoveBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **12**
- Egg species: **8**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **1**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_HOWL — Howl

- V1 cost: **3**
- V1 role: `setup`
- V1 tags: `stat_boost_offense`
- V1 rules: `standard_attempt`

### Migration differences

- `target_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_USER_AND_ALLY"
  },
  "effect": {
    "v1": "EFFECT_ATTACK_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "1"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_STAT_CHANGE`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `B_UPDATED_MOVE_DATA >= GEN_8 ? TARGET_USER_AND_ALLY : TARGET_USER`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
    "attack": "1"
  }
]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_ATK_UP_1 }",
  "snatchAffected": "TRUE",
  "ignoresProtect": "TRUE",
  "ignoresSubstitute": "B_UPDATED_MOVE_FLAGS >= GEN_CHAMPIONS",
  "mirrorMoveBanned": "TRUE",
  "soundMove": "B_UPDATED_MOVE_FLAGS >= GEN_8",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **26**
- Egg species: **11**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

## MOVE_WATER_SPORT — Water Sport

- V1 cost: **1**
- V1 role: `field`
- V1 tags: `field_modifier`
- V1 rules: `standard_attempt`

### Migration differences

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0,
    "delta": -100
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### Current mechanics

- Effect: `EFFECT_WATER_SPORT`
- Power: `0`
- Accuracy: `0`
- Type: `TYPE_WATER`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_FIELD`
- Priority: `0`

Additional effects:

```json
[]
```

Properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPDEF_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "skyBattleBanned": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Gen-9 level-up species: **1**
- Egg species: **14**
- TM: **False**
- HM: **False**
- Explicit FRLG trainer usage: **0**

### Decision

- Approved V2 cost: `—`
- KEEP / CHANGE: `—`
- Reasoning: `—`

---

