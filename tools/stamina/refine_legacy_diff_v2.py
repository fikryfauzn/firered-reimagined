#!/usr/bin/env python3

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

OLD_SOURCE = ROOT / "tools/stamina/legacy_v1/moves_source.json"
OLD_STAMINA = ROOT / "tools/stamina/legacy_v1/stamina_moves.json"
NEW_SOURCE = ROOT / "tools/stamina/data/moves_source_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_migration_refined_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_migration_refined_v2.md"


ALIASES = {
    "MOVE_VICE_GRIP": "MOVE_VISE_GRIP",
    "MOVE_HI_JUMP_KICK": "MOVE_HIGH_JUMP_KICK",
    "MOVE_FAINT_ATTACK": "MOVE_FEINT_ATTACK",
    "MOVE_SMELLING_SALT": "MOVE_SMELLING_SALTS",
}


# Current project battle baseline:
#
# GEN_LATEST = GEN_9
# B_UPDATED_MOVE_DATA = GEN_LATEST
# B_UPDATED_MOVE_TYPES = GEN_LATEST
# B_UPDATED_MOVE_FLAGS = GEN_LATEST
# B_PHYSICAL_SPECIAL_SPLIT = GEN_LATEST
#
ENV = {
    **{f"GEN_{i}": i for i in range(1, 10)},
    "GEN_LATEST": 9,

    "B_UPDATED_MOVE_DATA": 9,
    "B_UPDATED_MOVE_TYPES": 9,
    "B_UPDATED_MOVE_FLAGS": 9,
    "B_PHYSICAL_SPECIAL_SPLIT": 9,
}


def load(path):
    return json.loads(path.read_text())



# Additional active project configuration needed for semantic resolution.
ENV.update({
    "GEN_CHAMPIONS": 10,
    "B_HIDDEN_POWER_DMG": 9,
})

def split_ternary(expr):
    """
    Split:
        CONDITION ? TRUE : FALSE

    at top level.
    """
    depth = 0
    q = None

    for i, c in enumerate(expr):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "?" and depth == 0:
            q = i
            break

    if q is None:
        return None

    depth = 0
    nested_q = 0

    for i in range(q + 1, len(expr)):
        c = expr[i]

        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "?" and depth == 0:
            nested_q += 1
        elif c == ":" and depth == 0:
            if nested_q:
                nested_q -= 1
            else:
                return (
                    expr[:q].strip(),
                    expr[q + 1:i].strip(),
                    expr[i + 1:].strip(),
                )

    return None


def operand(value):
    value = value.strip()

    if re.fullmatch(r"-?\d+", value):
        return int(value)

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


def eval_condition(condition):
    condition = strip_outer_parens(condition)

    # Logical OR
    parts = split_logic(condition, "||")
    if parts:
        left, right = parts
        lv = eval_condition(left)
        rv = eval_condition(right)

        if lv is True or rv is True:
            return True
        if lv is False and rv is False:
            return False
        return None

    # Logical AND
    parts = split_logic(condition, "&&")
    if parts:
        left, right = parts
        lv = eval_condition(left)
        rv = eval_condition(right)

        if lv is False or rv is False:
            return False
        if lv is True and rv is True:
            return True
        return None

    m = re.fullmatch(
        r"([A-Z0-9_]+|-?\d+)\s*"
        r"(>=|<=|==|!=|>|<)\s*"
        r"([A-Z0-9_]+|-?\d+)",
        condition,
    )

    if not m:
        return None

    left = operand(m.group(1))
    right = operand(m.group(3))

    if left is None or right is None:
        return None

    op = m.group(2)

    if op == ">=":
        return left >= right
    if op == "<=":
        return left <= right
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    if op == ">":
        return left > right
    if op == "<":
        return left < right

    return None


