#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path.cwd()

QUEUE = ROOT / "tools/stamina/data/legacy_review_queue_v2.json"
CONTEXT = ROOT / "tools/stamina/data/move_context_v2.json"
V2_SOURCE = ROOT / "tools/stamina/data/moves_source_v2.json"

V1_FINAL = ROOT / "tools/stamina/legacy_v1/stamina_moves.json"
V1_SOURCE = ROOT / "tools/stamina/legacy_v1/moves_source.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_review_packets_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_review_mechanic_modernization_v2.md"


def load(path):
    return json.loads(path.read_text())


queue_doc = load(QUEUE)
context_doc = load(CONTEXT)
v2_source_doc = load(V2_SOURCE)

v1_final_doc = load(V1_FINAL)
v1_source_doc = load(V1_SOURCE)


context_by_name = {
    x["constant"]: x
    for x in context_doc["moves"]
}

v2_by_name = {
    x["constant"]: x
    for x in v2_source_doc["moves"]
}

v1_final = v1_final_doc["moves"]

v1_source = {
    x["id"]: x
    for x in v1_source_doc["moves"]
}


packets = []


for q in queue_doc["moves"]:
    if q["final_status"] not in {
        "REVIEW_REQUIRED",
        "REVIEW_WATCHLIST",
    }:
        continue

    name = q["v2_constant"]
    legacy_name = q["legacy_constant"]

    ctx = context_by_name[name]
    new = v2_by_name[name]
    old_final = v1_final[legacy_name]
    old_source = v1_source[legacy_name]

    packet = {
        "numeric_id": q["numeric_id"],
        "constant": name,
        "name": q["name"],

        "review": {
            "status": q["final_status"],
            "family": q["review_family"],
            "reason": q["review_reason"],
        },

        "legacy": {
            "cost": q["legacy_cost"],
            "primary_role": q["legacy_primary_role"],
            "mechanic_tags": q["legacy_mechanic_tags"],
            "stamina_rules": q["legacy_stamina_rules"],

            "design": old_final.get("design", {}),

            "source": old_source.get("source", {}),
        },

        "modern": {
            "effect": new["effect"],
            "power_expr": new["power_expr"],
            "type_expr": new["type_expr"],
            "accuracy_expr": new["accuracy_expr"],
            "pp_expr": new["pp_expr"],
            "target_expr": new["target_expr"],
            "priority_expr": new["priority_expr"],
            "category_expr": new["category_expr"],
            "additional_effects":
                new.get("additional_effects", []),
            "properties":
                new.get("properties", {}),
        },

        "migration_diff": {
            "changes": q["changes"],
            "details": q["details"],
            "encoding_resolution":
                q.get("encoding_resolution"),
            "manual_encoding_decision":
                q.get("manual_encoding_decision"),
        },

        "campaign_context": {
            "any_supported_game_species_count":
                ctx["learnability"][
                    "any_supported_game_species_count"
                ],

            "active_levelup_generation":
                ctx["learnability"][
                    "active_levelup_generation"
                ],

            "active_levelup_species_count":
                ctx["learnability"][
                    "active_levelup_species_count"
                ],

            "active_levelup_occurrences":
                ctx["learnability"][
                    "active_levelup_occurrences"
                ],

            "active_levelup_species":
                ctx["learnability"][
                    "active_levelup_species"
                ],

            "egg_species_count":
                ctx["learnability"][
                    "egg_species_count"
                ],

            "egg_species":
                ctx["learnability"][
                    "egg_species"
                ],

            "is_current_tm":
                ctx["learnability"]["is_current_tm"],

            "is_current_hm":
                ctx["learnability"]["is_current_hm"],

            "explicit_frlg_trainer_move_count":
                ctx["campaign_context"][
                    "explicit_frlg_trainer_move_count"
                ],
        },

        # Human-authored fields.
        # These stay null until reviewed.
        "decision": {
            "status": "PENDING",
            "approved_cost": None,
            "cost_change": None,
            "reasoning": [],
            "review_notes": "",
        },
    }

    packets.append(packet)


# Review order:
#   1. mechanic modernization
#   2. tactical semantics
#   3. major numeric profile
#   4. mechanic identity
#   5. watchlist
family_order = {
    "MECHANIC_MODERNIZATION": 0,
    "TACTICAL_SEMANTICS": 1,
    "MAJOR_NUMERIC_PROFILE": 2,
    "MECHANIC_IDENTITY": 3,
    None: 4,
}

