#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

LEGACY_SOURCE = ROOT / "tools/stamina/legacy_v1/moves_source.json"
LEGACY_STAMINA = ROOT / "tools/stamina/legacy_v1/stamina_moves.json"
LEGACY_SPECIAL = ROOT / "tools/stamina/legacy_v1/moves_special_cases.json"
V2_SOURCE = ROOT / "tools/stamina/data/moves_source_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_migration_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_mechanical_diff_v2.md"


def load(path):
    return json.loads(path.read_text())


def normalize_target(value):
    if value is None:
        return None
    return value.replace("MOVE_TARGET_", "TARGET_")


def normalize_category(value):
    if value is None:
        return None

    mapping = {
        "DAMAGE_CATEGORY_PHYSICAL": "physical",
        "DAMAGE_CATEGORY_SPECIAL": "special",
        "DAMAGE_CATEGORY_STATUS": "status",
    }

    return mapping.get(value, value.lower())


def integer_expr(value):
    if value is None:
        return None

    value = str(value).strip()

    try:
        return int(value)
    except ValueError:
        return None


legacy_source_doc = load(LEGACY_SOURCE)
legacy_stamina_doc = load(LEGACY_STAMINA)
legacy_special_doc = load(LEGACY_SPECIAL)
v2_doc = load(V2_SOURCE)

legacy_source = {
    row["id"]: row
    for row in legacy_source_doc["moves"]
}

legacy_stamina = legacy_stamina_doc["moves"]
legacy_special = legacy_special_doc["moves"]

v2_moves = {
    row["constant"]: row
    for row in v2_doc["moves"]
}


rows = []

for constant, old_stamina in legacy_stamina.items():
    old_source_row = legacy_source[constant]
    old = old_source_row["source"]
    new = v2_moves.get(constant)

    if new is None:
        rows.append({
            "constant": constant,
            "numeric_id": old_stamina["numeric_id"],
            "legacy_cost": old_stamina["cost"],
            "status": "LEGACY_REAUDIT",
            "reasons": ["missing_from_v2"],
        })
        continue

    reasons = []
    differences = {}

    # Structural engine entries keep their explicit V1 semantics.
    structural = constant in {
        "MOVE_NONE",
        "MOVE_STRUGGLE",
    }

    # Effect family
    if old["effect"] != new["effect"]:
        reasons.append("effect_changed")
        differences["effect"] = {
            "v1": old["effect"],
            "v2": new["effect"],
        }

    # Power
    new_power = integer_expr(new["power_expr"])

    if new_power is None:
        reasons.append("power_is_config_dependent")
        differences["power"] = {
            "v1": old["power"],
            "v2_expr": new["power_expr"],
        }
    elif old["power"] != new_power:
        reasons.append("power_changed")
        differences["power"] = {
            "v1": old["power"],
            "v2": new_power,
        }

    # Accuracy
    new_accuracy = integer_expr(new["accuracy_expr"])

    if new_accuracy is None:
        reasons.append("accuracy_is_config_dependent")
        differences["accuracy"] = {
            "v1": old["accuracy"],
            "v2_expr": new["accuracy_expr"],
        }
    elif old["accuracy"] != new_accuracy:
        reasons.append("accuracy_changed")
        differences["accuracy"] = {
            "v1": old["accuracy"],
            "v2": new_accuracy,
        }

    # Type
    if old["type"] != new["type_expr"]:
        reasons.append("type_changed")
        differences["type"] = {
            "v1": old["type"],
            "v2": new["type_expr"],
        }

    # Damage category
    old_category = old["gen3_damage_class"]
    new_category = normalize_category(new["category_expr"])

    if (
        old_category not in {"none", None}
        and old_category != new_category
    ):
        reasons.append("damage_category_changed")
        differences["category"] = {
            "v1": old_category,
            "v2": new_category,
        }

    # Target
    old_target = normalize_target(old["target"])
    new_target = new["target_expr"]

    if old_target != new_target:
        reasons.append("target_changed")
        differences["target"] = {
            "v1": old_target,
            "v2": new_target,
        }

    # Priority
    new_priority = integer_expr(new["priority_expr"])

    if new_priority is None:
        reasons.append("priority_is_config_dependent")
        differences["priority"] = {
            "v1": old["priority"],
            "v2_expr": new["priority_expr"],
        }
    elif old["priority"] != new_priority:
        reasons.append("priority_changed")
        differences["priority"] = {
            "v1": old["priority"],
            "v2": new_priority,
        }

    # RHH frequently represents modern move identity through
    # additionalEffects even when the top-level EFFECT_* is generic.
    #
    # This is deliberately conservative. A move with new nested effects
    # must be inspected before inheriting an old cost.
    if new["additional_effects"]:
        reasons.append("v2_additional_effects_present")
        differences["additional_effects"] = new[
            "additional_effects"
        ]

    if structural:
        status = "LEGACY_SAFE"
        reasons = []
        differences = {}
    elif reasons:
        status = "LEGACY_REAUDIT"
    else:
        status = "LEGACY_SAFE"

    rows.append({
        "constant": constant,
        "numeric_id": old_stamina["numeric_id"],
        "name": new["name"],
        "status": status,
        "legacy_cost": old_stamina["cost"],
        "legacy_primary_role": old_stamina["primary_role"],
        "legacy_mechanic_tags": old_stamina["mechanic_tags"],
        "legacy_stamina_rules": old_stamina["stamina_rules"],
        "legacy_review_flags": old_stamina["review_flags"],
        "legacy_design": old_stamina["design"],
        "legacy_campaign_context": old_stamina[
            "campaign_context"
        ],
        "legacy_special_case": legacy_special.get(constant),
        "reasons": reasons,
        "differences": differences,
    })


