#!/usr/bin/env python3

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()

SEMANTICS = ROOT / "tools/stamina/data/new_move_semantics_v2d.json"

OUT_JSON = ROOT / "tools/stamina/data/new_move_candidate_bands_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/new_move_candidate_bands_v2.md"


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")

    return json.loads(path.read_text())


doc = load(SEMANTICS)
moves = doc["moves"]

assert len(moves) == 493


def truthy(value):
    if value is True:
        return True

    if isinstance(value, str):
        return value.upper() == "TRUE"

    return False


def round_half_up(value):
    return int(math.floor(value + 0.5))


def weighted_center(anchors):
    if not anchors:
        return None

    weighted = 0.0
    total = 0.0

    for a in anchors[:3]:
        # Similarity score is evidence strength.
        weight = max(float(a["score"]), 0.01)

        weighted += a["cost"] * weight
        total += weight

    if total == 0:
        return None

    result = round_half_up(
        weighted / total
    )

    return max(0, min(6, result))


# ----------------------------------------------------------------------
# Families that require explicit human attention even when their
# legacy anchors agree.
#
# These contain mechanics where "similar BP" is not enough to reason
# about Stamina value.
# ----------------------------------------------------------------------

MANDATORY_REVIEW_FAMILIES = {
    "special_damage_formula",
    "conditional_damage",
    "multi_hit_damage",
    "recharge_damage",
    "two_turn",
    "forced_multiturn",
    "sacrifice_damage",
    "counter_damage",
    "called_or_copied",
    "utility_status",
    "noncombat_utility",
    "pp_control_damage",
    "heal_block_damage",
    "status_removal_damage",
    "pivot_support",
    "reposition",
    "sacrifice_support",
    "revival_support",
}


# ----------------------------------------------------------------------
# Produce candidate evidence
# ----------------------------------------------------------------------

rows = []


