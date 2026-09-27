#!/usr/bin/env python3

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()

SOURCE = ROOT / "tools/stamina/data/moves_source_v2.json"
CONTEXT = ROOT / "tools/stamina/data/move_context_v2.json"
LEGACY = ROOT / "tools/stamina/data/legacy_costs_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/new_move_semantics_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/new_move_semantics_v2.md"


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")

    return json.loads(path.read_text())


source_doc = load(SOURCE)
context_doc = load(CONTEXT)
legacy_doc = load(LEGACY)

all_moves = source_doc["moves"]

source_by_name = {
    x["constant"]: x
    for x in all_moves
}

context_by_name = {
    x["constant"]: x
    for x in context_doc["moves"]
}

legacy_cost_by_name = {
    x["constant"]: x
    for x in legacy_doc["moves"]
}


# ----------------------------------------------------------------------
# Basic expression helpers
# ----------------------------------------------------------------------

def literal_int(value):
    if isinstance(value, int):
        return value

    if isinstance(value, str):
        s = value.strip()

        if re.fullmatch(r"-?\d+", s):
            return int(s)

    return None


def json_blob(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).upper()


# ----------------------------------------------------------------------
# Mechanical semantic tags
# ----------------------------------------------------------------------

def semantic_tags(move):
    tags = set()

    effect = str(move.get("effect", "")).upper()
    category = str(move.get("category_expr", "")).upper()
    target = str(move.get("target_expr", "")).upper()

    properties = move.get("properties", {}) or {}
    additional = move.get("additional_effects", []) or []

    blob = " ".join([
        effect,
        json_blob(properties),
        json_blob(additional),
    ])

    power = literal_int(move.get("power_expr"))
    priority = literal_int(move.get("priority_expr"))

    # --------------------------------------------------------------
    # Basic damage / status identity
    # --------------------------------------------------------------

    if category == "DAMAGE_CATEGORY_STATUS":
        tags.add("status_move")
    else:
        tags.add("damaging_move")

    if (
        power is not None
        and power > 0
        and category != "DAMAGE_CATEGORY_STATUS"
    ):
        tags.add("direct_damage")

    # --------------------------------------------------------------
    # Damage mechanics
    # --------------------------------------------------------------

    if "ABSORB" in blob or "DRAIN" in effect:
        tags.add("drain")

    if "RECOIL" in effect or "RECOIL" in blob:
        tags.add("recoil")

    if (
        "WRAP" in blob
        or "BIND" in effect
        or "TRAP" in effect
    ):
        tags.add("trapping")

    if (
        properties.get("multiHit") is True
        or "STRIKECOUNT" in blob
        or "MULTIHIT" in blob
    ):
        tags.add("multi_hit")

    if (
        properties.get("twoTurnAttack")
        or "TWO_TURNS" in effect
        or "SEMI_INVULNERABLE" in effect
    ):
        tags.add("two_turn")

    if any(x in blob for x in (
        "THRASH",
        "UPROAR",
        "ROLLOUT",
        "RAMPAGE",
    )):
        tags.add("forced_multiturn")

    if "FUTURE_SIGHT" in effect:
        tags.add("delayed_damage")

    if any(x in effect for x in (
        "LEVEL_DAMAGE",
        "FIXED_DAMAGE",
        "PSYWAVE",
        "ENDEAVOR",
        "SUPER_FANG",
        "FINAL_GAMBIT",
    )):
        tags.add("special_damage_formula")

    if "OHKO" in effect:
        tags.add("ohko")

    # --------------------------------------------------------------
    # Priority
    # --------------------------------------------------------------

    if priority is not None:
        if priority > 0:
            tags.add("positive_priority")
        elif priority < 0:
            tags.add("negative_priority")

    if priority is not None and priority > 0 and "damaging_move" in tags:
        tags.add("priority_damage")

    # --------------------------------------------------------------
    # Stat manipulation
    # --------------------------------------------------------------

    if any(x in blob for x in (
        "STAT_PLUS",
        "STAT_MINUS",
        "STAT_CHANGE",
    )):
        tags.add("stat_change")

    if (
        "STAT_PLUS" in blob
        and (
            '"SELF":"TRUE"' in blob
            or '"SELF":TRUE' in blob
            or target == "TARGET_USER"
        )
    ):
        tags.add("setup")

    if "STAT_MINUS" in blob:
        tags.add("debuff")

    # --------------------------------------------------------------
    # Status effects
    # --------------------------------------------------------------

    if any(x in blob for x in (
        "SLEEP",
        "POISON",
        "TOXIC",
        "PARALYSIS",
        "BURN",
        "FREEZE",
        "FROSTBITE",
        "CONFUSION",
    )):
        tags.add("status_control")

    if "FLINCH" in blob:
        tags.add("flinch")

    # --------------------------------------------------------------
    # Healing / protection
    # --------------------------------------------------------------

    if (
        properties.get("healingMove") is True
        or any(x in effect for x in (
            "RESTORE_HP",
            "SOFTBOILED",
            "MOONLIGHT",
            "MORNING_SUN",
            "SYNTHESIS",
            "ROOST",
            "HEAL_ORDER",
            "SHORE_UP",
            "LIFE_DEW",
        ))
    ):
        tags.add("healing")

    if any(x in effect for x in (
        "PROTECT",
        "ENDURE",
        "KING_SHIELD",
        "SPIKY_SHIELD",
        "BANEFUL_BUNKER",
        "SILK_TRAP",
        "BURNING_BULWARK",
    )):
        tags.add("protection")

    # --------------------------------------------------------------
    # Battle-field / support systems
    # --------------------------------------------------------------

    if "WEATHER" in effect:
        tags.add("weather")

    if any(x in effect for x in (
        "REFLECT",
        "LIGHT_SCREEN",
        "AURORA_VEIL",
        "SAFEGUARD",
        "MIST",
        "TAILWIND",
        "TRICK_ROOM",
        "WONDER_ROOM",
        "MAGIC_ROOM",
        "GRAVITY",
        "TERRAIN",
    )):
        tags.add("field_control")

    if any(x in blob for x in (
        "SPIKES",
        "STEALTH_ROCK",
        "TOXIC_SPIKES",
        "STICKY_WEB",
    )):
        tags.add("hazard")

    if any(x in effect for x in (
        "RAPID_SPIN",
        "DEFOG",
        "MORTAL_SPIN",
        "TIDY_UP",
    )):
        tags.add("hazard_control")

    if any(x in effect for x in (
        "FOLLOW_ME",
        "RAGE_POWDER",
    )):
        tags.add("redirection")

    if "HELPING_HAND" in effect:
        tags.add("ally_support")

    # --------------------------------------------------------------
    # Switching / item / ability interaction
    # --------------------------------------------------------------

    if any(x in effect for x in (
        "TELEPORT",
        "BATON_PASS",
        "U_TURN",
        "VOLT_SWITCH",
        "FLIP_TURN",
        "PARTING_SHOT",
        "CHILLY_RECEPTION",
    )):
        tags.add("pivot")

    if any(x in effect for x in (
        "KNOCK_OFF",
        "STEAL_ITEM",
        "TRICK",
        "BESTOW",
        "RECYCLE",
        "FLING",
        "POLTERGEIST",
    )):
        tags.add("item_control")

    if any(x in effect for x in (
        "SKILL_SWAP",
        "ROLE_PLAY",
        "WORRY_SEED",
        "GASTRO_ACID",
        "ENTRAINMENT",
        "SIMPLE_BEAM",
        "CORE_ENFORCER",
    )):
        tags.add("ability_control")

    # --------------------------------------------------------------
    # Called / copied moves
    # --------------------------------------------------------------

    if any(x in effect for x in (
        "METRONOME",
        "COPYCAT",
        "ASSIST",
        "SLEEP_TALK",
        "NATURE_POWER",
        "MIRROR_MOVE",
        "MIMIC",
    )):
        tags.add("called_or_copied_move")

    # --------------------------------------------------------------
    # Target semantics
    # --------------------------------------------------------------

    if target in {
        "TARGET_BOTH",
        "TARGET_FOES_AND_ALLY",
        "TARGET_ALL_BATTLERS",
        "TARGET_USER_AND_ALLY",
    }:
        tags.add("spread_or_multi_target")

    if target == "TARGET_ALLY":
        tags.add("ally_target")

    if target == "TARGET_FIELD":
        tags.add("field_target")

    # --------------------------------------------------------------
    # Explicit properties
    # --------------------------------------------------------------

    property_map = {
        "soundMove": "sound",
        "powderMove": "powder",
        "bitingMove": "biting",
        "punchingMove": "punching",
        "slicingMove": "slicing",
        "ballisticMove": "ballistic",
        "danceMove": "dance",
        "windMove": "wind",
        "makesContact": "contact",
    }

    for prop, tag in property_map.items():
        if properties.get(prop) is True:
            tags.add(tag)

    return sorted(tags)