# Every post-FireRed normal move is genuinely new Stamina work.
for move in v2_doc["moves"]:
    if move["id"] <= 354:
        continue

    rows.append({
        "constant": move["constant"],
        "numeric_id": move["id"],
        "name": move["name"],
        "status": "NEW_MOVE",
        "legacy_cost": None,
        "legacy_primary_role": None,
        "legacy_mechanic_tags": [],
        "legacy_stamina_rules": [],
        "legacy_review_flags": [],
        "legacy_design": None,
        "legacy_campaign_context": None,
        "legacy_special_case": None,
        "reasons": ["not_present_in_fire_red_v1"],
        "differences": {},
    })


rows.sort(key=lambda x: x["numeric_id"])

counts = Counter(row["status"] for row in rows)
reason_counts = Counter()

for row in rows:
    for reason in row["reasons"]:
        reason_counts[reason] += 1


output = {
    "schema": "firered-reimagined.stamina.legacy-migration.v2",
    "schema_version": 1,
    "sources": {
        "legacy_repository_commit":
            "6aba2480ea45223c4582f344b71e41b208b722d4",
        "legacy_authored_dataset":
            "tools/stamina/legacy_v1/stamina_moves.json",
        "v2_source":
            "tools/stamina/data/moves_source_v2.json",
    },
    "policy": {
        "LEGACY_SAFE":
            "Core mechanical identity matched automatically. "
            "V1 cost may be inherited as a V2 candidate, not final balance.",
        "LEGACY_REAUDIT":
            "Mechanical identity changed or requires manual semantic review. "
            "V1 cost is historical reference only.",
        "NEW_MOVE":
            "No FireRed Stamina V1 cost exists.",
    },
    "counts": dict(counts),
    "reason_counts": dict(reason_counts),
    "moves": rows,
}

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_MD.parent.mkdir(parents=True, exist_ok=True)

OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


safe = [
    row for row in rows
    if row["status"] == "LEGACY_SAFE"
]

reaudit = [
    row for row in rows
    if row["status"] == "LEGACY_REAUDIT"
]

new_moves = [
    row for row in rows
    if row["status"] == "NEW_MOVE"
]


lines = [
    "# Stamina V2 — Legacy Mechanical Diff",
    "",
    "## Summary",
    "",
    f"- Legacy safe: **{len(safe)}**",
    f"- Legacy re-audit: **{len(reaudit)}**",
    f"- New moves: **{len(new_moves)}**",
    f"- Total normal move records: **{len(rows)}**",
    "",
    "## Re-audit reason counts",
    "",
]

for reason, count in reason_counts.most_common():
    if reason == "not_present_in_fire_red_v1":
        continue
    lines.append(f"- `{reason}`: **{count}**")


lines += [
    "",
    "## Legacy moves requiring re-audit",
    "",
]

for row in reaudit:
    lines.append(
        f"### {row['constant']} — old cost {row['legacy_cost']}"
    )
    lines.append("")

    for reason in row["reasons"]:
        lines.append(f"- `{reason}`")

    if row.get("differences"):
        lines.append("")
        lines.append("```json")
        lines.append(
            json.dumps(
                row.get("differences", {}),
                indent=2,
            )
        )
        lines.append("```")

    lines.append("")


lines += [
    "## Legacy-safe moves",
    "",
]

for row in safe:
    lines.append(
        f"- `{row['constant']}` — candidate cost "
        f"**{row['legacy_cost']}**"
    )


lines += [
    "",
    "## New moves",
    "",
]

for row in new_moves:
    lines.append(
        f"- `{row['constant']}` — {row['name']}"
    )


OUT_MD.write_text("\n".join(lines) + "\n")

print("Legacy → V2 migration diff complete.")
print()
print(f"LEGACY_SAFE    : {len(safe)}")
print(f"LEGACY_REAUDIT : {len(reaudit)}")
print(f"NEW_MOVE       : {len(new_moves)}")
print(f"TOTAL          : {len(rows)}")
print()
print("Top re-audit reasons:")

for reason, count in reason_counts.most_common(12):
    if reason != "not_present_in_fire_red_v1":
        print(f"  {reason:32} {count}")

print()
print("Wrote:")
print("  tools/stamina/data/legacy_migration_v2.json")
print("  tools/stamina/reports/legacy_mechanical_diff_v2.md")
