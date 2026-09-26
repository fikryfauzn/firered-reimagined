# Stamina V2 — Legacy Mechanical Diff

## Summary

- Legacy safe: **68**
- Legacy re-audit: **287**
- New moves: **493**
- Total normal move records: **848**

## Re-audit reason counts

- `effect_changed`: **200**
- `v2_additional_effects_present`: **149**
- `damage_category_changed`: **53**
- `power_is_config_dependent`: **53**
- `accuracy_is_config_dependent`: **36**
- `accuracy_changed`: **31**
- `target_changed`: **17**
- `type_changed`: **9**
- `power_changed`: **8**
- `priority_is_config_dependent`: **5**
- `missing_from_v2`: **4**
- `priority_changed`: **3**

## Legacy moves requiring re-audit

### MOVE_KARATE_CHOP — old cost 2

- `effect_changed`
- `type_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "type": {
    "v1": "TYPE_FIGHTING",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_2 ? TYPE_FIGHTING : TYPE_NORMAL"
  }
}
```

### MOVE_DOUBLE_SLAP — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_COMET_PUNCH — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_PAY_DAY — old cost 1

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PAY_DAY",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PAYDAY"
    }
  ]
}
```

### MOVE_FIRE_PUNCH — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BURN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_ICE_PUNCH — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FREEZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FREEZE_OR_FROSTBITE",
      "chance": "10"
    }
  ]
}
```

### MOVE_THUNDER_PUNCH — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "10"
    }
  ]
}
```

### MOVE_VICE_GRIP — old cost 2

- `missing_from_v2`

### MOVE_RAZOR_WIND — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_RAZOR_WIND",
    "v2": "EFFECT_TWO_TURNS_ATTACK"
  },
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_3 ? 100 : 75"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_SWORDS_DANCE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "2"
    }
  ]
}
```

### MOVE_GUST — old cost 1

- `effect_changed`
- `type_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_GUST",
    "v2": "EFFECT_HIT"
  },
  "type": {
    "v1": "TYPE_FLYING",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_2 ? TYPE_FLYING : TYPE_NORMAL"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_WING_ATTACK — old cost 2

- `power_is_config_dependent`

```json
{
  "power": {
    "v1": 60,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 60 : 35"
  }
}
```

### MOVE_WHIRLWIND — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_FLY — old cost 3

- `power_is_config_dependent`

```json
{
  "power": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 90 : 70"
  }
}
```

### MOVE_BIND — old cost 2

- `effect_changed`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "accuracy": {
    "v1": 75,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 85 : 75"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_BIND"
    }
  ]
}
```

### MOVE_VINE_WHIP — old cost 1

- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 35,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 45 : 35"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_STOMP — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_DOUBLE_KICK — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_DOUBLE_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_JUMP_KICK — old cost 2

- `power_changed`

```json
{
  "power": {
    "v1": 70,
    "v2": 100
  }
}
```

### MOVE_ROLLING_KICK — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
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

### MOVE_SAND_ATTACK — old cost 3

- `effect_changed`
- `type_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "type": {
    "v1": "TYPE_GROUND",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_2 ? TYPE_GROUND : TYPE_NORMAL"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "accuracy": "1"
    }
  ]
}
```

### MOVE_HEADBUTT — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
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

### MOVE_FURY_ATTACK — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_TACKLE — old cost 1

- `power_changed`
- `accuracy_is_config_dependent`

```json
{
  "power": {
    "v1": 35,
    "v2": 40
  },
  "accuracy": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 95"
  }
}
```

### MOVE_BODY_SLAM — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "30"
    }
  ]
}
```

### MOVE_WRAP — old cost 2

- `effect_changed`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 90 : 85"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_WRAP"
    }
  ]
}
```

### MOVE_THRASH — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RAMPAGE",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 120 : 90"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_THRASH",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_DOUBLE_EDGE — old cost 4

- `effect_changed`
- `power_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_DOUBLE_EDGE",
    "v2": "EFFECT_RECOIL"
  },
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 120 : 100"
  }
}
```

### MOVE_TAIL_WHIP — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "defense": "1"
    }
  ]
}
```

### MOVE_POISON_STING — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 30 : 20"
    }
  ]
}
```

### MOVE_TWINEEDLE — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TWINEEDLE",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "20"
    }
  ]
}
```

### MOVE_PIN_MISSILE — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 14,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 25 : 14"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 95 : 85"
  }
}
```

### MOVE_LEER — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "defense": "1"
    }
  ]
}
```

### MOVE_BITE — old cost 3

- `effect_changed`
- `type_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
    "v2": "EFFECT_HIT"
  },
  "type": {
    "v1": "TYPE_DARK",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_2 ? TYPE_DARK : TYPE_NORMAL"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 30 : 10"
    }
  ]
}
```

### MOVE_GROWL — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "attack": "1"
    }
  ]
}
```

### MOVE_ROAR — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 0 : 100"
  }
}
```

### MOVE_SING — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_SONIC_BOOM — old cost 2

- `effect_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SONICBOOM",
    "v2": "EFFECT_FIXED_HP_DAMAGE"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_DISABLE — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 55,
    "v2": 100
  }
}
```

### MOVE_ACID — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
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

### MOVE_EMBER — old cost 1

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BURN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_FLAMETHROWER — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BURN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_HYDRO_PUMP — old cost 4

- `power_is_config_dependent`

```json
{
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 110 : 120"
  }
}
```

### MOVE_SURF — old cost 4

- `power_is_config_dependent`
- `target_changed`

```json
{
  "power": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95"
  },
  "target": {
    "v1": "TARGET_BOTH",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_4 ? TARGET_FOES_AND_ALLY : TARGET_BOTH"
  }
}
```

### MOVE_ICE_BEAM — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FREEZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FREEZE_OR_FROSTBITE",
      "chance": "10"
    }
  ]
}
```

### MOVE_BLIZZARD — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FREEZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 110 : 120"
  },
  "accuracy": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 70 : 90"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FREEZE_OR_FROSTBITE",
      "chance": "10"
    }
  ]
}
```

### MOVE_PSYBEAM — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "10"
    }
  ]
}
```

### MOVE_BUBBLE_BEAM — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### MOVE_AURORA_BEAM — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "attack": "1",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### MOVE_HYPER_BEAM — old cost 5

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RECHARGE",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RECHARGE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_LOW_KICK — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_LOW_KICK",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_3 ? EFFECT_LOW_KICK : EFFECT_HIT"
  },
  "power": {
    "v1": 1,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_3 ? 1 : 50"
  },
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_3 ? 100 : 90"
  }
}
```

### MOVE_COUNTER — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_COUNTER",
    "v2": "EFFECT_REFLECT_DAMAGE"
  }
}
```

### MOVE_ABSORB — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ABSORB",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_ABSORB",
      "absorbPercentage": "50"
    }
  ]
}
```

### MOVE_MEGA_DRAIN — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ABSORB",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_ABSORB",
      "absorbPercentage": "50"
    }
  ]
}
```

### MOVE_GROWTH — old cost 3

- `effect_changed`
- `type_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_ATTACK_UP",
    "v2": "EFFECT_GROWTH"
  },
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_CHAMPIONS ? TYPE_GRASS : TYPE_NORMAL"
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

### MOVE_RAZOR_LEAF — old cost 3

- `effect_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_POISON_POWDER — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_POISON",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_STUN_SPORE — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_SLEEP_POWDER — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_PETAL_DANCE — old cost 5

- `effect_changed`
- `power_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RAMPAGE",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 70,
    "v2": 120
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_THRASH",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_STRING_SHOT — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_DRAGON_RAGE — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_DRAGON_RAGE",
    "v2": "EFFECT_FIXED_HP_DAMAGE"
  }
}
```

### MOVE_FIRE_SPIN — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 15,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 35 : 15"
  },
  "accuracy": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 85 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_FIRE_SPIN"
    }
  ]
}
```

### MOVE_THUNDER_SHOCK — old cost 1

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "10"
    }
  ]
}
```

### MOVE_THUNDERBOLT — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "10"
    }
  ]
}
```

### MOVE_THUNDER_WAVE — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  },
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_7 ? 90 : 100"
  }
}
```

### MOVE_THUNDER — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_THUNDER",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 110 : 120"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 30 : 10"
    }
  ]
}
```

### MOVE_ROCK_THROW — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 90 : 65"
  }
}
```

### MOVE_DIG — old cost 3

- `power_changed`

```json
{
  "power": {
    "v1": 60,
    "v2": 80
  }
}
```

### MOVE_TOXIC — old cost 4

- `effect_changed`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_TOXIC",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 90 : 85"
  }
}
```

### MOVE_CONFUSION — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "10"
    }
  ]
}
```

### MOVE_PSYCHIC — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spDef": "1",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### MOVE_HYPNOSIS — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_MEDITATE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
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

