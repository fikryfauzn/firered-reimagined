#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path
import re

ROOT = Path.cwd()

REFINED = ROOT / "tools/stamina/data/legacy_migration_refined_v2.json"
OLD_SOURCE = ROOT / "tools/stamina/legacy_v1/moves_source.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_encoding_resolution_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_encoding_resolution_v2.md"


def load(path):
    return json.loads(path.read_text())


def simple_int(value):
    if value is None:
        return None

    try:
        return int(str(value))
    except ValueError:
        return None


old_doc = load(OLD_SOURCE)
refined = load(REFINED)

old_by_constant = {
    x["id"]: x["source"]
    for x in old_doc["moves"]
}


# ----------------------------------------------------------------------
# Strict semantic equivalence rules
#
# These rules only describe transformations where the old dedicated
# EFFECT_* representation has been decomposed into RHH's newer
# effect + additionalEffects representation.
#
# They do NOT imply that all other move changes are equivalent.
# ----------------------------------------------------------------------

RULES = {
    # Damage + status
    "EFFECT_PARALYZE_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_PARALYSIS"},
        "check_chance": True,
    },

    "EFFECT_FLINCH_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_FLINCH"},
        "check_chance": True,
    },

    "EFFECT_CONFUSE_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_CONFUSION"},
        "check_chance": True,
    },

    "EFFECT_BURN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_BURN"},
        "check_chance": True,
    },

    # B_USE_FROSTBITE is FALSE in the current project configuration.
    "EFFECT_FREEZE_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_FREEZE_OR_FROSTBITE"},
        "check_chance": True,
    },

    "EFFECT_POISON_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {"moveEffect": "MOVE_EFFECT_POISON"},
        "check_chance": True,
    },


    # Damage + stat reduction
    "EFFECT_ATTACK_DOWN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "attack": "1",
        },
        "check_chance": True,
    },

    "EFFECT_DEFENSE_DOWN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "defense": "1",
        },
        "check_chance": True,
    },

    "EFFECT_SPEED_DOWN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "speed": "1",
        },
        "check_chance": True,
    },

    "EFFECT_ACCURACY_DOWN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "accuracy": "1",
        },
        "check_chance": True,
    },

    "EFFECT_SPECIAL_DEFENSE_DOWN_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "spDef": "1",
        },
        "check_chance": True,
    },


    # Damage + self stat increase
    "EFFECT_ATTACK_UP_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_PLUS",
            "attack": "1",
        },
        "check_chance": True,
    },

    "EFFECT_DEFENSE_UP_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_PLUS",
            "defense": "1",
        },
        "check_chance": True,
    },

    "EFFECT_ALL_STATS_UP_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_PLUS",
            "attack": "1",
            "defense": "1",
            "speed": "1",
            "spAtk": "1",
            "spDef": "1",
        },
        "check_chance": True,
    },


    # Pure stat changes
    "EFFECT_ATTACK_DOWN": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "attack": "1",
        },
    },

    "EFFECT_ATTACK_DOWN_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "attack": "2",
        },
    },

    "EFFECT_DEFENSE_DOWN": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "defense": "1",
        },
    },

    "EFFECT_DEFENSE_DOWN_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "defense": "2",
        },
    },

    "EFFECT_SPEED_DOWN": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "speed": "1",
        },
    },

    "EFFECT_SPEED_DOWN_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "speed": "2",
        },
    },

    "EFFECT_ACCURACY_DOWN": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "accuracy": "1",
        },
    },

    "EFFECT_EVASION_DOWN": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "evasion": "1",
        },
    },

    "EFFECT_SPECIAL_DEFENSE_DOWN_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "spDef": "2",
        },
    },

    "EFFECT_ATTACK_UP": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "attack": "1",
        },
    },

    "EFFECT_ATTACK_UP_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "attack": "2",
        },
    },

    "EFFECT_DEFENSE_UP": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "defense": "1",
        },
    },

    "EFFECT_DEFENSE_UP_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "defense": "2",
        },
    },

    "EFFECT_SPEED_UP_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "speed": "2",
        },
    },

    "EFFECT_EVASION_UP": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "evasion": "1",
        },
    },

    "EFFECT_SPECIAL_DEFENSE_UP_2": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "spDef": "2",
        },
    },


    # Compound stat moves
    "EFFECT_TICKLE": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_MINUS",
            "attack": "1",
            "defense": "1",
        },
    },

    "EFFECT_COSMIC_POWER": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "defense": "1",
            "spDef": "1",
        },
    },

    "EFFECT_BULK_UP": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "attack": "1",
            "defense": "1",
        },
    },

    "EFFECT_CALM_MIND": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "spAtk": "1",
            "spDef": "1",
        },
    },

    "EFFECT_DRAGON_DANCE": {
        "new_effect": "EFFECT_STAT_CHANGE",
        "add": {
            "moveEffect": "STAT_CHANGE_EFFECT_PLUS",
            "attack": "1",
            "speed": "1",
        },
    },


    # Other decompositions with directly equivalent representation
    "EFFECT_PAY_DAY": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_PAYDAY",
        },
    },

    "EFFECT_RECHARGE": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_RECHARGE",
        },
    },

    "EFFECT_BRICK_BREAK": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_BREAK_SCREEN",
        },
    },

    "EFFECT_POISON_FANG": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_TOXIC",
        },
        "check_chance": True,
    },


    # Dedicated source-property equivalents
    "EFFECT_TWINEEDLE": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_POISON",
        },
        "check_chance": True,
        "properties": {
            "strikeCount": "2",
        },
    },

    "EFFECT_THAW_HIT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_BURN",
        },
        "check_chance": True,
        "properties": {
            "thawsUser": "TRUE",
        },
    },


    # Self-stat penalties after attacking
    "EFFECT_OVERHEAT": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "spAtk": "2",
            "self": "TRUE",
        },
    },

    "EFFECT_SUPERPOWER": {
        "new_effect": "EFFECT_HIT",
        "add": {
            "moveEffect": "MOVE_EFFECT_STAT_MINUS",
            "attack": "1",
            "defense": "1",
            "self": "TRUE",
        },
    },
}