def resolve(expr):
    if expr is None:
        return None

    expr = str(expr).strip()

    if re.fullmatch(r"-?\d+", expr):
        return int(expr)

    ternary = split_ternary(expr)

    if ternary:
        cond, true_expr, false_expr = ternary
        answer = eval_condition(cond)

        if answer is None:
            return None

        return resolve(true_expr if answer else false_expr)

    # plain symbolic value:
    # TYPE_WATER, TARGET_SELECTED, EFFECT_HIT, etc.
    if re.fullmatch(r"[A-Z][A-Z0-9_]*", expr):
        return ENV.get(expr, expr)

    return None


def old_category(old):
    return old["gen3_damage_class"]


def new_category(new):
    raw = resolve(new["category_expr"])

    mapping = {
        "DAMAGE_CATEGORY_PHYSICAL": "physical",
        "DAMAGE_CATEGORY_SPECIAL": "special",
        "DAMAGE_CATEGORY_STATUS": "status",
    }

    return mapping.get(raw, raw)


def normalize_target(value):
    if value is None:
        return None
    return value.replace("MOVE_TARGET_", "TARGET_")


old_source_doc = load(OLD_SOURCE)
old_stamina_doc = load(OLD_STAMINA)
new_source_doc = load(NEW_SOURCE)

old_source = {
    x["id"]: x["source"]
    for x in old_source_doc["moves"]
}

old_stamina = old_stamina_doc["moves"]

new_by_constant = {
    x["constant"]: x
    for x in new_source_doc["moves"]
}

new_by_id = {
    x["id"]: x
    for x in new_source_doc["moves"]
}


rows = []