### MOVE_AGILITY — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "speed": "2"
    }
  ]
}
```

### MOVE_QUICK_ATTACK — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_QUICK_ATTACK",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_RAGE — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RAGE",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RAGE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_TELEPORT — old cost 1

- `priority_is_config_dependent`

```json
{
  "priority": {
    "v1": 0,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_8 ? -6 : 0"
  }
}
```

### MOVE_NIGHT_SHADE — old cost 3

- `damage_category_changed`

```json
{
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_MIMIC — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_3 ? 0 : 100"
  }
}
```

### MOVE_SCREECH — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "defense": "2"
    }
  ]
}
```

### MOVE_DOUBLE_TEAM — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_EVASION_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "evasion": "1"
    }
  ]
}
```

### MOVE_HARDEN — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "1"
    }
  ]
}
```

### MOVE_MINIMIZE — old cost 4

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "evasion": "(B_MINIMIZE_EVASION >= GEN_5) ? 2 : 1"
    }
  ]
}
```

### MOVE_SMOKESCREEN — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "accuracy": "1"
    }
  ]
}
```

### MOVE_WITHDRAW — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "1"
    }
  ]
}
```

### MOVE_DEFENSE_CURL — old cost 3

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "1"
    }
  ]
}
```

### MOVE_BARRIER — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "2"
    }
  ]
}
```

### MOVE_HAZE — old cost 2

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_BIDE — old cost 3

- `accuracy_is_config_dependent`
- `priority_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "(B_UPDATED_MOVE_DATA >= GEN_4 || B_UPDATED_MOVE_DATA == GEN_1) ? 0 : 100"
  },
  "priority": {
    "v1": 0,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 1 : 0"
  }
}
```

### MOVE_SELF_DESTRUCT — old cost 5

- `effect_changed`
- `power_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_EXPLOSION",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 200,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 200 : 130"
  }
}
```

### MOVE_LICK — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 30 : 20"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "30"
    }
  ]
}
```

### MOVE_SMOG — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 30 : 20"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "40"
    }
  ]
}
```

### MOVE_SLUDGE — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 30 : 40"
    }
  ]
}
```

### MOVE_BONE_CLUB — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
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

### MOVE_FIRE_BLAST — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BURN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 110 : 120"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 30"
    }
  ]
}
```

### MOVE_WATERFALL — old cost 3

- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "20"
    }
  ]
}
```

### MOVE_CLAMP — old cost 2

- `effect_changed`
- `accuracy_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "accuracy": {
    "v1": 75,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 85 : 75"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_CLAMP"
    }
  ]
}
```

### MOVE_SWIFT — old cost 4

- `effect_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ALWAYS_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_SKULL_BASH — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SKULL_BASH",
    "v2": "EFFECT_TWO_TURNS_ATTACK"
  },
  "power": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 130 : 100"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "defense": "1",
      "self": "TRUE",
      "onChargeTurnOnly": "TRUE"
    }
  ]
}
```

### MOVE_SPIKE_CANNON — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_CONSTRICT — old cost 1

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### MOVE_AMNESIA — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "spDef": "2"
    }
  ]
}
```

### MOVE_KINESIS — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "accuracy": "1"
    }
  ]
}
```

### MOVE_SOFT_BOILED — old cost 4

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_HI_JUMP_KICK — old cost 3

- `missing_from_v2`

### MOVE_GLARE — old cost 3

- `effect_changed`
- `accuracy_changed`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  },
  "accuracy": {
    "v1": 75,
    "v2": 100
  }
}
```

### MOVE_DREAM_EATER — old cost 4

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_ABSORB",
      "absorbPercentage": "50"
    }
  ]
}
```

### MOVE_POISON_GAS — old cost 2

- `effect_changed`
- `accuracy_changed`
- `target_changed`

```json
{
  "effect": {
    "v1": "EFFECT_POISON",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  },
  "accuracy": {
    "v1": 55,
    "v2": 90
  },
  "target": {
    "v1": "TARGET_SELECTED",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_5 ? TARGET_BOTH : TARGET_SELECTED"
  }
}
```

### MOVE_BARRAGE — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_LEECH_LIFE — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ABSORB",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_7 ? 80 : 20"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_ABSORB",
      "absorbPercentage": "50"
    }
  ]
}
```

### MOVE_LOVELY_KISS — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_SKY_ATTACK — old cost 5

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SKY_ATTACK",
    "v2": "EFFECT_TWO_TURNS_ATTACK"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "30"
    }
  ]
}
```

### MOVE_BUBBLE — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 40 : 20"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "B_UPDATED_MOVE_DATA >= GEN_2 ? 10 : 33"
    }
  ]
}
```

### MOVE_DIZZY_PUNCH — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "20"
    }
  ]
}
```

### MOVE_SPORE — old cost 5

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_FLASH — old cost 2

- `effect_changed`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "accuracy": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 100 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "accuracy": "1"
    }
  ]
}
```

### MOVE_PSYWAVE — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 80,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 100 : 80"
  }
}
```

### MOVE_SPLASH — old cost 1

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SPLASH",
    "v2": "EFFECT_DO_NOTHING"
  }
}
```

### MOVE_ACID_ARMOR — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "2"
    }
  ]
}
```

### MOVE_CRABHAMMER — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 100 : 90"
  },
  "accuracy": {
    "v1": 85,
    "v2": 95
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_EXPLOSION — old cost 5

- `effect_changed`
- `power_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_EXPLOSION",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 250,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_2 ? 250 : 170"
  }
}
```

### MOVE_FURY_SWIPES — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_BONEMERANG — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_DOUBLE_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_ROCK_SLIDE — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
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

### MOVE_HYPER_FANG — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_HIT",
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

### MOVE_SHARPEN — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
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

### MOVE_TRI_ATTACK — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRI_ATTACK",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RANDOM_FROM_LIST",
      "chance": "20",
      "randomMoveEffects": "{ MOVE_EFFECT_BURN, MOVE_EFFECT_PARALYSIS, MOVE_EFFECT_FREEZE_OR_FROSTBITE }"
    }
  ]
}
```

### MOVE_SUPER_FANG — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SUPER_FANG",
    "v2": "EFFECT_FIXED_PERCENT_DAMAGE"
  }
}
```

### MOVE_SLASH — old cost 3

- `effect_changed`
- `power_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA == GEN_CHAMPIONS ? 80 : 70"
  }
}
```

### MOVE_THIEF — old cost 1

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_THIEF",
    "v2": "EFFECT_STEAL_ITEM"
  },
  "power": {
    "v1": 40,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 60 : 40"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_SPIDER_WEB — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_MIND_READER — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 0 : 100"
  }
}
```

### MOVE_NIGHTMARE — old cost 3

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 100 : 0"
  }
}
```

### MOVE_FLAME_WHEEL — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_THAW_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_SNORE — old cost 1

- `power_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "power": {
    "v1": 40,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 50 : 40"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "30"
    }
  ]
}
```

### MOVE_CURSE — old cost 3

- `type_changed`
- `v2_additional_effects_present`

```json
{
  "type": {
    "v1": "TYPE_MYSTERY",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_5 ? TYPE_GHOST : TYPE_MYSTERY"
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

### MOVE_CONVERSION_2 — old cost 1

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_5 ? TARGET_SELECTED : TARGET_USER"
  }
}
```

### MOVE_AEROBLAST — old cost 4

- `effect_changed`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_COTTON_SPORE — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`
- `target_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 85"
  },
  "target": {
    "v1": "TARGET_SELECTED",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_6 ? TARGET_BOTH : TARGET_SELECTED"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "speed": "2"
    }
  ]
}
```

### MOVE_POWDER_SNOW — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FREEZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FREEZE_OR_FROSTBITE",
      "chance": "10"
    }
  ]
}
```

### MOVE_PROTECT — old cost 3

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### MOVE_MACH_PUNCH — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_QUICK_ATTACK",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_SCARY_FACE — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "accuracy": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 90"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "speed": "2"
    }
  ]
}
```

### MOVE_FAINT_ATTACK — old cost 3

- `missing_from_v2`

### MOVE_SWEET_KISS — old cost 3

- `type_changed`

```json
{
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL"
  }
}
```

### MOVE_BELLY_DRUM — old cost 4

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "STAT_CHANGE_FORCE_MAX"
    }
  ]
}
```

### MOVE_SLUDGE_BOMB — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "30"
    }
  ]
}
```

### MOVE_MUD_SLAP — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "accuracy": "1",
      "chance": "100"
    }
  ]
}
```

### MOVE_OCTAZOOKA — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "accuracy": "1",
      "chance": "50"
    }
  ]
}
```

### MOVE_ZAP_CANNON — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 120 : 100"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "100"
    }
  ]
}
```

### MOVE_FORESIGHT — old cost 1

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 0 : 100"
  }
}
```

### MOVE_PERISH_SONG — old cost 4

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_ALL_BATTLERS"
  }
}
```