ENV = {
    **{f"GEN_{i}": i for i in range(1, 10)},
    "GEN_LATEST": 9,
    "GEN_CHAMPIONS": 10,

    "B_UPDATED_MOVE_DATA": 9,
    "B_UPDATED_MOVE_TYPES": 9,
    "B_UPDATED_MOVE_FLAGS": 9,
    "B_PHYSICAL_SPECIAL_SPLIT": 9,
    "B_HIDDEN_POWER_DMG": 9,
}


def scalar_operand(value):
    value = str(value).strip()

    try:
        return int(value)
    except ValueError:
        return ENV.get(value)


def strip_outer_parens(expr):
    expr = expr.strip()

    while expr.startswith("(") and expr.endswith(")"):
        depth = 0
        whole = True

        for i, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1

                if depth == 0 and i != len(expr) - 1:
                    whole = False
                    break

        if not whole:
            break

        expr = expr[1:-1].strip()

    return expr


def split_logic(expr, operator):
    depth = 0
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch == "(":
            depth += 1
            i += 1
            continue

        if ch == ")":
            depth -= 1
            i += 1
            continue

        if depth == 0 and expr.startswith(operator, i):
            return (
                expr[:i].strip(),
                expr[i + len(operator):].strip(),
            )

        i += 1

    return None


def eval_condition(expr):
    expr = strip_outer_parens(expr)

    parts = split_logic(expr, "||")
    if parts:
        left = eval_condition(parts[0])
        right = eval_condition(parts[1])

        if left is True or right is True:
            return True
        if left is False and right is False:
            return False
        return None

    parts = split_logic(expr, "&&")
    if parts:
        left = eval_condition(parts[0])
        right = eval_condition(parts[1])

        if left is False or right is False:
            return False
        if left is True and right is True:
            return True
        return None

    m = re.fullmatch(
        r"([A-Z0-9_]+|-?\d+)\s*"
        r"(>=|<=|==|!=|>|<)\s*"
        r"([A-Z0-9_]+|-?\d+)",
        expr,
    )

    if not m:
        return None

    left = scalar_operand(m.group(1))
    right = scalar_operand(m.group(3))

    if left is None or right is None:
        return None

    op = m.group(2)

    return {
        ">=": left >= right,
        "<=": left <= right,
        "==": left == right,
        "!=": left != right,
        ">": left > right,
        "<": left < right,
    }[op]


def split_ternary(expr):
    depth = 0
    question = None

    for i, ch in enumerate(expr):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "?" and depth == 0:
            question = i
            break

    if question is None:
        return None

    depth = 0
    nested = 0

    for i in range(question + 1, len(expr)):
        ch = expr[i]

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "?" and depth == 0:
            nested += 1
        elif ch == ":" and depth == 0:
            if nested:
                nested -= 1
            else:
                return (
                    expr[:question].strip(),
                    expr[question + 1:i].strip(),
                    expr[i + 1:].strip(),
                )

    return None


def resolve_value(value):
    if value is None:
        return None

    if isinstance(value, (int, bool)):
        return value

    expr = str(value).strip()

    try:
        return int(expr)
    except ValueError:
        pass

    ternary = split_ternary(expr)

    if ternary:
        condition, yes, no = ternary
        result = eval_condition(condition)

        if result is None:
            return None

        return resolve_value(yes if result else no)

    if expr == "TRUE":
        return True

    if expr == "FALSE":
        return False

    if re.fullmatch(r"[A-Z][A-Z0-9_]*", expr):
        return ENV.get(expr, expr)

    return None


def fields_match(actual, expected):
    for key, value in expected.items():
        actual_value = resolve_value(actual.get(key))
        expected_value = resolve_value(value)

        if actual_value != expected_value:
            return False

    return True