for old_constant, stamina in old_stamina.items():
    numeric_id = stamina["numeric_id"]

    canonical = ALIASES.get(old_constant, old_constant)

    new = new_by_constant.get(canonical)

    if new is None:
        new = new_by_id.get(numeric_id)

    if new is None:
        rows.append({
            "numeric_id": numeric_id,
            "legacy_constant": old_constant,
            "v2_constant": None,
            "name": None,
            "legacy_cost": stamina["cost"],
            "status": "LEGACY_UNRESOLVED",
            "severity": "HIGH",
            "changes": ["identity_unresolved"],
            "details": {},
        })
        continue

    old = old_source[old_constant]

    changes = []
    details = {}


    # ------------------------------------------------------------
    # POWER
    # ------------------------------------------------------------

    np = resolve(new["power_expr"])

    if np is None:
        changes.append("power_unresolved")
        details["power"] = {
            "v1": old["power"],
            "v2_expr": new["power_expr"],
        }

    elif np != old["power"]:
        changes.append("power_changed")
        details["power"] = {
            "v1": old["power"],
            "v2": np,
            "delta": np - old["power"],
        }


    # ------------------------------------------------------------
    # ACCURACY
    # ------------------------------------------------------------

    na = resolve(new["accuracy_expr"])

    if na is None:
        changes.append("accuracy_unresolved")
        details["accuracy"] = {
            "v1": old["accuracy"],
            "v2_expr": new["accuracy_expr"],
        }

    elif na != old["accuracy"]:
        changes.append("accuracy_changed")
        details["accuracy"] = {
            "v1": old["accuracy"],
            "v2": na,
            "delta": na - old["accuracy"],
        }


    # ------------------------------------------------------------
    # TYPE
    # ------------------------------------------------------------

    nt = resolve(new["type_expr"])

    if nt is None:
        changes.append("type_unresolved")
        details["type"] = {
            "v1": old["type"],
            "v2_expr": new["type_expr"],
        }

    elif nt != old["type"]:
        changes.append("type_changed")
        details["type"] = {
            "v1": old["type"],
            "v2": nt,
        }


    # ------------------------------------------------------------
    # TARGET
    # ------------------------------------------------------------

    otarget = normalize_target(old["target"])
    ntarget = resolve(new["target_expr"])

    if ntarget is None:
        changes.append("target_unresolved")
        details["target"] = {
            "v1": otarget,
            "v2_expr": new["target_expr"],
        }

    elif ntarget != otarget:
        changes.append("target_changed")
        details["target"] = {
            "v1": otarget,
            "v2": ntarget,
        }


    # ------------------------------------------------------------
    # PRIORITY
    # ------------------------------------------------------------

    npriority = resolve(new["priority_expr"])

    if npriority is None:
        changes.append("priority_unresolved")
        details["priority"] = {
            "v1": old["priority"],
            "v2_expr": new["priority_expr"],
        }

    elif npriority != old["priority"]:
        changes.append("priority_changed")
        details["priority"] = {
            "v1": old["priority"],
            "v2": npriority,
        }


    # ------------------------------------------------------------
    # CATEGORY
    #
    # Gen III category changes are expected because Expansion uses
    # the modern physical/special split.
    # ------------------------------------------------------------

    oc = old_category(old)
    nc = new_category(new)

    if oc not in {"none", None} and nc is not None and oc != nc:
        changes.append("damage_category_changed")
        details["category"] = {
            "v1": oc,
            "v2": nc,
        }


    # ------------------------------------------------------------
    # EFFECT REPRESENTATION
    # ------------------------------------------------------------

    effect_changed = old["effect"] != new["effect"]

    if effect_changed:
        changes.append("effect_representation_changed")
        details["effect"] = {
            "v1": old["effect"],
            "v2": new["effect"],
        }


    if new["additional_effects"]:
        changes.append("v2_additional_effects")
        details["additional_effects"] = new["additional_effects"]


    # ------------------------------------------------------------
    # TRIAGE
    # ------------------------------------------------------------

    meaningful = set(changes)

    # These alone do not invalidate the old cost.
    low_change_types = {
        "damage_category_changed",
    }

    # Effect + additionalEffects is very often RHH moving an old
    # dedicated EFFECT_* into generic EFFECT_HIT + nested effect data.
    representation_pattern = (
        "effect_representation_changed" in meaningful
        and "v2_additional_effects" in meaningful
    )

    major = False

    if "priority_changed" in meaningful:
        major = True

    if "type_changed" in meaningful:
        major = True

    if "target_changed" in meaningful:
        major = True

    if "power_unresolved" in meaningful:
        major = True

    if "accuracy_unresolved" in meaningful:
        major = True

    if "type_unresolved" in meaningful:
        major = True

    if "target_unresolved" in meaningful:
        major = True

    if "priority_unresolved" in meaningful:
        major = True

    if "power_changed" in meaningful:
        p = details["power"]

        old_power = p["v1"]
        new_power = p["v2"]

        if old_power == 0:
            if new_power != 0:
                major = True
        else:
            delta = abs(new_power - old_power)
            ratio = delta / old_power

            # Significant damage-profile change.
            if delta >= 20 or ratio >= 0.25:
                major = True

    if "accuracy_changed" in meaningful:
        if abs(details["accuracy"]["delta"]) >= 20:
            major = True


    # Structural sentinels retain explicit existing semantics.
    if old_constant in {"MOVE_NONE", "MOVE_STRUGGLE"}:
        status = "LEGACY_SAFE"
        severity = "NONE"

    elif not meaningful:
        status = "LEGACY_SAFE"
        severity = "NONE"

    elif meaningful <= low_change_types:
        status = "LEGACY_MODERNIZED_MINOR"
        severity = "LOW"

    elif major:
        status = "LEGACY_REAUDIT"
        severity = "HIGH"

    elif representation_pattern:
        status = "LEGACY_ENCODING_REVIEW"
        severity = "MEDIUM"

    else:
        status = "LEGACY_MODERNIZED_MINOR"
        severity = "LOW"


    rows.append({
        "numeric_id": numeric_id,
        "legacy_constant": old_constant,
        "v2_constant": new["constant"],
        "name": new["name"],
        "legacy_cost": stamina["cost"],
        "legacy_primary_role": stamina["primary_role"],
        "legacy_mechanic_tags": stamina["mechanic_tags"],
        "legacy_stamina_rules": stamina["stamina_rules"],
        "legacy_design": stamina["design"],
        "status": status,
        "severity": severity,
        "changes": changes,
        "details": details,
    })