packets.sort(
    key=lambda x: (
        1 if x["review"]["status"] == "REVIEW_WATCHLIST" else 0,
        family_order.get(x["review"]["family"], 9),
        x["numeric_id"],
    )
)


output = {
    "schema":
        "firered-reimagined.stamina.legacy-review-packets.v2",
    "schema_version": 1,

    "rules": {
        "purpose":
            "Human Stamina V2 cost reassessment for legacy moves.",

        "legacy_cost_policy":
            "The V1 cost is a historical candidate, not a default "
            "answer for moves in this dataset.",

        "campaign_context_warning":
            "explicit_frlg_trainer_move_count includes only moves "
            "explicitly authored in trainer data; trainer Pokémon "
            "whose moves are derived at runtime are not reconstructed "
            "in this field.",

        "decision_values": [
            "KEEP",
            "CHANGE",
        ],

        "allowed_costs": [
            0, 1, 2, 3, 4, 5, 6
        ],
    },

    "summary": {
        "packet_count": len(packets),
        "required_count": sum(
            1 for x in packets
            if x["review"]["status"] == "REVIEW_REQUIRED"
        ),
        "watchlist_count": sum(
            1 for x in packets
            if x["review"]["status"] == "REVIEW_WATCHLIST"
        ),
    },

    "moves": packets,
}

OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


# ------------------------------------------------------------
# First human-review batch: mechanic modernization
# ------------------------------------------------------------

batch = [
    x for x in packets
    if x["review"]["family"] == "MECHANIC_MODERNIZATION"
]


lines = [
    "# Stamina V2 — Legacy Review Batch 01",
    "",
    "## Mechanic Modernization",
    "",
    f"Moves in batch: **{len(batch)}**",
    "",
    "This batch contains legacy moves where modern mechanics changed "
    "qualitatively. V1 costs are historical references only.",
    "",
]


for x in batch:
    old = x["legacy"]
    new = x["modern"]
    ctx = x["campaign_context"]
    diff = x["migration_diff"]

    lines += [
        f"## {x['constant']} — {x['name']}",
        "",
        f"- V1 cost: **{old['cost']}**",
        f"- V1 role: `{old['primary_role']}`",
        f"- V1 tags: "
        + (
            ", ".join(f"`{t}`" for t in old["mechanic_tags"])
            or "none"
        ),
        "",
        "### Migration difference",
        "",
    ]

    for change in diff["changes"]:
        lines.append(f"- `{change}`")

    lines += [
        "",
        "```json",
        json.dumps(diff["details"], indent=2),
        "```",
        "",
        "### Current mechanics",
        "",
        f"- Effect: `{new['effect']}`",
        f"- Power: `{new['power_expr']}`",
        f"- Accuracy: `{new['accuracy_expr']}`",
        f"- Type: `{new['type_expr']}`",
        f"- Category: `{new['category_expr']}`",
        f"- Target: `{new['target_expr']}`",
        f"- Priority: `{new['priority_expr']}`",
        "",
        "Additional effects:",
        "",
        "```json",
        json.dumps(new["additional_effects"], indent=2),
        "```",
        "",
        "Relevant properties:",
        "",
        "```json",
        json.dumps(new["properties"], indent=2),
        "```",
        "",
        "### Campaign context",
        "",
        f"- Active Gen-9 level-up species: "
        f"**{ctx['active_levelup_species_count']}**",
        f"- Egg species: **{ctx['egg_species_count']}**",
        f"- Current TM: **{ctx['is_current_tm']}**",
        f"- Current HM: **{ctx['is_current_hm']}**",
        f"- Explicit FRLG trainer usage: "
        f"**{ctx['explicit_frlg_trainer_move_count']}**",
        "",
        "### Human decision",
        "",
        "- Decision: `PENDING`",
        "- Approved V2 cost: `—`",
        "- Reasoning: `—`",
        "",
        "---",
        "",
    ]


OUT_MD.write_text("\n".join(lines) + "\n")


print("Legacy review packets complete.")
print()
print(f"TOTAL PACKETS : {len(packets)}")
print(
    "REQUIRED      :",
    output["summary"]["required_count"],
)
print(
    "WATCHLIST     :",
    output["summary"]["watchlist_count"],
)
print(f"BATCH 01      : {len(batch)}")
print()
print("Wrote:")
print("  tools/stamina/data/legacy_review_packets_v2.json")
print(
    "  tools/stamina/reports/"
    "legacy_review_mechanic_modernization_v2.md"
)
