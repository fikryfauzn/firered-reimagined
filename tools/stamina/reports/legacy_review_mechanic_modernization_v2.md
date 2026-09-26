# Stamina V2 — Legacy Review Batch 01

## Mechanic Modernization

Moves in batch: **10**

This batch contains legacy moves where modern mechanics changed qualitatively. V1 costs are historical references only.

## MOVE_ACID — Acid

- V1 cost: **2**
- V1 role: `damage`
- V1 tags: `direct_damage`, `spread`, `stat_drop_defense`

### Migration difference

- `damage_category_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "defense": "B_UPDATED_MOVE_DATA < GEN_4 ? 1 : 0",
      "spDef": "B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `40`
- Accuracy: `100`
- Type: `TYPE_POISON`
- Category: `DAMAGE_CATEGORY_SPECIAL`
- Target: `TARGET_BOTH`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_STAT_MINUS",
    "defense": "B_UPDATED_MOVE_DATA < GEN_4 ? 1 : 0",
    "spDef": "B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0",
    "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
  }
]
```

Relevant properties:

```json
{}
```

### Campaign context

- Active Gen-9 level-up species: **30**
- Egg species: **3**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **16**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_GROWTH — Growth

- V1 cost: **3**
- V1 role: `setup`
- V1 tags: `stat_boost_offense`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_ATTACK_UP",
    "v2": "EFFECT_GROWTH"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "B_UPDATED_MOVE_DATA >= GEN_5 ? 1 : 0",
      "spAtk": "1"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_GROWTH`
- Power: `0`
- Accuracy: `0`
- Type: `B_UPDATED_MOVE_TYPES >= GEN_CHAMPIONS ? TYPE_GRASS : TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_USER`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
    "attack": "B_UPDATED_MOVE_DATA >= GEN_5 ? 1 : 0",
    "spAtk": "1"
  }
]
```

Relevant properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPATK_UP_1 }",
  "ignoresProtect": "TRUE",
  "mirrorMoveBanned": "TRUE",
  "snatchAffected": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **71**
- Egg species: **8**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **7**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_STRING_SHOT — String Shot