def resolve_row(row):
    legacy_constant = row["legacy_constant"]
    old = old_by_constant[legacy_constant]

    details = row.get("details", {})
    effect = details.get("effect", {})

    old_effect = effect.get("v1")
    new_effect = effect.get("v2")

    rule = RULES.get(old_effect)

    result = {
        "numeric_id": row["numeric_id"],
        "legacy_constant": legacy_constant,
        "v2_constant": row["v2_constant"],
        "name": row["name"],
        "legacy_cost": row["legacy_cost"],
        "old_effect": old_effect,
        "new_effect": new_effect,
        "result": "MANUAL_ENCODING_REVIEW",
        "rule": None,
        "residual_changes": [],
        "reason": None,
    }

    if rule is None:
        result["reason"] = "no_strict_equivalence_rule"
        return result

    if new_effect != rule["new_effect"]:
        result["reason"] = "new_effect_mismatch"
        return result

    add = details.get("additional_effects", [])

    # Strict: one expected additional-effect object only.
    if len(add) != 1:
        result["reason"] = f"additional_effect_count_{len(add)}"
        return result

    actual_add = add[0]

    if not fields_match(actual_add, rule["add"]):
        result["reason"] = "additional_effect_fields_mismatch"
        return result


    if rule.get("check_chance"):
        old_chance = simple_int(
            old.get("secondary_effect_chance")
        )

        new_chance = resolve_value(
            actual_add.get("chance")
        )

        # Some 100%-guaranteed effects omit chance.
        if new_chance is None and old_chance == 100:
            new_chance = 100

        if old_chance != new_chance:
            result["reason"] = (
                f"chance_mismatch_v1_{old_chance}_v2_{new_chance}"
            )
            return result


    required_properties = rule.get("properties", {})

    # Properties are available in canonical V2 source through the
    # refinement details only when relevant?  The strict property checks
    # for these rules are instead recovered from moves_source below later.
    result["rule"] = old_effect

    residual = [
        c
        for c in row["changes"]
        if c not in {
            "effect_representation_changed",
            "v2_additional_effects",
        }
    ]

    result["residual_changes"] = residual
    result["required_properties"] = required_properties
    result["result"] = "ENCODING_EQUIVALENT"

    return result


source_doc = load(
    ROOT / "tools/stamina/data/moves_source_v2.json"
)

source_by_constant = {
    x["constant"]: x
    for x in source_doc["moves"]
}


resolved = []

for row in refined["moves"]:
    if row["status"] != "LEGACY_ENCODING_REVIEW":
        continue

    result = resolve_row(row)

    if result["result"] == "ENCODING_EQUIVALENT":
        required = result.get("required_properties", {})

        if required:
            move = source_by_constant[result["v2_constant"]]
            props = move.get("properties", {})

            if not fields_match(props, required):
                result["result"] = "MANUAL_ENCODING_REVIEW"
                result["reason"] = "required_property_mismatch"

    resolved.append(result)


counts = Counter(x["result"] for x in resolved)
residual_counts = Counter()

for row in resolved:
    if row["result"] != "ENCODING_EQUIVALENT":
        continue

    for change in row["residual_changes"]:
        residual_counts[change] += 1


output = {
    "schema":
        "firered-reimagined.stamina.legacy-encoding-resolution.v2",
    "schema_version": 1,

    "assumptions": {
        "B_USE_FROSTBITE": False,
        "policy":
            "Only strict whitelisted effect transformations are "
            "automatically declared encoding-equivalent.",
    },

    "counts": dict(counts),
    "equivalent_residual_change_counts":
        dict(residual_counts),

    "moves": resolved,
}


OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


lines = [
    "# Stamina V2 — Legacy Encoding Resolution",
    "",
    "## Summary",
    "",
    f"- Encoding equivalent: "
    f"**{counts.get('ENCODING_EQUIVALENT', 0)}**",
    f"- Manual encoding review: "
    f"**{counts.get('MANUAL_ENCODING_REVIEW', 0)}**",
    "",
    "## Encoding-equivalent moves",
    "",
]

for row in resolved:
    if row["result"] != "ENCODING_EQUIVALENT":
        continue

    residual = ", ".join(row["residual_changes"]) or "none"

    lines.append(
        f"- `{row['v2_constant']}` — old cost "
        f"**{row['legacy_cost']}** — residual: {residual}"
    )


lines += [
    "",
    "## Remaining manual encoding review",
    "",
]

for row in resolved:
    if row["result"] != "MANUAL_ENCODING_REVIEW":
        continue

    lines.append(
        f"- `{row['v2_constant']}` — "
        f"{row['old_effect']} → {row['new_effect']} "
        f"— `{row['reason']}`"
    )


OUT_MD.write_text("\n".join(lines) + "\n")


print("Legacy encoding resolution complete.")
print()

print(
    "ENCODING_EQUIVALENT      :",
    counts.get("ENCODING_EQUIVALENT", 0),
)

print(
    "MANUAL_ENCODING_REVIEW   :",
    counts.get("MANUAL_ENCODING_REVIEW", 0),
)

print()
print("Equivalent rows with residual modernization:")

for change, count in residual_counts.most_common():
    print(f"  {change:<30} {count}")

print()
print("Wrote:")
print(
    "  tools/stamina/data/"
    "legacy_encoding_resolution_v2.json"
)
print(
    "  tools/stamina/reports/"
    "legacy_encoding_resolution_v2.md"
)