# ------------------------------------------------------------
# NEW MOVES
# ------------------------------------------------------------

for new in new_source_doc["moves"]:
    if new["id"] <= 354:
        continue

    rows.append({
        "numeric_id": new["id"],
        "legacy_constant": None,
        "v2_constant": new["constant"],
        "name": new["name"],
        "legacy_cost": None,
        "legacy_primary_role": None,
        "legacy_mechanic_tags": [],
        "legacy_stamina_rules": [],
        "legacy_design": None,
        "status": "NEW_MOVE",
        "severity": "NEW",
        "changes": ["new_move"],
        "details": {},
    })


rows.sort(key=lambda x: x["numeric_id"])

counts = Counter(x["status"] for x in rows)
change_counts = Counter()

for row in rows:
    for c in row["changes"]:
        change_counts[c] += 1


out = {
    "schema": "firered-reimagined.stamina.legacy-migration-refined.v2",
    "schema_version": 1,
    "active_rules": {
        "generation": 9,
        "B_UPDATED_MOVE_DATA": 9,
        "B_UPDATED_MOVE_TYPES": 9,
        "B_UPDATED_MOVE_FLAGS": 9,
        "B_PHYSICAL_SPECIAL_SPLIT": 9,
    },
    "counts": dict(counts),
    "change_counts": dict(change_counts),
    "moves": rows,
}

OUT_JSON.write_text(
    json.dumps(out, indent=2) + "\n"
)


# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

lines = [
    "# Stamina V2 — Refined Legacy Migration",
    "",
    "## Summary",
    "",
]

for status in [
    "LEGACY_SAFE",
    "LEGACY_MODERNIZED_MINOR",
    "LEGACY_ENCODING_REVIEW",
    "LEGACY_REAUDIT",
    "LEGACY_UNRESOLVED",
    "NEW_MOVE",
]:
    lines.append(
        f"- `{status}`: **{counts.get(status, 0)}**"
    )


lines += [
    "",
    "## Change counts",
    "",
]

for change, count in change_counts.most_common():
    if change == "new_move":
        continue

    lines.append(f"- `{change}`: **{count}**")


for section, title in [
    ("LEGACY_REAUDIT", "High-priority re-audit"),
    ("LEGACY_ENCODING_REVIEW", "Effect-encoding review"),
    ("LEGACY_MODERNIZED_MINOR", "Minor modernization"),
    ("LEGACY_SAFE", "Legacy-safe"),
]:
    lines += [
        "",
        f"## {title}",
        "",
    ]

    for row in rows:
        if row["status"] != section:
            continue

        lines.append(
            f"- `{row['v2_constant'] or row['legacy_constant']}` "
            f"— old cost **{row['legacy_cost']}**"
        )

        if section != "LEGACY_SAFE":
            lines.append(
                f"  - changes: {', '.join(row['changes'])}"
            )


OUT_MD.write_text("\n".join(lines) + "\n")


print("Refined legacy triage complete.")
print()

for status in [
    "LEGACY_SAFE",
    "LEGACY_MODERNIZED_MINOR",
    "LEGACY_ENCODING_REVIEW",
    "LEGACY_REAUDIT",
    "LEGACY_UNRESOLVED",
    "NEW_MOVE",
]:
    print(
        f"{status:<26} {counts.get(status, 0)}"
    )

print()
print("Top changes:")

for change, count in change_counts.most_common(12):
    if change != "new_move":
        print(f"  {change:<32} {count}")

print()
print("Wrote:")
print("  tools/stamina/data/legacy_migration_refined_v2.json")
print("  tools/stamina/reports/legacy_migration_refined_v2.md")