- V1 cost: **3**
- V1 role: `control`
- V1 tags: `spread`, `stat_drop_speed`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "speed": "B_UPDATED_MOVE_DATA >= GEN_6 ? 2 : 1"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_STAT_CHANGE`
- Power: `0`
- Accuracy: `95`
- Type: `TYPE_BUG`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_BOTH`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
    "speed": "B_UPDATED_MOVE_DATA >= GEN_6 ? 2 : 1"
  }
]
```

Relevant properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_SPD_UP_1 }",
  "magicCoatAffected": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **29**
- Egg species: **1**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **0**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_SWEET_SCENT — Sweet Scent

- V1 cost: **3**
- V1 role: `control`
- V1 tags: `spread`, `stat_drop_evasion`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_EVASION_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "evasion": "(B_UPDATED_MOVE_DATA >= GEN_6) ? 2 : 1"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_STAT_CHANGE`
- Power: `0`
- Accuracy: `100`
- Type: `TYPE_NORMAL`
- Category: `DAMAGE_CATEGORY_STATUS`
- Target: `TARGET_BOTH`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
    "evasion": "(B_UPDATED_MOVE_DATA >= GEN_6) ? 2 : 1"
  }
]
```

Relevant properties:

```json
{
  "zMove": "{ .effect = Z_EFFECT_ACC_UP_1 }",
  "magicCoatAffected": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **58**
- Egg species: **8**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **7**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_CRUNCH — Crunch

- V1 cost: **3**
- V1 role: `damage`
- V1 tags: `direct_damage`, `stat_drop_defense`

### Migration difference

- `damage_category_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "defense": "B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0",
      "spDef": "B_UPDATED_MOVE_DATA < GEN_4 ? 1 : 0",
      "chance": "20"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `80`
- Accuracy: `100`
- Type: `TYPE_DARK`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_STAT_MINUS",
    "defense": "B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0",
    "spDef": "B_UPDATED_MOVE_DATA < GEN_4 ? 1 : 0",
    "chance": "20"
  }
]
```

Relevant properties:

```json
{
  "makesContact": "TRUE",
  "bitingMove": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **161**
- Egg species: **12**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **10**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_NEEDLE_ARM — Needle Arm

- V1 cost: **3**
- V1 role: `damage`
- V1 tags: `direct_damage`, `flinch`

### Migration difference

- `damage_category_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "effect": {
    "v1": "EFFECT_FLINCH_MINIMIZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "30"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `60`
- Accuracy: `100`
- Type: `TYPE_GRASS`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_FLINCH",
    "chance": "30"
  }
]
```

Relevant properties:

```json
{
  "makesContact": "TRUE",
  "minimizeDoubleDamage": "B_UPDATED_MOVE_FLAGS < GEN_4",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **0**
- Egg species: **0**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **0**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_POISON_FANG — Poison Fang

- V1 cost: **3**
- V1 role: `damage`
- V1 tags: `direct_damage`, `status_poison`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_FANG",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_TOXIC",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_6 ? 50 : 30"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `50`
- Accuracy: `100`
- Type: `TYPE_POISON`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_TOXIC",
    "chance": "B_UPDATED_MOVE_DATA >= GEN_6 ? 50 : 30"
  }
]
```

Relevant properties:

```json
{
  "makesContact": "TRUE",
  "bitingMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **18**
- Egg species: **5**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **1**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_ASTONISH — Astonish

- V1 cost: **2**
- V1 role: `damage`
- V1 tags: `direct_damage`, `flinch`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_MINIMIZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "30"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `30`
- Accuracy: `100`
- Type: `TYPE_GHOST`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_FLINCH",
    "chance": "30"
  }
]
```

Relevant properties:

```json
{
  "makesContact": "TRUE",
  "minimizeDoubleDamage": "B_UPDATED_MOVE_FLAGS < GEN_4",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **117**
- Egg species: **19**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **3**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_EXTRASENSORY — Extrasensory

- V1 cost: **3**
- V1 role: `damage`
- V1 tags: `direct_damage`, `flinch`

### Migration difference

- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_MINIMIZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "10"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_HIT`
- Power: `80`
- Accuracy: `100`
- Type: `TYPE_PSYCHIC`
- Category: `DAMAGE_CATEGORY_SPECIAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_FLINCH",
    "chance": "10"
  }
]
```

Relevant properties:

```json
{
  "minimizeDoubleDamage": "B_UPDATED_MOVE_FLAGS < GEN_4",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **33**
- Egg species: **13**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **0**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

## MOVE_VOLT_TACKLE — Volt Tackle

- V1 cost: **4**
- V1 role: `damage`
- V1 tags: `direct_damage`, `recoil`

### Migration difference

- `damage_category_changed`
- `effect_representation_changed`
- `v2_additional_effects`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "effect": {
    "v1": "EFFECT_DOUBLE_EDGE",
    "v2": "EFFECT_RECOIL"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "10"
    }
  ]
}
```

### Current mechanics

- Effect: `EFFECT_RECOIL`
- Power: `120`
- Accuracy: `100`
- Type: `TYPE_ELECTRIC`
- Category: `DAMAGE_CATEGORY_PHYSICAL`
- Target: `TARGET_SELECTED`
- Priority: `0`

Additional effects:

```json
[
  {
    "moveEffect": "MOVE_EFFECT_PARALYSIS",
    "chance": "10"
  }
]
```

Relevant properties:

```json
{
  "argument": "{ .recoilPercentage = 33 }",
  "makesContact": "TRUE",
  "validApprenticeMove": "TRUE"
}
```

### Campaign context

- Active Gen-9 level-up species: **0**
- Egg species: **0**
- Current TM: **False**
- Current HM: **False**
- Explicit FRLG trainer usage: **0**

### Human decision

- Decision: `PENDING`
- Approved V2 cost: `—`
- Reasoning: `—`

---