PRIMARY_PRECEDENCE = [
    ("ohko", "ohko"),
    ("called_or_copied_move", "called_or_copied"),
    ("delayed_damage", "delayed_damage"),
    ("forced_multiturn", "forced_multiturn"),
    ("two_turn", "two_turn"),
    ("trapping", "trapping"),
    ("hazard_control", "hazard_control"),
    ("hazard", "hazard"),
    ("pivot", "pivot"),
    ("redirection", "redirection"),
    ("protection", "protection"),
    ("healing", "healing"),
    ("weather", "weather"),
    ("field_control", "field_control"),
    ("item_control", "item_control"),
    ("ability_control", "ability_control"),
    ("ally_support", "ally_support"),
    ("drain", "drain_damage"),
    ("recoil", "recoil_damage"),
    ("priority_damage", "priority_damage"),
    ("multi_hit", "multi_hit_damage"),
    ("special_damage_formula", "special_damage_formula"),
    ("setup", "setup"),
    ("status_control", "status_control"),
    ("debuff", "debuff"),
    ("direct_damage", "direct_damage"),
    ("status_move", "other_status"),
]


def primary_family(tags):
    s = set(tags)

    for tag, family in PRIMARY_PRECEDENCE:
        if tag in s:
            return family

    return "other"


# ----------------------------------------------------------------------
# Structural feature maps for anchor similarity
# ----------------------------------------------------------------------