### MOVE_ICY_WIND — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "100"
    }
  ]
}
```

### MOVE_DETECT — old cost 3

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### MOVE_BONE_RUSH — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 25,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_CHAMPIONS ? 30 : 25"
  },
  "accuracy": {
    "v1": 80,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 90 : 80"
  }
}
```

### MOVE_LOCK_ON — old cost 2

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 0 : 100"
  }
}
```

### MOVE_OUTRAGE — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RAMPAGE",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 120 : 90"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_THRASH",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_SANDSTORM — old cost 2

- `effect_changed`
- `target_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SANDSTORM",
    "v2": "EFFECT_WEATHER"
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_GIGA_DRAIN — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ABSORB",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 60,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 75 : 60"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_ABSORB",
      "absorbPercentage": "50"
    }
  ]
}
```

### MOVE_ENDURE — old cost 2

- `priority_changed`

```json
{
  "priority": {
    "v1": 3,
    "v2": 4
  }
}
```

### MOVE_CHARM — old cost 3

- `effect_changed`
- `type_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "attack": "2"
    }
  ]
}
```

### MOVE_SWAGGER — old cost 2

- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "accuracy": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_7 ? 85 : 90"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "2"
    }
  ]
}
```

### MOVE_SPARK — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "30"
    }
  ]
}
```

### MOVE_FURY_CUTTER — old cost 2

- `power_changed`

```json
{
  "power": {
    "v1": 10,
    "v2": 40
  }
}
```

### MOVE_STEEL_WING — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "defense": "1",
      "self": "TRUE",
      "chance": "10"
    }
  ]
}
```

### MOVE_MEAN_LOOK — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_HEAL_BELL — old cost 4

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_USER_AND_ALLY"
  }
}
```

### MOVE_PAIN_SPLIT — old cost 3

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_3 ? 0 : 100"
  }
}
```

### MOVE_SACRED_FIRE — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_THAW_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "50"
    }
  ]
}
```

### MOVE_DYNAMIC_PUNCH — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "100"
    }
  ]
}
```

### MOVE_DRAGON_BREATH — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_PARALYZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "30"
    }
  ]
}
```

### MOVE_PURSUIT — old cost 1

- `damage_category_changed`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_RAPID_SPIN — old cost 1

- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_8 ? 50 : 20"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "speed": "1",
      "self": "TRUE",
      "chance": "100"
    }
  ]
}
```

### MOVE_SWEET_SCENT — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_IRON_TAIL — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "defense": "1",
      "chance": "30"
    }
  ]
}
```

### MOVE_METAL_CLAW — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_UP_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "attack": "1",
      "self": "TRUE",
      "chance": "10"
    }
  ]
}
```

### MOVE_VITAL_THROW — old cost 4

- `effect_changed`
- `accuracy_changed`

```json
{
  "effect": {
    "v1": "EFFECT_VITAL_THROW",
    "v2": "EFFECT_HIT"
  },
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_MOONLIGHT — old cost 4

- `type_changed`

```json
{
  "type": {
    "v1": "TYPE_NORMAL",
    "v2": "B_UPDATED_MOVE_TYPES >= GEN_6 ? TYPE_FAIRY : TYPE_NORMAL"
  }
}
```

### MOVE_HIDDEN_POWER — old cost 3

- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 1,
    "v2_expr": "B_HIDDEN_POWER_DMG >= GEN_6 ? 60 : 1"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_CROSS_CHOP — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_TWISTER — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TWISTER",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "20"
    }
  ]
}
```

### MOVE_RAIN_DANCE — old cost 2

- `effect_changed`
- `target_changed`

```json
{
  "effect": {
    "v1": "EFFECT_RAIN_DANCE",
    "v2": "EFFECT_WEATHER"
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_SUNNY_DAY — old cost 2

- `effect_changed`
- `target_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SUNNY_DAY",
    "v2": "EFFECT_WEATHER"
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_CRUNCH — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
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

### MOVE_MIRROR_COAT — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MIRROR_COAT",
    "v2": "EFFECT_REFLECT_DAMAGE"
  }
}
```

### MOVE_EXTREME_SPEED — old cost 4

- `effect_changed`
- `priority_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_QUICK_ATTACK",
    "v2": "EFFECT_HIT"
  },
  "priority": {
    "v1": 1,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 2 : 1"
  }
}
```

### MOVE_ANCIENT_POWER — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ALL_STATS_UP_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "attack": "1",
      "defense": "1",
      "spDef": "1",
      "spAtk": "1",
      "speed": "1",
      "self": "TRUE",
      "chance": "10"
    }
  ]
}
```

### MOVE_SHADOW_BALL — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spDef": "1",
      "chance": "20"
    }
  ]
}
```

### MOVE_FUTURE_SIGHT — old cost 4

- `power_changed`
- `accuracy_is_config_dependent`

```json
{
  "power": {
    "v1": 80,
    "v2": 120
  },
  "accuracy": {
    "v1": 90,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 90"
  }
}
```

### MOVE_ROCK_SMASH — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 40 : 20"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "defense": "1",
      "chance": "50"
    }
  ]
}
```

### MOVE_WHIRLPOOL — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 15,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 35 : 15"
  },
  "accuracy": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 85 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_WHIRLPOOL"
    }
  ]
}
```

### MOVE_BEAT_UP — old cost 3

- `power_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "power": {
    "v1": 10,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 1 : 10"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BEAT_UP_MESSAGE",
      "preAttackEffect": "TRUE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_FAKE_OUT — old cost 2

- `effect_changed`
- `priority_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FAKE_OUT",
    "v2": "EFFECT_FIRST_TURN_ONLY"
  },
  "priority": {
    "v1": 1,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 3 : 1"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "100"
    }
  ]
}
```

### MOVE_UPROAR — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_UPROAR",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 50,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 90 : 50"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_UPROAR",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_STOCKPILE — old cost 2

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "1",
      "spDef": "1"
    }
  ]
}
```

### MOVE_SPIT_UP — old cost 4

- `power_changed`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 100,
    "v2": 1
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_HEAT_WAVE — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BURN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 95 : 100"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_HAIL — old cost 2

- `effect_changed`
- `target_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HAIL",
    "v2": "EFFECT_WEATHER"
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_FLATTER — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLATTER",
    "v2": "EFFECT_SWAGGER"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "spAtk": "1"
    }
  ]
}
```

### MOVE_WILL_O_WISP — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_WILL_O_WISP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  },
  "accuracy": {
    "v1": 75,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 85 : 75"
  }
}
```

### MOVE_MEMENTO — old cost 3

- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 100 : 0"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "attack": "2",
      "spAtk": "2"
    }
  ]
}
```

### MOVE_SMELLING_SALT — old cost 2

- `missing_from_v2`

### MOVE_FOLLOW_ME — old cost 3

- `accuracy_changed`
- `priority_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "priority": {
    "v1": 3,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 2 : 3"
  }
}
```

### MOVE_NATURE_POWER — old cost 3

- `power_changed`
- `target_changed`

```json
{
  "power": {
    "v1": 0,
    "v2": 1
  },
  "target": {
    "v1": "TARGET_DEPENDS",
    "v2": "B_UPDATED_MOVE_FLAGS >= GEN_6 ? TARGET_SELECTED : TARGET_DEPENDS"
  }
}
```

### MOVE_CHARGE — old cost 2

- `accuracy_changed`
- `v2_additional_effects_present`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "spDef": "1"
    }
  ]
}
```

### MOVE_HELPING_HAND — old cost 2

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_4 ? TARGET_ALLY : TARGET_USER"
  }
}
```

### MOVE_ROLE_PLAY — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_WISH — old cost 3

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_ASSIST — old cost 3

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_INGRAIN — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_SUPERPOWER — old cost 4

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SUPERPOWER",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "attack": "1",
      "defense": "1",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_MAGIC_COAT — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_RECYCLE — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_BRICK_BREAK — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BRICK_BREAK",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BREAK_SCREEN",
      "preAttackEffect": "TRUE"
    }
  ]
}
```

### MOVE_YAWN — old cost 3

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_KNOCK_OFF — old cost 1

- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 20,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 65 : 20"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_ERUPTION — old cost 6

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ERUPTION",
    "v2": "EFFECT_POWER_BASED_ON_USER_HP"
  }
}
```

### MOVE_SKILL_SWAP — old cost 3

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_IMPRISON — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_REFRESH — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_GRUDGE — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_SNATCH — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_SECRET_POWER — old cost 3

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "sheerForceOverride": "TRUE"
    }
  ]
}
```

### MOVE_DIVE — old cost 3

- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 60,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 80 : 60"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_ARM_THRUST — old cost 2

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_CAMOUFLAGE — old cost 1

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_TAIL_GLOW — old cost 3

- `effect_changed`
- `accuracy_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_ATTACK_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "spAtk": "B_UPDATED_MOVE_DATA >= GEN_5 ? 3 : 2"
    }
  ]
}
```

