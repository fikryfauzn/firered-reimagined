#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

SOURCE = (
    ROOT
    / "tools/stamina/data/new_move_candidate_bands_v2.json"
)

OUT_JSON = (
    ROOT
    / "tools/stamina/data/new_move_review_queue_v2.json"
)

OUT_MD = (
    ROOT
    / "tools/stamina/reports/new_move_review_queue_v2.md"
)


def load(path):
    if not path.exists():
        raise SystemExit(
            f"Missing input: {path}"
        )

    return json.loads(
        path.read_text()
    )


doc = load(SOURCE)
moves = doc["moves"]

assert len(moves) == 493


# ============================================================
# Review priority
# ============================================================

CRITICAL_FAMILIES = {
    "revival_support",
    "sacrifice_support",
    "sacrifice_damage",
    "special_damage_formula",
    "conditional_damage",
    "called_or_copied",
    "forced_multiturn",
    "recharge_damage",
    "two_turn",
    "multi_hit_damage",
    "counter_damage",
    "pivot_support",
    "reposition",
}

HIGH_VALUE_FAMILIES = {
    "protection",
    "priority_damage",
    "redirection",
    "hazard",
    "hazard_control",
    "ability_control",
    "stat_control",
    "ally_support",
    "terrain",
    "weather",
    "item_control",
    "status_removal_damage",
    "pp_control_damage",
    "heal_block_damage",
}


def priority_score(row):
    score = 0

    status = row["review_status"]
    family = row["primary_family"]

    band = row["candidate_band"]

    width = (
        band["max"]
        - band["min"]
    )

    reasons = set(
        row["review_reasons"]
    )

    if status == "REVIEW_REQUIRED":
        score += 1000

    elif status == "REVIEW_WATCHLIST":
        score += 500

    if family in CRITICAL_FAMILIES:
        score += 300

    elif family in HIGH_VALUE_FAMILIES:
        score += 150

    if row["confidence"] == "LOW":
        score += 120

    elif row["confidence"] == "MEDIUM":
        score += 50

    score += width * 30

    if (
        "SEVERE_ANCHOR_DISAGREEMENT"
        in reasons
    ):
        score += 100

    if (
        "NO_USEFUL_LEGACY_FAMILY_ANCHOR"
        in reasons
    ):
        score += 80

    if (
        "MECHANIC_FAMILY_REQUIRES_REVIEW"
        in reasons
    ):
        score += 70

    if (
        "EXTREME_BASE_POWER"
        in reasons
    ):
        score += 40

    if (
        "GUARANTEED_CRITICAL_HIT"
        in reasons
    ):
        score += 40

    if (
        "HIGH_FIXED_STRIKE_COUNT"
        in reasons
    ):
        score += 40

    return score


# ============================================================
# Tier assignment
# ============================================================

queue = []

for row in moves:
    status = row["review_status"]

    if status == "REVIEW_REQUIRED":
        tier = "A"

    elif status == "REVIEW_WATCHLIST":
        tier = "B"

    else:
        tier = "C"

    item = dict(row)

    item["review_tier"] = tier
    item["review_priority_score"] = (
        priority_score(row)
    )

    item["human_decision"] = {
        "status": "PENDING",
        "approved_cost": None,
        "decision": None,
        "notes": None,
    }

    queue.append(item)


queue.sort(
    key=lambda x: (
        x["review_tier"],
        -x["review_priority_score"],
        x["numeric_id"],
    )
)


# ============================================================
# Sequential review numbers
# ============================================================

for i, row in enumerate(
    queue,
    start=1,
):
    row["review_index"] = i


# ============================================================
# Validation
# ============================================================

assert len(queue) == 493

assert {
    x["numeric_id"]
    for x in queue
} == set(range(355, 848))

assert all(
    x["human_decision"]["status"]
    == "PENDING"
    for x in queue
)


tier_counts = Counter(
    x["review_tier"]
    for x in queue
)

family_counts_a = Counter(
    x["primary_family"]
    for x in queue
    if x["review_tier"] == "A"
)


# ============================================================
# JSON
# ============================================================

output = {
    "schema":
        "firered-reimagined.stamina.new-move-review-queue.v2",

    "schema_version":
        1,

    "status":
        "HUMAN_REVIEW_PENDING",

    "source":
        str(
            SOURCE.relative_to(ROOT)
        ),

    "summary": {
        "move_count":
            len(queue),

        "tier_counts":
            dict(tier_counts),

        "tier_a_family_counts":
            dict(
                family_counts_a.most_common()
            ),
    },

    "moves":
        queue,
}

OUT_JSON.write_text(
    json.dumps(
        output,
        indent=2,
    )
    + "\n"
)


# ============================================================
# Markdown review packet
# ============================================================

lines = [
    "# Stamina V2 — Expansion Move Review Queue",
    "",
    "Status: **HUMAN REVIEW PENDING**",
    "",
    "## Tiers",
    "",
    "- **A** — explicit mechanical/design review required",
    "- **B** — watchlist / ambiguous evidence",
    "- **C** — narrow candidate suitable for later batch confirmation",
    "",
]

for tier in (
    "A",
    "B",
    "C",
):
    members = [
        x for x in queue
        if x["review_tier"] == tier
    ]

    lines += [
        "",
        f"## Tier {tier}",
        "",
        f"Moves: **{len(members)}**",
        "",
    ]

    for x in members:
        band = x[
            "candidate_band"
        ]

        anchors = ", ".join(
            f"{a['constant']}={a['cost']}"
            for a in
            x[
                "anchor_evidence"
            ]["top_anchors"]
        )

        reasons = ", ".join(
            x["review_reasons"]
        ) or "-"

        lines.append(
            f"### {x['review_index']:03d}. "
            f"{x['constant']}"
        )

        lines.append("")

        lines.append(
            f"- Family: "
            f"`{x['primary_family']}`"
        )

        lines.append(
            f"- Candidate: "
            f"**{band['min']}–{band['max']}**, "
            f"center **{band['center']}**"
        )

        lines.append(
            f"- Confidence: "
            f"`{x['confidence']}`"
        )

        lines.append(
            f"- Priority score: "
            f"`{x['review_priority_score']}`"
        )

        lines.append(
            f"- Anchors: {anchors}"
        )

        lines.append(
            f"- Reasons: {reasons}"
        )

        lines.append(
            "- Human decision: **PENDING**"
        )

        lines.append("")


OUT_MD.write_text(
    "\n".join(lines)
    + "\n"
)


# ============================================================
# Console
# ============================================================

print(
    "New-move human review queue built."
)

print()

print(
    "MOVES:",
    len(queue),
)

print("\nTiers:")

for tier in (
    "A",
    "B",
    "C",
):
    print(
        f"  Tier {tier}: "
        f"{tier_counts[tier]}"
    )


print("\nTier A families:")

for family, count in (
    family_counts_a.most_common()
):
    print(
        f"  {family:<26} "
        f"{count}"
    )


print("\nFirst 30 review items:")

for x in queue[:30]:
    b = x["candidate_band"]

    print(
        f"  {x['review_index']:03d} "
        f"{x['constant']:<30} "
        f"{x['primary_family']:<24} "
        f"[{b['min']}-{b['max']}] "
        f"C={b['center']} "
        f"score={x['review_priority_score']}"
    )


print()

print("Wrote:")
print(
    " ",
    OUT_JSON.relative_to(ROOT),
)
print(
    " ",
    OUT_MD.relative_to(ROOT),
)