def power_band(move):
    p = literal_int(move.get("power_expr"))

    if p is None:
        return "power_expr"

    if p == 0:
        return "power_0"

    if p == 1 and str(move.get("effect", "")) != "EFFECT_HIT":
        return "power_sentinel"

    if p <= 40:
        return "power_low"

    if p <= 70:
        return "power_medium"

    if p <= 100:
        return "power_strong"

    if p <= 130:
        return "power_very_strong"

    return "power_extreme"


def accuracy_band(move):
    a = literal_int(move.get("accuracy_expr"))

    if a is None:
        return "accuracy_expr"

    if a == 0:
        return "accuracy_no_check"

    if a <= 70:
        return "accuracy_low"

    if a < 90:
        return "accuracy_medium"

    return "accuracy_high"


def priority_band(move):
    p = literal_int(move.get("priority_expr"))

    if p is None:
        return "priority_expr"

    if p < 0:
        return "priority_negative"

    if p == 0:
        return "priority_zero"

    if p == 1:
        return "priority_plus1"

    return "priority_plus2_or_more"


def weighted_features(move):
    f = {}

    def add(token, weight):
        old = f.get(token)

        if old is None or weight > old:
            f[token] = weight

    tags = semantic_tags(move)

    for tag in tags:
        add(f"tag:{tag}", 6.0)

    add(
        f"family:{primary_family(tags)}",
        8.0,
    )

    add(
        f"effect:{move.get('effect')}",
        8.0,
    )

    add(
        f"category:{move.get('category_expr')}",
        3.0,
    )

    add(
        f"target:{move.get('target_expr')}",
        2.5,
    )

    add(
        power_band(move),
        2.5,
    )

    add(
        accuracy_band(move),
        1.5,
    )

    add(
        priority_band(move),
        2.5,
    )

    # Structured additional effects matter heavily.
    additional = move.get("additional_effects", []) or []

    def walk(prefix, value):
        if isinstance(value, dict):
            for k, v in value.items():
                add(
                    f"{prefix}:key:{k}",
                    2.5,
                )
                walk(
                    f"{prefix}.{k}",
                    v,
                )

        elif isinstance(value, list):
            for item in value:
                walk(prefix, item)

        elif isinstance(value, (str, int, bool)):
            s = str(value)

            if len(s) <= 80:
                add(
                    f"{prefix}:value:{s}",
                    2.0,
                )

    walk("additional", additional)

    # Curated properties from the collector.
    properties = move.get("properties", {}) or {}

    for key, value in properties.items():
        if value in (False, None, 0, "", []):
            continue

        add(
            f"property:{key}",
            2.0,
        )

        if isinstance(value, (str, int, bool)):
            add(
                f"property:{key}={value}",
                1.0,
            )

    return f


