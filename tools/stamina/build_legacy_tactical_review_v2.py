#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path.cwd()

PACKETS = ROOT / "tools/stamina/data/legacy_review_packets_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_tactical_review_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_tactical_review_v2.md"


def load(path):
    return json.loads(path.read_text())


doc = load(PACKETS)

moves = [
    x for x in doc["moves"]
    if x["review"]["family"] == "TACTICAL_SEMANTICS"
]

moves.sort(key=lambda x: x["numeric_id"])

assert len(moves) == 29, f"Expected 29 tactical moves, got {len(moves)}"


out = {
    "schema":
        "firered-reimagined.stamina.legacy-tactical-review.v2",
    "schema_version": 1,
    "count": len(moves),
    "moves": moves,
}

OUT_JSON.write_text(
    json.dumps(out, indent=2) + "\n"
)


lines = [
    "# Stamina V2 — Legacy Review Batch 02",
    "",
    "## Tactical Semantics",
    "",
    f"Moves in batch: **{len(moves)}**",
    "",
    "These moves require human cost review because their tactical "
    "behavior changed in ways not captured by raw power alone.",
    "",
]


for x in moves:
    old = x["legacy"]
    new = x["modern"]
    diff = x["migration_diff"]
    ctx = x["campaign_context"]

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
        f"- V1 rules: "
        + (
            ", ".join(f"`{t}`" for t in old["stamina_rules"])
            or "none"
        ),
        "",
        "### Migration differences",
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
        "Properties:",
        "",
        "```json",
        json.dumps(new["properties"], indent=2),
        "```",
        "",
        "### Campaign context",
        "",
        f"- Gen-9 level-up species: "
        f"**{ctx['active_levelup_species_count']}**",
        f"- Egg species: **{ctx['egg_species_count']}**",
        f"- TM: **{ctx['is_current_tm']}**",
        f"- HM: **{ctx['is_current_hm']}**",
        f"- Explicit FRLG trainer usage: "
        f"**{ctx['explicit_frlg_trainer_move_count']}**",
        "",
        "### Decision",
        "",
        "- Approved V2 cost: `—`",
        "- KEEP / CHANGE: `—`",
        "- Reasoning: `—`",
        "",
        "---",
        "",
    ]


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


print("Tactical review batch complete.")
print("COUNT:", len(moves))
print()

for x in moves:
    d = x["migration_diff"]["details"]

    old_target = d.get("target", {}).get("v1")
    new_target = d.get("target", {}).get("v2")

    old_priority = d.get("priority", {}).get("v1")
    new_priority = d.get("priority", {}).get("v2")

    print(
        f"{x['numeric_id']:>3} "
        f"{x['constant']:<24} "
        f"V1={x['legacy']['cost']} "
        f"target={old_target}->{new_target} "
        f"priority={old_priority}->{new_priority}"
    )

print()
print("Wrote:")
print(" ", OUT_JSON.relative_to(ROOT))
print(" ", OUT_MD.relative_to(ROOT))