for move in moves:
    family = move["primary_family"]

    evidence = move[
        "legacy_anchor_evidence"
    ]

    anchors = evidence[
        "top_anchors"
    ]

    top3 = anchors[:3]

    anchor_lo = evidence["cost_min"]
    anchor_hi = evidence["cost_max"]

    if anchor_lo is None or anchor_hi is None:
        raise SystemExit(
            f"No anchor range: {move['constant']}"
        )

    anchor_span = anchor_hi - anchor_lo

    scope = evidence["scope"]

    center = weighted_center(top3)

    if center is None:
        raise SystemExit(
            f"No center: {move['constant']}"
        )

    # ------------------------------------------------------------------
    # Candidate band
    #
    # SAME_FAMILY:
    #   preserve actual anchor range.
    #
    # RELATED/GLOBAL:
    #   widen by one tier because those anchors provide weaker evidence.
    # ------------------------------------------------------------------

    band_lo = anchor_lo
    band_hi = anchor_hi

    if scope in {
        "RELATED_FAMILY",
        "SAME_PLUS_RELATED",
        "GLOBAL_FALLBACK",
    }:
        band_lo = max(
            0,
            band_lo - 1,
        )

        band_hi = min(
            6,
            band_hi + 1,
        )

    # Center must always lie inside candidate band.
    band_lo = min(
        band_lo,
        center,
    )

    band_hi = max(
        band_hi,
        center,
    )

    # ------------------------------------------------------------------
    # Review reasons
    # ------------------------------------------------------------------

    reasons = []

    if scope == "GLOBAL_FALLBACK":
        reasons.append(
            "NO_USEFUL_LEGACY_FAMILY_ANCHOR"
        )

    elif scope == "RELATED_FAMILY":
        reasons.append(
            "RELATED_FAMILY_ANCHORS_ONLY"
        )

    elif scope == "SAME_PLUS_RELATED":
        reasons.append(
            "SPARSE_SAME_FAMILY_ANCHORS"
        )

    same_family_count = evidence[
        "same_family_anchor_count"
    ]

    if same_family_count < 3:
        reasons.append(
            "FEWER_THAN_3_SAME_FAMILY_ANCHORS"
        )

    if anchor_span >= 3:
        reasons.append(
            "SEVERE_ANCHOR_DISAGREEMENT"
        )

    elif anchor_span == 2:
        reasons.append(
            "MODERATE_ANCHOR_DISAGREEMENT"
        )

    if family in MANDATORY_REVIEW_FAMILIES:
        reasons.append(
            "MECHANIC_FAMILY_REQUIRES_REVIEW"
        )

    resolved = move[
        "resolved_mechanics"
    ]

    power = resolved["power"]
    accuracy = resolved["accuracy"]
    priority = resolved["priority"]

    mechanics = move["mechanics"]
    props = mechanics.get(
        "properties",
        {},
    ) or {}

    tags = set(
        move.get(
            "semantic_tags",
            [],
        )
    )

    # ------------------------------------------------------------------
    # Mechanical watch flags
    # ------------------------------------------------------------------

    if (
        isinstance(power, (int, float))
        and power >= 140
    ):
        reasons.append(
            "EXTREME_BASE_POWER"
        )

    if (
        isinstance(priority, (int, float))
        and priority >= 2
    ):
        reasons.append(
            "HIGH_POSITIVE_PRIORITY"
        )

    if (
        accuracy == 0
        and "damaging_move" in tags
    ):
        reasons.append(
            "DAMAGE_WITH_NO_NORMAL_ACCURACY_CHECK"
        )

    if "multi_target" in tags:
        reasons.append(
            "MULTI_TARGET_VALUE"
        )

    strike_count = props.get(
        "strikeCount"
    )

    try:
        strike_count_int = (
            int(strike_count)
            if strike_count is not None
            else None
        )
    except (TypeError, ValueError):
        strike_count_int = None

    if (
        strike_count_int is not None
        and strike_count_int >= 3
    ):
        reasons.append(
            "HIGH_FIXED_STRIKE_COUNT"
        )

    if truthy(
        props.get("alwaysCriticalHit")
    ):
        reasons.append(
            "GUARANTEED_CRITICAL_HIT"
        )

    if (
        truthy(props.get("ignoresProtect"))
        and "damaging_move" in tags
    ):
        reasons.append(
            "IGNORES_PROTECT"
        )

    # A direct-damage classification with a custom primary effect
    # deserves inspection even if it is otherwise mechanically simple.
    if (
        family == "direct_damage"
        and mechanics["effect"]
            != "EFFECT_HIT"
    ):
        reasons.append(
            "CUSTOM_DAMAGE_EFFECT"
        )

    # Deduplicate while preserving order.
    reasons = list(dict.fromkeys(reasons))

    # ------------------------------------------------------------------
    # Confidence
    #
    # Confidence describes how useful the candidate band is.
    # It does NOT mean the move is approved.
    # ------------------------------------------------------------------

    severe = (
        scope == "GLOBAL_FALLBACK"
        or anchor_span >= 3
    )

    moderate = (
        scope in {
            "RELATED_FAMILY",
            "SAME_PLUS_RELATED",
        }
        or anchor_span == 2
        or family
            in MANDATORY_REVIEW_FAMILIES
    )

    if severe:
        confidence = "LOW"

    elif moderate:
        confidence = "MEDIUM"

    else:
        confidence = "HIGH"

    # ------------------------------------------------------------------
    # Review status
    # ------------------------------------------------------------------

    required_reason_names = {
        "NO_USEFUL_LEGACY_FAMILY_ANCHOR",
        "SEVERE_ANCHOR_DISAGREEMENT",
        "MECHANIC_FAMILY_REQUIRES_REVIEW",
        "EXTREME_BASE_POWER",
        "HIGH_POSITIVE_PRIORITY",
        "HIGH_FIXED_STRIKE_COUNT",
        "GUARANTEED_CRITICAL_HIT",
    }

    if any(
        r in required_reason_names
        for r in reasons
    ):
        review_status = "REVIEW_REQUIRED"

    elif reasons:
        review_status = "REVIEW_WATCHLIST"

    else:
        review_status = "NARROW_CANDIDATE"

    row = {
        "numeric_id":
            move["numeric_id"],

        "constant":
            move["constant"],

        "name":
            move["name"],

        "primary_family":
            family,

        "candidate_band": {
            "min": band_lo,
            "max": band_hi,
            "center": center,
        },

        "confidence":
            confidence,

        "review_status":
            review_status,

        "review_reasons":
            reasons,

        "anchor_evidence": {
            "scope":
                scope,

            "same_family_anchor_count":
                same_family_count,

            "raw_anchor_min":
                anchor_lo,

            "raw_anchor_max":
                anchor_hi,

            "raw_anchor_span":
                anchor_span,

            "top_anchors":
                top3,
        },

        "mechanical_summary": {
            "power":
                power,

            "accuracy":
                accuracy,

            "priority":
                priority,

            "effect":
                mechanics["effect"],

            "target":
                mechanics["target_expr"],

            "category":
                mechanics["category_expr"],

            "semantic_tags":
                move["semantic_tags"],

            "additional_semantics":
                move[
                    "additional_semantics"
                ],
        },

        "campaign_context":
            move["campaign_context"],

        "approval_status":
            "UNAPPROVED",
    }

    rows.append(row)


rows.sort(
    key=lambda x: x["numeric_id"]
)


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

assert len(rows) == 493

assert [
    x["numeric_id"]
    for x in rows
] == list(range(355, 848))