### MOVE_LUSTER_PURGE — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 70,
    "v2_expr": "(B_UPDATED_MOVE_DATA >= GEN_9) ? 95 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spDef": "1",
      "chance": "50"
    }
  ]
}
```

### MOVE_MIST_BALL — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_ATTACK_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 70,
    "v2_expr": "(B_UPDATED_MOVE_DATA >= GEN_9) ? 95 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spAtk": "1",
      "chance": "50"
    }
  ]
}
```

### MOVE_FEATHER_DANCE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
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

### MOVE_TEETER_DANCE — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_TEETER_DANCE",
    "v2": "EFFECT_CONFUSE"
  }
}
```

### MOVE_BLAZE_KICK — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BLAZE_KICK",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_BURN",
      "chance": "10"
    }
  ]
}
```

### MOVE_MUD_SPORT — old cost 1

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_ICE_BALL — old cost 5

- `damage_category_changed`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_NEEDLE_ARM — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_FLINCH_MINIMIZE_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_FLINCH",
      "chance": "30"
    }
  ]
}
```

### MOVE_SLACK_OFF — old cost 4

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_HYPER_VOICE — old cost 5

- `damage_category_changed`

```json
{
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_POISON_FANG — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_CRUSH_CLAW — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "defense": "1",
      "chance": "50"
    }
  ]
}
```

### MOVE_BLAST_BURN — old cost 5

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RECHARGE",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RECHARGE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_HYDRO_CANNON — old cost 5

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RECHARGE",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RECHARGE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_METEOR_MASH — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_UP_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 100"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 85"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "attack": "1",
      "self": "TRUE",
      "chance": "20"
    }
  ]
}
```

### MOVE_ASTONISH — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_WEATHER_BALL — old cost 3

- `damage_category_changed`

```json
{
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_AROMATHERAPY — old cost 4

- `target_changed`

```json
{
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_USER_AND_ALLY"
  }
}
```

### MOVE_FAKE_TEARS — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "spDef": "2"
    }
  ]
}
```

### MOVE_AIR_CUTTER — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 55,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 60 : 55"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_OVERHEAT — old cost 4

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_OVERHEAT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 140,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 130 : 140"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spAtk": "2",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_ODOR_SLEUTH — old cost 1

- `accuracy_is_config_dependent`

```json
{
  "accuracy": {
    "v1": 100,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 0 : 100"
  }
}
```

### MOVE_ROCK_TOMB — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 50,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 60 : 50"
  },
  "accuracy": {
    "v1": 80,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 95 : 80"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "100"
    }
  ]
}
```

### MOVE_SILVER_WIND — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ALL_STATS_UP_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_PLUS",
      "attack": "1",
      "defense": "1",
      "spDef": "1",
      "spAtk": "1",
      "speed": "1",
      "self": "TRUE",
      "chance": "10"
    }
  ]
}
```

### MOVE_METAL_SOUND — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPECIAL_DEFENSE_DOWN_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "spDef": "2"
    }
  ]
}
```

### MOVE_GRASS_WHISTLE — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SLEEP",
    "v2": "EFFECT_NON_VOLATILE_STATUS"
  }
}
```

### MOVE_TICKLE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TICKLE",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
      "attack": "1",
      "defense": "1"
    }
  ]
}
```

### MOVE_COSMIC_POWER — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_COSMIC_POWER",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "1",
      "spDef": "1"
    }
  ]
}
```

### MOVE_WATER_SPOUT — old cost 6

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ERUPTION",
    "v2": "EFFECT_POWER_BASED_ON_USER_HP"
  }
}
```

### MOVE_SIGNAL_BEAM — old cost 3

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "10"
    }
  ]
}
```

### MOVE_SHADOW_PUNCH — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ALWAYS_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_EXTRASENSORY — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

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

### MOVE_SKY_UPPERCUT — old cost 4

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_SKY_UPPERCUT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_SAND_TOMB — old cost 2

- `effect_changed`
- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_TRAP",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 15,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 35 : 15"
  },
  "accuracy": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 85 : 70"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_WRAP",
      "wrapped": "B_MSG_WRAPPED_SAND_TOMB"
    }
  ]
}
```

### MOVE_MUDDY_WATER — old cost 5

- `effect_changed`
- `power_is_config_dependent`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ACCURACY_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 95,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_6 ? 90 : 95"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "accuracy": "1",
      "chance": "30"
    }
  ]
}
```

### MOVE_BULLET_SEED — old cost 1

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 10,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 25 : 10"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_AERIAL_ACE — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ALWAYS_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_ICICLE_SPEAR — old cost 1

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 10,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 25 : 10"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_IRON_DEFENSE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DEFENSE_UP_2",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "defense": "2"
    }
  ]
}
```

### MOVE_BLOCK — old cost 2

- `accuracy_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  }
}
```

### MOVE_HOWL — old cost 3

- `effect_changed`
- `target_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_ATTACK_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "B_UPDATED_MOVE_DATA >= GEN_8 ? TARGET_USER_AND_ALLY : TARGET_USER"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "1"
    }
  ]
}
```

### MOVE_DRAGON_CLAW — old cost 3

- `damage_category_changed`

```json
{
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_FRENZY_PLANT — old cost 5

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_RECHARGE",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_RECHARGE",
      "self": "TRUE"
    }
  ]
}
```

### MOVE_BULK_UP — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_BULK_UP",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "1",
      "defense": "1"
    }
  ]
}
```

### MOVE_BOUNCE — old cost 4

- `v2_additional_effects_present`

```json
{
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "30"
    }
  ]
}
```

### MOVE_MUD_SHOT — old cost 2

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_SPEED_DOWN_HIT",
    "v2": "EFFECT_HIT"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "speed": "1",
      "chance": "100"
    }
  ]
}
```

### MOVE_POISON_TAIL — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_POISON_TAIL",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_POISON",
      "chance": "10"
    }
  ]
}
```

### MOVE_COVET — old cost 1

- `effect_changed`
- `power_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_THIEF",
    "v2": "EFFECT_STEAL_ITEM"
  },
  "power": {
    "v1": 40,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 60 : 40"
  }
}
```

### MOVE_VOLT_TACKLE — old cost 4

- `effect_changed`
- `damage_category_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DOUBLE_EDGE",
    "v2": "EFFECT_RECOIL"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_PARALYSIS",
      "chance": "10"
    }
  ]
}
```

### MOVE_MAGICAL_LEAF — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ALWAYS_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_WATER_SPORT — old cost 1

- `accuracy_changed`
- `target_changed`

```json
{
  "accuracy": {
    "v1": 100,
    "v2": 0
  },
  "target": {
    "v1": "TARGET_USER",
    "v2": "TARGET_FIELD"
  }
}
```

### MOVE_CALM_MIND — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CALM_MIND",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "spAtk": "1",
      "spDef": "1"
    }
  ]
}
```

### MOVE_LEAF_BLADE — old cost 3

- `effect_changed`
- `power_is_config_dependent`
- `damage_category_changed`

```json
{
  "effect": {
    "v1": "EFFECT_HIGH_CRITICAL",
    "v2": "EFFECT_HIT"
  },
  "power": {
    "v1": 70,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_4 ? 90 : 70"
  },
  "category": {
    "v1": "special",
    "v2": "physical"
  }
}
```

### MOVE_DRAGON_DANCE — old cost 3

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_DRAGON_DANCE",
    "v2": "EFFECT_STAT_CHANGE"
  },
  "additional_effects": [
    {
      "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
      "attack": "1",
      "speed": "1"
    }
  ]
}
```

### MOVE_ROCK_BLAST — old cost 3

- `effect_changed`
- `accuracy_is_config_dependent`

```json
{
  "effect": {
    "v1": "EFFECT_MULTI_HIT",
    "v2": "EFFECT_HIT"
  },
  "accuracy": {
    "v1": 80,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 90 : 80"
  }
}
```

### MOVE_SHOCK_WAVE — old cost 3

- `effect_changed`

```json
{
  "effect": {
    "v1": "EFFECT_ALWAYS_HIT",
    "v2": "EFFECT_HIT"
  }
}
```