def weighted_jaccard(a, b):
    keys = set(a) | set(b)

    if not keys:
        return 0.0

    numerator = 0.0
    denominator = 0.0

    for key in keys:
        av = a.get(key, 0.0)
        bv = b.get(key, 0.0)

        numerator += min(av, bv)
        denominator += max(av, bv)

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ----------------------------------------------------------------------
# Build legacy anchor reference
# ----------------------------------------------------------------------

legacy_anchors = []

for name, cost_row in legacy_cost_by_name.items():
    move = source_by_name[name]

    legacy_anchors.append({
        "constant": name,
        "name": move["name"],
        "cost": cost_row["v2_candidate_cost"],
        "family": primary_family(
            semantic_tags(move)
        ),
        "tags": semantic_tags(move),
        "features": weighted_features(move),
    })


# ----------------------------------------------------------------------
# Build Expansion-only move classifications
# ----------------------------------------------------------------------

new_moves = [
    x for x in all_moves
    if 355 <= x["id"] <= 847
]

assert len(new_moves) == 493, (
    f"Expected 493 new moves, got {len(new_moves)}"
)


rows = []


for move in new_moves:
    name = move["constant"]
    tags = semantic_tags(move)
    family = primary_family(tags)
    features = weighted_features(move)

    scored = []

    for anchor in legacy_anchors:
        score = weighted_jaccard(
            features,
            anchor["features"],
        )

        scored.append({
            "constant": anchor["constant"],
            "name": anchor["name"],
            "cost": anchor["cost"],
            "family": anchor["family"],
            "score": round(score, 4),
        })

    scored.sort(
        key=lambda x: (
            -x["score"],
            abs(
                (literal_int(move.get("power_expr")) or 0)
                -
                (
                    literal_int(
                        source_by_name[
                            x["constant"]
                        ].get("power_expr")
                    )
                    or 0
                )
            ),
            x["constant"],
        )
    )

    top = scored[:5]

    top3_costs = [
        x["cost"]
        for x in top[:3]
    ]

    cost_vote = Counter(top3_costs)

    most_common = cost_vote.most_common()

    anchor_cost_mode = None

    if most_common:
        top_count = most_common[0][1]

        tied = [
            cost
            for cost, count in most_common
            if count == top_count
        ]

        if len(tied) == 1:
            anchor_cost_mode = tied[0]

    ctx = context_by_name[name]

    row = {
        "numeric_id": move["id"],
        "constant": name,
        "name": move["name"],

        "primary_family": family,
        "semantic_tags": tags,

        "mechanics": {
            "effect": move["effect"],
            "power_expr": move["power_expr"],
            "type_expr": move["type_expr"],
            "accuracy_expr": move["accuracy_expr"],
            "pp_expr": move["pp_expr"],
            "target_expr": move["target_expr"],
            "priority_expr": move["priority_expr"],
            "category_expr": move["category_expr"],
            "additional_effects":
                move.get("additional_effects", []),
            "properties":
                move.get("properties", {}),
        },

        "campaign_context": {
            "active_levelup_species_count":
                ctx["learnability"][
                    "active_levelup_species_count"
                ],

            "egg_species_count":
                ctx["learnability"][
                    "egg_species_count"
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

        "legacy_anchor_evidence": {
            "top_anchors": top,
            "top_score":
                top[0]["score"] if top else 0.0,

            "top3_costs":
                top3_costs,

            # Evidence only.
            # This is deliberately NOT a V2 cost recommendation.
            "anchor_cost_mode":
                anchor_cost_mode,

            "anchor_cost_min":
                min(top3_costs)
                if top3_costs else None,

            "anchor_cost_max":
                max(top3_costs)
                if top3_costs else None,
        },

        "classification_status":
            "UNREVIEWED",
    }

    rows.append(row)


rows.sort(key=lambda x: x["numeric_id"])


# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------

family_counts = Counter(
    x["primary_family"]
    for x in rows
)

tag_counts = Counter()

for x in rows:
    tag_counts.update(
        x["semantic_tags"]
    )


# Anchor disagreement statistics.
same_top3 = 0
spread_1 = 0
spread_2plus = 0

for x in rows:
    e = x["legacy_anchor_evidence"]

    lo = e["anchor_cost_min"]
    hi = e["anchor_cost_max"]

    if lo is None or hi is None:
        continue

    span = hi - lo

    if span == 0:
        same_top3 += 1
    elif span == 1:
        spread_1 += 1
    else:
        spread_2plus += 1


output = {
    "schema":
        "firered-reimagined.stamina.new-move-semantics.v2",
    "schema_version": 1,

    "status":
        "CLASSIFICATION_ONLY",

    "warning":
        "anchor_cost_mode is similarity evidence only and must "
        "not be treated as an approved Stamina V2 cost.",

    "summary": {
        "move_count": len(rows),
        "family_counts":
            dict(family_counts.most_common()),

        "anchor_agreement": {
            "top3_same_cost":
                same_top3,

            "top3_cost_span_1":
                spread_1,

            "top3_cost_span_2plus":
                spread_2plus,
        },
    },

    "moves": rows,
}


OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


# ----------------------------------------------------------------------
# Human-readable report
# ----------------------------------------------------------------------

lines = [
    "# Stamina V2 — Expansion New-Move Semantic Classification",
    "",
    "Status: **CLASSIFICATION ONLY**",
    "",
    f"- New ordinary moves: **{len(rows)}**",
    "",
    "Legacy anchor costs shown here are evidence only. "
    "No new move has an approved V2 cost at this stage.",
    "",
    "## Family counts",
    "",
]

for family, count in family_counts.most_common():
    lines.append(
        f"- `{family}`: **{count}**"
    )


lines += [
    "",
    "## Anchor agreement",
    "",
    f"- Top 3 anchors same cost: **{same_top3}**",
    f"- Top 3 cost span = 1: **{spread_1}**",
    f"- Top 3 cost span >= 2: **{spread_2plus}**",
    "",
    "## Moves by family",
    "",
]


by_family = defaultdict(list)

for x in rows:
    by_family[
        x["primary_family"]
    ].append(x)


for family, members in sorted(
    by_family.items(),
    key=lambda kv: (-len(kv[1]), kv[0]),
):
    lines += [
        f"### {family}",
        "",
    ]

    for x in members:
        anchors = x[
            "legacy_anchor_evidence"
        ]["top_anchors"][:3]

        anchor_text = ", ".join(
            f"{a['constant']}:{a['cost']}"
            f" ({a['score']:.2f})"
            for a in anchors
        )

        lines.append(
            f"- `{x['constant']}` — "
            f"{x['name']} — "
            f"anchors: {anchor_text}"
        )

    lines.append("")


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


print("New-move semantic classification complete.")
print()
print("MOVES:", len(rows))
print()

print("Families:")

for family, count in family_counts.most_common():
    print(
        f"  {family:<24} {count}"
    )

print()
print("Anchor agreement:")
print("  same cost :", same_top3)
print("  span 1    :", spread_1)
print("  span >= 2 :", spread_2plus)

print()
print("Largest families:")

for family, count in family_counts.most_common(12):
    examples = [
        x["constant"]
        for x in rows
        if x["primary_family"] == family
    ][:5]

    print(
        f"  {family:<24} "
        f"{count:>3}  "
        + ", ".join(examples)
    )

print()
print("Wrote:")
print(" ", OUT_JSON.relative_to(ROOT))
print(" ", OUT_MD.relative_to(ROOT))