for x in rows:
    b = x["candidate_band"]

    assert 0 <= b["min"] <= 6
    assert 0 <= b["max"] <= 6
    assert 0 <= b["center"] <= 6

    assert (
        b["min"]
        <= b["center"]
        <= b["max"]
    )

    assert (
        x["approval_status"]
        == "UNAPPROVED"
    )


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------

status_counts = Counter(
    x["review_status"]
    for x in rows
)

confidence_counts = Counter(
    x["confidence"]
    for x in rows
)

center_counts = Counter(
    x["candidate_band"]["center"]
    for x in rows
)

width_counts = Counter(
    x["candidate_band"]["max"]
    -
    x["candidate_band"]["min"]
    for x in rows
)

reason_counts = Counter()

for x in rows:
    reason_counts.update(
        x["review_reasons"]
    )


# ----------------------------------------------------------------------
# Output JSON
# ----------------------------------------------------------------------

output = {
    "schema":
        "firered-reimagined.stamina.new-move-candidate-bands.v2",

    "schema_version":
        1,

    "status":
        "CANDIDATES_ONLY",

    "warning":
        "Candidate bands and centers are review aids only. "
        "No Expansion-only move has an approved Stamina cost.",

    "summary": {
        "move_count":
            len(rows),

        "review_status_counts":
            dict(status_counts),

        "confidence_counts":
            dict(confidence_counts),

        "candidate_center_distribution":
            dict(
                sorted(
                    center_counts.items()
                )
            ),

        "band_width_distribution":
            dict(
                sorted(
                    width_counts.items()
                )
            ),

        "review_reason_counts":
            dict(
                reason_counts.most_common()
            ),
    },

    "moves":
        rows,
}


OUT_JSON.write_text(
    json.dumps(
        output,
        indent=2,
    ) + "\n"
)


# ----------------------------------------------------------------------
# Human-readable report
# ----------------------------------------------------------------------

lines = [
    "# Stamina V2 — New Move Candidate Bands",
    "",
    "Status: **CANDIDATES ONLY — UNAPPROVED**",
    "",
    f"- Moves: **{len(rows)}**",
    "",
    "## Review status",
    "",
]

for status, count in status_counts.most_common():
    lines.append(
        f"- `{status}`: **{count}**"
    )


lines += [
    "",
    "## Confidence",
    "",
]

for confidence, count in confidence_counts.most_common():
    lines.append(
        f"- `{confidence}`: **{count}**"
    )


lines += [
    "",
    "## Candidate centers",
    "",
]

for cost, count in sorted(
    center_counts.items()
):
    lines.append(
        f"- Cost {cost}: **{count}**"
    )


lines += [
    "",
    "## Review reasons",
    "",
]

for reason, count in reason_counts.most_common():
    lines.append(
        f"- `{reason}`: **{count}**"
    )


for status in (
    "REVIEW_REQUIRED",
    "REVIEW_WATCHLIST",
    "NARROW_CANDIDATE",
):
    members = [
        x for x in rows
        if x["review_status"]
           == status
    ]

    lines += [
        "",
        f"## {status}",
        "",
    ]

    for x in members:
        b = x["candidate_band"]

        anchors = ", ".join(
            f"{a['constant']}:{a['cost']}"
            for a in
            x["anchor_evidence"][
                "top_anchors"
            ]
        )

        reasons = ", ".join(
            x["review_reasons"]
        ) or "-"

        lines.append(
            f"- `{x['constant']}` "
            f"[{b['min']}-{b['max']}] "
            f"center={b['center']} "
            f"confidence={x['confidence']} "
            f"family={x['primary_family']} "
            f"anchors={anchors} "
            f"reasons={reasons}"
        )


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


# ----------------------------------------------------------------------
# Console summary
# ----------------------------------------------------------------------

print("New-move candidate-band generation complete.")
print()
print("MOVES:", len(rows))

print("\nReview status:")
for status, count in status_counts.most_common():
    print(
        f"  {status:<18} {count}"
    )

print("\nConfidence:")
for confidence, count in confidence_counts.most_common():
    print(
        f"  {confidence:<8} {count}"
    )

print("\nCandidate centers:")
for cost, count in sorted(center_counts.items()):
    print(
        f"  cost {cost}: {count}"
    )

print("\nBand widths:")
for width, count in sorted(width_counts.items()):
    print(
        f"  width {width}: {count}"
    )

print("\nTop review reasons:")
for reason, count in reason_counts.most_common(15):
    print(
        f"  {reason:<38} {count}"
    )

print()
print("Wrote:")
print(" ", OUT_JSON.relative_to(ROOT))
print(" ", OUT_MD.relative_to(ROOT))