### MOVE_WATER_PULSE — old cost 2

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_CONFUSE_HIT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_CONFUSION",
      "chance": "20"
    }
  ]
}
```

### MOVE_DOOM_DESIRE — old cost 4

- `power_is_config_dependent`
- `accuracy_is_config_dependent`
- `damage_category_changed`

```json
{
  "power": {
    "v1": 120,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 140 : 120"
  },
  "accuracy": {
    "v1": 85,
    "v2_expr": "B_UPDATED_MOVE_DATA >= GEN_5 ? 100 : 85"
  },
  "category": {
    "v1": "physical",
    "v2": "special"
  }
}
```

### MOVE_PSYCHO_BOOST — old cost 5

- `effect_changed`
- `v2_additional_effects_present`

```json
{
  "effect": {
    "v1": "EFFECT_OVERHEAT",
    "v2": "EFFECT_HIT"
  },
  "additional_effects": [
    {
      "moveEffect": "MOVE_EFFECT_STAT_MINUS",
      "spAtk": "2",
      "self": "TRUE"
    }
  ]
}
```

## Legacy-safe moves

- `MOVE_NONE` — candidate cost **0**
- `MOVE_POUND` — candidate cost **1**
- `MOVE_MEGA_PUNCH` — candidate cost **3**
- `MOVE_SCRATCH` — candidate cost **1**
- `MOVE_GUILLOTINE` — candidate cost **5**
- `MOVE_CUT` — candidate cost **2**
- `MOVE_SLAM` — candidate cost **3**
- `MOVE_MEGA_KICK` — candidate cost **4**
- `MOVE_HORN_ATTACK` — candidate cost **3**
- `MOVE_HORN_DRILL` — candidate cost **5**
- `MOVE_TAKE_DOWN` — candidate cost **3**
- `MOVE_SUPERSONIC` — candidate cost **2**
- `MOVE_MIST` — candidate cost **2**
- `MOVE_WATER_GUN` — candidate cost **1**
- `MOVE_PECK` — candidate cost **1**
- `MOVE_DRILL_PECK` — candidate cost **3**
- `MOVE_SUBMISSION` — candidate cost **2**
- `MOVE_SEISMIC_TOSS` — candidate cost **3**
- `MOVE_STRENGTH` — candidate cost **3**
- `MOVE_LEECH_SEED` — candidate cost **3**
- `MOVE_SOLAR_BEAM` — candidate cost **5**
- `MOVE_EARTHQUAKE` — candidate cost **4**
- `MOVE_FISSURE` — candidate cost **5**
- `MOVE_RECOVER` — candidate cost **4**
- `MOVE_CONFUSE_RAY` — candidate cost **3**
- `MOVE_LIGHT_SCREEN` — candidate cost **3**
- `MOVE_REFLECT` — candidate cost **3**
- `MOVE_FOCUS_ENERGY` — candidate cost **2**
- `MOVE_METRONOME` — candidate cost **3**
- `MOVE_MIRROR_MOVE` — candidate cost **3**
- `MOVE_EGG_BOMB` — candidate cost **4**
- `MOVE_TRANSFORM` — candidate cost **3**
- `MOVE_REST` — candidate cost **3**
- `MOVE_CONVERSION` — candidate cost **1**
- `MOVE_SUBSTITUTE` — candidate cost **3**
- `MOVE_STRUGGLE` — candidate cost **0**
- `MOVE_SKETCH` — candidate cost **3**
- `MOVE_TRIPLE_KICK` — candidate cost **3**
- `MOVE_FLAIL` — candidate cost **3**
- `MOVE_REVERSAL` — candidate cost **3**
- `MOVE_SPITE` — candidate cost **2**
- `MOVE_SPIKES` — candidate cost **3**
- `MOVE_DESTINY_BOND` — candidate cost **4**
- `MOVE_ROLLOUT` — candidate cost **5**
- `MOVE_FALSE_SWIPE` — candidate cost **1**
- `MOVE_MILK_DRINK` — candidate cost **4**
- `MOVE_ATTRACT` — candidate cost **2**
- `MOVE_SLEEP_TALK` — candidate cost **2**
- `MOVE_RETURN` — candidate cost **4**
- `MOVE_PRESENT` — candidate cost **2**
- `MOVE_FRUSTRATION` — candidate cost **4**
- `MOVE_SAFEGUARD` — candidate cost **2**
- `MOVE_MAGNITUDE` — candidate cost **3**
- `MOVE_MEGAHORN` — candidate cost **5**
- `MOVE_BATON_PASS` — candidate cost **3**
- `MOVE_ENCORE` — candidate cost **3**
- `MOVE_MORNING_SUN` — candidate cost **4**
- `MOVE_SYNTHESIS` — candidate cost **4**
- `MOVE_PSYCH_UP` — candidate cost **2**
- `MOVE_SWALLOW` — candidate cost **3**
- `MOVE_TORMENT` — candidate cost **2**
- `MOVE_FACADE` — candidate cost **3**
- `MOVE_FOCUS_PUNCH` — candidate cost **5**
- `MOVE_TAUNT` — candidate cost **2**
- `MOVE_TRICK` — candidate cost **2**
- `MOVE_REVENGE` — candidate cost **2**
- `MOVE_ENDEAVOR` — candidate cost **4**
- `MOVE_SHEER_COLD` — candidate cost **5**

## New moves

- `MOVE_ROOST` — Roost
- `MOVE_GRAVITY` — Gravity
- `MOVE_MIRACLE_EYE` — Miracle Eye
- `MOVE_WAKE_UP_SLAP` — Wake-Up Slap
- `MOVE_HAMMER_ARM` — Hammer Arm
- `MOVE_GYRO_BALL` — Gyro Ball
- `MOVE_HEALING_WISH` — Healing Wish
- `MOVE_BRINE` — Brine
- `MOVE_NATURAL_GIFT` — Natural Gift
- `MOVE_FEINT` — Feint
- `MOVE_PLUCK` — Pluck
- `MOVE_TAILWIND` — Tailwind
- `MOVE_ACUPRESSURE` — Acupressure
- `MOVE_METAL_BURST` — Metal Burst
- `MOVE_U_TURN` — U-turn
- `MOVE_CLOSE_COMBAT` — Close Combat
- `MOVE_PAYBACK` — Payback
- `MOVE_ASSURANCE` — Assurance
- `MOVE_EMBARGO` — Embargo
- `MOVE_FLING` — Fling
- `MOVE_PSYCHO_SHIFT` — Psycho Shift
- `MOVE_TRUMP_CARD` — Trump Card
- `MOVE_HEAL_BLOCK` — Heal Block
- `MOVE_WRING_OUT` — Wring Out
- `MOVE_POWER_TRICK` — Power Trick
- `MOVE_GASTRO_ACID` — Gastro Acid
- `MOVE_LUCKY_CHANT` — Lucky Chant
- `MOVE_ME_FIRST` — Me First
- `MOVE_COPYCAT` — Copycat
- `MOVE_POWER_SWAP` — Power Swap
- `MOVE_GUARD_SWAP` — Guard Swap
- `MOVE_PUNISHMENT` — Punishment
- `MOVE_LAST_RESORT` — Last Resort
- `MOVE_WORRY_SEED` — Worry Seed
- `MOVE_SUCKER_PUNCH` — Sucker Punch
- `MOVE_TOXIC_SPIKES` — Toxic Spikes
- `MOVE_HEART_SWAP` — Heart Swap
- `MOVE_AQUA_RING` — Aqua Ring
- `MOVE_MAGNET_RISE` — Magnet Rise
- `MOVE_FLARE_BLITZ` — Flare Blitz
- `MOVE_FORCE_PALM` — Force Palm
- `MOVE_AURA_SPHERE` — Aura Sphere
- `MOVE_ROCK_POLISH` — Rock Polish
- `MOVE_POISON_JAB` — Poison Jab
- `MOVE_DARK_PULSE` — Dark Pulse
- `MOVE_NIGHT_SLASH` — Night Slash
- `MOVE_AQUA_TAIL` — Aqua Tail
- `MOVE_SEED_BOMB` — Seed Bomb
- `MOVE_AIR_SLASH` — Air Slash
- `MOVE_X_SCISSOR` — X-Scissor
- `MOVE_BUG_BUZZ` — Bug Buzz
- `MOVE_DRAGON_PULSE` — Dragon Pulse
- `MOVE_DRAGON_RUSH` — Dragon Rush
- `MOVE_POWER_GEM` — Power Gem
- `MOVE_DRAIN_PUNCH` — Drain Punch
- `MOVE_VACUUM_WAVE` — Vacuum Wave
- `MOVE_FOCUS_BLAST` — Focus Blast
- `MOVE_ENERGY_BALL` — Energy Ball
- `MOVE_BRAVE_BIRD` — Brave Bird
- `MOVE_EARTH_POWER` — Earth Power
- `MOVE_SWITCHEROO` — Switcheroo
- `MOVE_GIGA_IMPACT` — Giga Impact
- `MOVE_NASTY_PLOT` — Nasty Plot
- `MOVE_BULLET_PUNCH` — Bullet Punch
- `MOVE_AVALANCHE` — Avalanche
- `MOVE_ICE_SHARD` — Ice Shard
- `MOVE_SHADOW_CLAW` — Shadow Claw
- `MOVE_THUNDER_FANG` — Thunder Fang
- `MOVE_ICE_FANG` — Ice Fang
- `MOVE_FIRE_FANG` — Fire Fang
- `MOVE_SHADOW_SNEAK` — Shadow Sneak
- `MOVE_MUD_BOMB` — Mud Bomb
- `MOVE_PSYCHO_CUT` — Psycho Cut
- `MOVE_ZEN_HEADBUTT` — Zen Headbutt
- `MOVE_MIRROR_SHOT` — Mirror Shot
- `MOVE_FLASH_CANNON` — Flash Cannon
- `MOVE_ROCK_CLIMB` — Rock Climb
- `MOVE_DEFOG` — Defog
- `MOVE_TRICK_ROOM` — Trick Room
- `MOVE_DRACO_METEOR` — Draco Meteor
- `MOVE_DISCHARGE` — Discharge
- `MOVE_LAVA_PLUME` — Lava Plume
- `MOVE_LEAF_STORM` — Leaf Storm
- `MOVE_POWER_WHIP` — Power Whip
- `MOVE_ROCK_WRECKER` — Rock Wrecker
- `MOVE_CROSS_POISON` — Cross Poison
- `MOVE_GUNK_SHOT` — Gunk Shot
- `MOVE_IRON_HEAD` — Iron Head
- `MOVE_MAGNET_BOMB` — Magnet Bomb
- `MOVE_STONE_EDGE` — Stone Edge
- `MOVE_CAPTIVATE` — Captivate
- `MOVE_STEALTH_ROCK` — Stealth Rock
- `MOVE_GRASS_KNOT` — Grass Knot
- `MOVE_CHATTER` — Chatter
- `MOVE_JUDGMENT` — Judgment
- `MOVE_BUG_BITE` — Bug Bite
- `MOVE_CHARGE_BEAM` — Charge Beam
- `MOVE_WOOD_HAMMER` — Wood Hammer
- `MOVE_AQUA_JET` — Aqua Jet
- `MOVE_ATTACK_ORDER` — Attack Order
- `MOVE_DEFEND_ORDER` — Defend Order
- `MOVE_HEAL_ORDER` — Heal Order
- `MOVE_HEAD_SMASH` — Head Smash
- `MOVE_DOUBLE_HIT` — Double Hit
- `MOVE_ROAR_OF_TIME` — Roar of Time
- `MOVE_SPACIAL_REND` — Spacial Rend
- `MOVE_LUNAR_DANCE` — Lunar Dance
- `MOVE_CRUSH_GRIP` — Crush Grip
- `MOVE_MAGMA_STORM` — Magma Storm
- `MOVE_DARK_VOID` — Dark Void
- `MOVE_SEED_FLARE` — Seed Flare
- `MOVE_OMINOUS_WIND` — Ominous Wind
- `MOVE_SHADOW_FORCE` — Shadow Force
- `MOVE_HONE_CLAWS` — Hone Claws
- `MOVE_WIDE_GUARD` — Wide Guard
- `MOVE_GUARD_SPLIT` — Guard Split
- `MOVE_POWER_SPLIT` — Power Split
- `MOVE_WONDER_ROOM` — Wonder Room
- `MOVE_PSYSHOCK` — Psyshock
- `MOVE_VENOSHOCK` — Venoshock
- `MOVE_AUTOTOMIZE` — Autotomize
- `MOVE_RAGE_POWDER` — Rage Powder
- `MOVE_TELEKINESIS` — Telekinesis
- `MOVE_MAGIC_ROOM` — Magic Room
- `MOVE_SMACK_DOWN` — Smack Down
- `MOVE_STORM_THROW` — Storm Throw
- `MOVE_FLAME_BURST` — Flame Burst
- `MOVE_SLUDGE_WAVE` — Sludge Wave
- `MOVE_QUIVER_DANCE` — Quiver Dance
- `MOVE_HEAVY_SLAM` — Heavy Slam
- `MOVE_SYNCHRONOISE` — Synchronoise
- `MOVE_ELECTRO_BALL` — Electro Ball
- `MOVE_SOAK` — Soak
- `MOVE_FLAME_CHARGE` — Flame Charge
- `MOVE_COIL` — Coil
- `MOVE_LOW_SWEEP` — Low Sweep
- `MOVE_ACID_SPRAY` — Acid Spray
- `MOVE_FOUL_PLAY` — Foul Play
- `MOVE_SIMPLE_BEAM` — Simple Beam
- `MOVE_ENTRAINMENT` — Entrainment
- `MOVE_AFTER_YOU` — After You
- `MOVE_ROUND` — Round
- `MOVE_ECHOED_VOICE` — Echoed Voice
- `MOVE_CHIP_AWAY` — Chip Away
- `MOVE_CLEAR_SMOG` — Clear Smog
- `MOVE_STORED_POWER` — Stored Power
- `MOVE_QUICK_GUARD` — Quick Guard
- `MOVE_ALLY_SWITCH` — Ally Switch
- `MOVE_SCALD` — Scald
- `MOVE_SHELL_SMASH` — Shell Smash
- `MOVE_HEAL_PULSE` — Heal Pulse
- `MOVE_HEX` — Hex
- `MOVE_SKY_DROP` — Sky Drop
- `MOVE_SHIFT_GEAR` — Shift Gear
- `MOVE_CIRCLE_THROW` — Circle Throw
- `MOVE_INCINERATE` — Incinerate
- `MOVE_QUASH` — Quash
- `MOVE_ACROBATICS` — Acrobatics
- `MOVE_REFLECT_TYPE` — Reflect Type
- `MOVE_RETALIATE` — Retaliate
- `MOVE_FINAL_GAMBIT` — Final Gambit
- `MOVE_BESTOW` — Bestow
- `MOVE_INFERNO` — Inferno
- `MOVE_WATER_PLEDGE` — Water Pledge
- `MOVE_FIRE_PLEDGE` — Fire Pledge
- `MOVE_GRASS_PLEDGE` — Grass Pledge
- `MOVE_VOLT_SWITCH` — Volt Switch
- `MOVE_STRUGGLE_BUG` — Struggle Bug
- `MOVE_BULLDOZE` — Bulldoze
- `MOVE_FROST_BREATH` — Frost Breath
- `MOVE_DRAGON_TAIL` — Dragon Tail
- `MOVE_WORK_UP` — Work Up
- `MOVE_ELECTROWEB` — Electroweb
- `MOVE_WILD_CHARGE` — Wild Charge
- `MOVE_DRILL_RUN` — Drill Run
- `MOVE_DUAL_CHOP` — Dual Chop
- `MOVE_HEART_STAMP` — Heart Stamp
- `MOVE_HORN_LEECH` — Horn Leech
- `MOVE_SACRED_SWORD` — Sacred Sword
- `MOVE_RAZOR_SHELL` — Razor Shell
- `MOVE_HEAT_CRASH` — Heat Crash
- `MOVE_LEAF_TORNADO` — Leaf Tornado
- `MOVE_STEAMROLLER` — Steamroller
- `MOVE_COTTON_GUARD` — Cotton Guard
- `MOVE_NIGHT_DAZE` — Night Daze
- `MOVE_PSYSTRIKE` — Psystrike
- `MOVE_TAIL_SLAP` — Tail Slap
- `MOVE_HURRICANE` — Hurricane
- `MOVE_HEAD_CHARGE` — Head Charge
- `MOVE_GEAR_GRIND` — Gear Grind
- `MOVE_SEARING_SHOT` — Searing Shot
- `MOVE_TECHNO_BLAST` — Techno Blast
- `MOVE_RELIC_SONG` — Relic Song
- `MOVE_SECRET_SWORD` — Secret Sword
- `MOVE_GLACIATE` — Glaciate
- `MOVE_BOLT_STRIKE` — Bolt Strike
- `MOVE_BLUE_FLARE` — Blue Flare
- `MOVE_FIERY_DANCE` — Fiery Dance
- `MOVE_FREEZE_SHOCK` — Freeze Shock
- `MOVE_ICE_BURN` — Ice Burn
- `MOVE_SNARL` — Snarl
- `MOVE_ICICLE_CRASH` — Icicle Crash
- `MOVE_V_CREATE` — V-create
- `MOVE_FUSION_FLARE` — Fusion Flare
- `MOVE_FUSION_BOLT` — Fusion Bolt
- `MOVE_FLYING_PRESS` — Flying Press
- `MOVE_MAT_BLOCK` — Mat Block
- `MOVE_BELCH` — Belch
- `MOVE_ROTOTILLER` — Rototiller
- `MOVE_STICKY_WEB` — Sticky Web
- `MOVE_FELL_STINGER` — Fell Stinger
- `MOVE_PHANTOM_FORCE` — Phantom Force
- `MOVE_TRICK_OR_TREAT` — Trick-or-Treat
- `MOVE_NOBLE_ROAR` — Noble Roar
- `MOVE_ION_DELUGE` — Ion Deluge
- `MOVE_PARABOLIC_CHARGE` — Parabolic Charge
- `MOVE_FORESTS_CURSE` — Forest's Curse
- `MOVE_PETAL_BLIZZARD` — Petal Blizzard
- `MOVE_FREEZE_DRY` — Freeze-Dry
- `MOVE_DISARMING_VOICE` — Disarming Voice
- `MOVE_PARTING_SHOT` — Parting Shot
- `MOVE_TOPSY_TURVY` — Topsy-Turvy
- `MOVE_DRAINING_KISS` — Draining Kiss
- `MOVE_CRAFTY_SHIELD` — Crafty Shield
- `MOVE_FLOWER_SHIELD` — Flower Shield
- `MOVE_GRASSY_TERRAIN` — Grassy Terrain
- `MOVE_MISTY_TERRAIN` — Misty Terrain
- `MOVE_ELECTRIFY` — Electrify
- `MOVE_PLAY_ROUGH` — Play Rough
- `MOVE_FAIRY_WIND` — Fairy Wind
- `MOVE_MOONBLAST` — Moonblast
- `MOVE_BOOMBURST` — Boomburst
- `MOVE_FAIRY_LOCK` — Fairy Lock
- `MOVE_KINGS_SHIELD` — King's Shield
- `MOVE_PLAY_NICE` — Play Nice
- `MOVE_CONFIDE` — Confide
- `MOVE_DIAMOND_STORM` — Diamond Storm
- `MOVE_STEAM_ERUPTION` — Steam Eruption
- `MOVE_HYPERSPACE_HOLE` — Hyperspace Hole
- `MOVE_WATER_SHURIKEN` — Water Shuriken
- `MOVE_MYSTICAL_FIRE` — Mystical Fire
- `MOVE_SPIKY_SHIELD` — Spiky Shield
- `MOVE_AROMATIC_MIST` — Aromatic Mist
- `MOVE_EERIE_IMPULSE` — Eerie Impulse
- `MOVE_VENOM_DRENCH` — Venom Drench
- `MOVE_POWDER` — Powder
- `MOVE_GEOMANCY` — Geomancy
- `MOVE_MAGNETIC_FLUX` — Magnetic Flux
- `MOVE_HAPPY_HOUR` — Happy Hour
- `MOVE_ELECTRIC_TERRAIN` — Electric Terrain
- `MOVE_DAZZLING_GLEAM` — Dazzling Gleam
- `MOVE_CELEBRATE` — Celebrate
- `MOVE_HOLD_HANDS` — Hold Hands
- `MOVE_BABY_DOLL_EYES` — Baby-Doll Eyes
- `MOVE_NUZZLE` — Nuzzle
- `MOVE_HOLD_BACK` — Hold Back
- `MOVE_INFESTATION` — Infestation
- `MOVE_POWER_UP_PUNCH` — Power-Up Punch
- `MOVE_OBLIVION_WING` — Oblivion Wing
- `MOVE_THOUSAND_ARROWS` — Thousand Arrows
- `MOVE_THOUSAND_WAVES` — Thousand Waves
- `MOVE_LANDS_WRATH` — Land's Wrath
- `MOVE_LIGHT_OF_RUIN` — Light Of Ruin
- `MOVE_ORIGIN_PULSE` — Origin Pulse
- `MOVE_PRECIPICE_BLADES` — Precipice Blades
- `MOVE_DRAGON_ASCENT` — Dragon Ascent
- `MOVE_HYPERSPACE_FURY` — Hyperspace Fury
- `MOVE_SHORE_UP` — Shore Up
- `MOVE_FIRST_IMPRESSION` — First Impression
- `MOVE_BANEFUL_BUNKER` — Baneful Bunker
- `MOVE_SPIRIT_SHACKLE` — Spirit Shackle
- `MOVE_DARKEST_LARIAT` — Darkest Lariat
- `MOVE_SPARKLING_ARIA` — Sparkling Aria
- `MOVE_ICE_HAMMER` — Ice Hammer
- `MOVE_FLORAL_HEALING` — Floral Healing
- `MOVE_HIGH_HORSEPOWER` — High Horsepower
- `MOVE_STRENGTH_SAP` — Strength Sap
- `MOVE_SOLAR_BLADE` — Solar Blade
- `MOVE_LEAFAGE` — Leafage
- `MOVE_SPOTLIGHT` — Spotlight
- `MOVE_TOXIC_THREAD` — Toxic Thread
- `MOVE_LASER_FOCUS` — Laser Focus
- `MOVE_GEAR_UP` — Gear Up
- `MOVE_THROAT_CHOP` — Throat Chop
- `MOVE_POLLEN_PUFF` — Pollen Puff
- `MOVE_ANCHOR_SHOT` — Anchor Shot
- `MOVE_PSYCHIC_TERRAIN` — Psychic Terrain
- `MOVE_LUNGE` — Lunge
- `MOVE_FIRE_LASH` — Fire Lash
- `MOVE_POWER_TRIP` — Power Trip
- `MOVE_BURN_UP` — Burn Up
- `MOVE_SPEED_SWAP` — Speed Swap
- `MOVE_SMART_STRIKE` — Smart Strike
- `MOVE_PURIFY` — Purify
- `MOVE_REVELATION_DANCE` — Revelation Dance
- `MOVE_CORE_ENFORCER` — Core Enforcer
- `MOVE_TROP_KICK` — Trop Kick
- `MOVE_INSTRUCT` — Instruct
- `MOVE_BEAK_BLAST` — Beak Blast
- `MOVE_CLANGING_SCALES` — Clanging Scales
- `MOVE_DRAGON_HAMMER` — Dragon Hammer
- `MOVE_BRUTAL_SWING` — Brutal Swing
- `MOVE_AURORA_VEIL` — Aurora Veil
- `MOVE_SHELL_TRAP` — Shell Trap
- `MOVE_FLEUR_CANNON` — Fleur Cannon
- `MOVE_PSYCHIC_FANGS` — Psychic Fangs
- `MOVE_STOMPING_TANTRUM` — Stomping Tantrum
- `MOVE_SHADOW_BONE` — Shadow Bone
- `MOVE_ACCELEROCK` — Accelerock
- `MOVE_LIQUIDATION` — Liquidation
- `MOVE_PRISMATIC_LASER` — Prismatic Laser
- `MOVE_SPECTRAL_THIEF` — Spectral Thief
- `MOVE_SUNSTEEL_STRIKE` — Sunsteel Strike
- `MOVE_MOONGEIST_BEAM` — Moongeist Beam
- `MOVE_TEARFUL_LOOK` — Tearful Look
- `MOVE_ZING_ZAP` — Zing Zap
- `MOVE_NATURES_MADNESS` — Nature's Madness
- `MOVE_MULTI_ATTACK` — Multi-Attack
- `MOVE_MIND_BLOWN` — Mind Blown
- `MOVE_PLASMA_FISTS` — Plasma Fists
- `MOVE_PHOTON_GEYSER` — Photon Geyser
- `MOVE_ZIPPY_ZAP` — Zippy Zap
- `MOVE_SPLISHY_SPLASH` — Splishy Splash
- `MOVE_FLOATY_FALL` — Floaty Fall
- `MOVE_PIKA_PAPOW` — Pika Papow
- `MOVE_BOUNCY_BUBBLE` — Bouncy Bubble
- `MOVE_BUZZY_BUZZ` — Buzzy Buzz
- `MOVE_SIZZLY_SLIDE` — Sizzly Slide
- `MOVE_GLITZY_GLOW` — Glitzy Glow
- `MOVE_BADDY_BAD` — Baddy Bad
- `MOVE_SAPPY_SEED` — Sappy Seed
- `MOVE_FREEZY_FROST` — Freezy Frost
- `MOVE_SPARKLY_SWIRL` — Sparkly Swirl
- `MOVE_VEEVEE_VOLLEY` — Veevee Volley
- `MOVE_DOUBLE_IRON_BASH` — Double Iron Bash
- `MOVE_DYNAMAX_CANNON` — Dynamax Cannon
- `MOVE_SNIPE_SHOT` — Snipe Shot
- `MOVE_JAW_LOCK` — Jaw Lock
- `MOVE_STUFF_CHEEKS` — Stuff Cheeks
- `MOVE_NO_RETREAT` — No Retreat
- `MOVE_TAR_SHOT` — Tar Shot
- `MOVE_MAGIC_POWDER` — Magic Powder
- `MOVE_DRAGON_DARTS` — Dragon Darts
- `MOVE_TEATIME` — Teatime
- `MOVE_OCTOLOCK` — Octolock
- `MOVE_BOLT_BEAK` — Bolt Beak
- `MOVE_FISHIOUS_REND` — Fishious Rend
- `MOVE_COURT_CHANGE` — Court Change
- `MOVE_CLANGOROUS_SOUL` — Clangorous Soul
- `MOVE_BODY_PRESS` — Body Press
- `MOVE_DECORATE` — Decorate
- `MOVE_DRUM_BEATING` — Drum Beating
- `MOVE_SNAP_TRAP` — Snap Trap
- `MOVE_PYRO_BALL` — Pyro Ball
- `MOVE_BEHEMOTH_BLADE` — Behemoth Blade
- `MOVE_BEHEMOTH_BASH` — Behemoth Bash
- `MOVE_AURA_WHEEL` — Aura Wheel
- `MOVE_BREAKING_SWIPE` — Breaking Swipe
- `MOVE_BRANCH_POKE` — Branch Poke
- `MOVE_OVERDRIVE` — Overdrive
- `MOVE_APPLE_ACID` — Apple Acid
- `MOVE_GRAV_APPLE` — Grav Apple
- `MOVE_SPIRIT_BREAK` — Spirit Break
- `MOVE_STRANGE_STEAM` — Strange Steam
- `MOVE_LIFE_DEW` — Life Dew
- `MOVE_OBSTRUCT` — Obstruct
- `MOVE_FALSE_SURRENDER` — False Surrender
- `MOVE_METEOR_ASSAULT` — Meteor Assault
- `MOVE_ETERNABEAM` — Eternabeam
- `MOVE_STEEL_BEAM` — Steel Beam
- `MOVE_EXPANDING_FORCE` — Expanding Force
- `MOVE_STEEL_ROLLER` — Steel Roller
- `MOVE_SCALE_SHOT` — Scale Shot
- `MOVE_METEOR_BEAM` — Meteor Beam
- `MOVE_SHELL_SIDE_ARM` — Shell Side Arm
- `MOVE_MISTY_EXPLOSION` — Misty Explosion
- `MOVE_GRASSY_GLIDE` — Grassy Glide
- `MOVE_RISING_VOLTAGE` — Rising Voltage
- `MOVE_TERRAIN_PULSE` — Terrain Pulse
- `MOVE_SKITTER_SMACK` — Skitter Smack
- `MOVE_BURNING_JEALOUSY` — Burning Jealousy
- `MOVE_LASH_OUT` — Lash Out
- `MOVE_POLTERGEIST` — Poltergeist
- `MOVE_CORROSIVE_GAS` — Corrosive Gas
- `MOVE_COACHING` — Coaching
- `MOVE_FLIP_TURN` — Flip Turn
- `MOVE_TRIPLE_AXEL` — Triple Axel
- `MOVE_DUAL_WINGBEAT` — Dual Wingbeat
- `MOVE_SCORCHING_SANDS` — Scorching Sands
- `MOVE_JUNGLE_HEALING` — Jungle Healing
- `MOVE_WICKED_BLOW` — Wicked Blow
- `MOVE_SURGING_STRIKES` — Surging Strikes
- `MOVE_THUNDER_CAGE` — Thunder Cage
- `MOVE_DRAGON_ENERGY` — Dragon Energy
- `MOVE_FREEZING_GLARE` — Freezing Glare
- `MOVE_FIERY_WRATH` — Fiery Wrath
- `MOVE_THUNDEROUS_KICK` — Thunderous Kick
- `MOVE_GLACIAL_LANCE` — Glacial Lance
- `MOVE_ASTRAL_BARRAGE` — Astral Barrage
- `MOVE_EERIE_SPELL` — Eerie Spell
- `MOVE_DIRE_CLAW` — Dire Claw
- `MOVE_PSYSHIELD_BASH` — Psyshield Bash
- `MOVE_POWER_SHIFT` — Power Shift
- `MOVE_STONE_AXE` — Stone Axe
- `MOVE_SPRINGTIDE_STORM` — Springtide Storm
- `MOVE_MYSTICAL_POWER` — Mystical Power
- `MOVE_RAGING_FURY` — Raging Fury
- `MOVE_WAVE_CRASH` — Wave Crash
- `MOVE_CHLOROBLAST` — Chloroblast
- `MOVE_MOUNTAIN_GALE` — Mountain Gale
- `MOVE_VICTORY_DANCE` — Victory Dance
- `MOVE_HEADLONG_RUSH` — Headlong Rush
- `MOVE_BARB_BARRAGE` — Barb Barrage
- `MOVE_ESPER_WING` — Esper Wing
- `MOVE_BITTER_MALICE` — Bitter Malice
- `MOVE_SHELTER` — Shelter
- `MOVE_TRIPLE_ARROWS` — Triple Arrows
- `MOVE_INFERNAL_PARADE` — Infernal Parade
- `MOVE_CEASELESS_EDGE` — Ceaseless Edge
- `MOVE_BLEAKWIND_STORM` — Bleakwind Storm
- `MOVE_WILDBOLT_STORM` — Wildbolt Storm
- `MOVE_SANDSEAR_STORM` — Sandsear Storm
- `MOVE_LUNAR_BLESSING` — Lunar Blessing
- `MOVE_TAKE_HEART` — Take Heart
- `MOVE_TERA_BLAST` — Tera Blast
- `MOVE_SILK_TRAP` — Silk Trap
- `MOVE_AXE_KICK` — Axe Kick
- `MOVE_LAST_RESPECTS` — Last Respects
- `MOVE_LUMINA_CRASH` — Lumina Crash
- `MOVE_ORDER_UP` — Order Up
- `MOVE_JET_PUNCH` — Jet Punch
- `MOVE_SPICY_EXTRACT` — Spicy Extract
- `MOVE_SPIN_OUT` — Spin Out
- `MOVE_POPULATION_BOMB` — Population Bomb
- `MOVE_ICE_SPINNER` — Ice Spinner
- `MOVE_GLAIVE_RUSH` — Glaive Rush
- `MOVE_REVIVAL_BLESSING` — Revival Blessing
- `MOVE_SALT_CURE` — Salt Cure
- `MOVE_TRIPLE_DIVE` — Triple Dive
- `MOVE_MORTAL_SPIN` — Mortal Spin
- `MOVE_DOODLE` — Doodle
- `MOVE_FILLET_AWAY` — Fillet Away
- `MOVE_KOWTOW_CLEAVE` — Kowtow Cleave
- `MOVE_FLOWER_TRICK` — Flower Trick
- `MOVE_TORCH_SONG` — Torch Song
- `MOVE_AQUA_STEP` — Aqua Step
- `MOVE_RAGING_BULL` — Raging Bull
- `MOVE_MAKE_IT_RAIN` — Make It Rain
- `MOVE_RUINATION` — Ruination
- `MOVE_COLLISION_COURSE` — Collision Course
- `MOVE_ELECTRO_DRIFT` — Electro Drift
- `MOVE_SHED_TAIL` — Shed Tail
- `MOVE_CHILLY_RECEPTION` — Chilly Reception
- `MOVE_TIDY_UP` — Tidy Up
- `MOVE_SNOWSCAPE` — Snowscape
- `MOVE_POUNCE` — Pounce
- `MOVE_TRAILBLAZE` — Trailblaze
- `MOVE_CHILLING_WATER` — Chilling Water
- `MOVE_HYPER_DRILL` — Hyper Drill
- `MOVE_TWIN_BEAM` — Twin Beam
- `MOVE_RAGE_FIST` — Rage Fist
- `MOVE_ARMOR_CANNON` — Armor Cannon
- `MOVE_BITTER_BLADE` — Bitter Blade
- `MOVE_DOUBLE_SHOCK` — Double Shock
- `MOVE_GIGATON_HAMMER` — Gigaton Hammer
- `MOVE_COMEUPPANCE` — Comeuppance
- `MOVE_AQUA_CUTTER` — Aqua Cutter
- `MOVE_BLAZING_TORQUE` — Blazing Torque
- `MOVE_WICKED_TORQUE` — Wicked Torque
- `MOVE_NOXIOUS_TORQUE` — Noxious Torque
- `MOVE_COMBAT_TORQUE` — Combat Torque
- `MOVE_MAGICAL_TORQUE` — Magical Torque
- `MOVE_PSYBLADE` — Psyblade
- `MOVE_HYDRO_STEAM` — Hydro Steam
- `MOVE_BLOOD_MOON` — Blood Moon
- `MOVE_MATCHA_GOTCHA` — Matcha Gotcha
- `MOVE_SYRUP_BOMB` — Syrup Bomb
- `MOVE_IVY_CUDGEL` — Ivy Cudgel
- `MOVE_ELECTRO_SHOT` — Electro Shot
- `MOVE_TERA_STARSTORM` — Tera Starstorm
- `MOVE_FICKLE_BEAM` — Fickle Beam
- `MOVE_BURNING_BULWARK` — Burning Bulwark
- `MOVE_THUNDERCLAP` — Thunderclap
- `MOVE_MIGHTY_CLEAVE` — Mighty Cleave
- `MOVE_TACHYON_CUTTER` — Tachyon Cutter
- `MOVE_HARD_PRESS` — Hard Press
- `MOVE_DRAGON_CHEER` — Dragon Cheer
- `MOVE_ALLURING_VOICE` — Alluring Voice
- `MOVE_TEMPER_FLARE` — Temper Flare
- `MOVE_SUPERCELL_SLAM` — Supercell Slam
- `MOVE_PSYCHIC_NOISE` — Psychic Noise
- `MOVE_UPPER_HAND` — Upper Hand
- `MOVE_MALIGNANT_CHAIN` — Malignant Chain
