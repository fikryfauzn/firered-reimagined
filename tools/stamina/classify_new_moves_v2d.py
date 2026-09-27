#!/usr/bin/env python3

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()

SOURCE = ROOT / "tools/stamina/data/moves_source_v2.json"
CONTEXT = ROOT / "tools/stamina/data/move_context_v2.json"
LEGACY = ROOT / "tools/stamina/data/legacy_costs_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/new_move_semantics_v2d.json"
OUT_MD = ROOT / "tools/stamina/reports/new_move_semantics_v2d.md"


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


# ======================================================================
# ACTIVE CONFIG
#
# Must match the active FireRed preprocessing environment already used
# by the Stamina V2 collector/refiner.
# ======================================================================

ENV = {
    "FALSE": 0,
    "TRUE": 1,

    "GEN_1": 1,
    "GEN_2": 2,
    "GEN_3": 3,
    "GEN_4": 4,
    "GEN_5": 5,
    "GEN_6": 6,
    "GEN_7": 7,
    "GEN_8": 8,
    "GEN_9": 9,
    "GEN_CHAMPIONS": 10,
    "GEN_LATEST": 9,

    "B_UPDATED_MOVE_DATA": 9,
    "B_UPDATED_MOVE_FLAGS": 9,
    "B_UPDATED_MOVE_TYPES": 9,
    "B_PHYSICAL_SPECIAL_SPLIT": 9,
}


# ======================================================================
# EXPRESSION RESOLUTION
# ======================================================================

def strip_outer_parens(expr):
    expr = expr.strip()

    while (
        len(expr) >= 2
        and expr[0] == "("
        and expr[-1] == ")"
    ):
        depth = 0
        valid = True

        for i, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1

                if depth == 0 and i != len(expr) - 1:
                    valid = False
                    break

        if not valid or depth != 0:
            break

        expr = expr[1:-1].strip()

    return expr


def split_top_level_ternary(expr):
    expr = strip_outer_parens(expr)

    depth = 0
    qpos = None

    for i, ch in enumerate(expr):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "?" and depth == 0:
            qpos = i
            break

    if qpos is None:
        return None

    depth = 0
    nested = 0
    colon = None

    for i in range(qpos + 1, len(expr)):
        ch = expr[i]

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        elif depth == 0:
            if ch == "?":
                nested += 1

            elif ch == ":":
                if nested == 0:
                    colon = i
                    break

                nested -= 1

    if colon is None:
        return None

    return (
        expr[:qpos].strip(),
        expr[qpos + 1:colon].strip(),
        expr[colon + 1:].strip(),
    )


def eval_simple(expr):
    expr = strip_outer_parens(str(expr).strip())

    expr = expr.replace("&&", " and ")
    expr = expr.replace("||", " or ")

    # C logical negation, but don't break !=.
    expr = re.sub(
        r"(?<![=!<>])!(?!=)",
        " not ",
        expr,
    )

    if not re.fullmatch(
        r"[A-Za-z0-9_()\s<>=!&|+\-*/%.]+",
        expr,
    ):
        raise ValueError(expr)

    return eval(
        expr,
        {"__builtins__": {}},
        ENV,
    )


def resolve_scalar(value):
    if isinstance(value, bool):
        return int(value)

    if isinstance(value, int):
        return value

    if value is None:
        return None

    expr = strip_outer_parens(str(value).strip())

    if re.fullmatch(r"-?\d+", expr):
        return int(expr)

    ternary = split_top_level_ternary(expr)

    if ternary:
        cond, yes, no = ternary

        try:
            result = bool(eval_simple(cond))
        except Exception:
            return None

        return resolve_scalar(
            yes if result else no
        )

    try:
        value = eval_simple(expr)

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, (int, float)):
            return value

    except Exception:
        pass

    return None


# ======================================================================
# SEMANTIC HELPERS
# ======================================================================

def truthy(value):
    if value is True:
        return True

    if isinstance(value, str):
        return value.strip().upper() == "TRUE"

    return False


def blob(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).upper()


STATUS_TERMS = {
    "SLEEP",
    "POISON",
    "TOXIC",
    "PARALYSIS",
    "BURN",
    "FREEZE",
    "FROSTBITE",
    "CONFUSION",
}


def additional_semantics(move):
    result = {
        "self_boost": False,
        "target_boost": False,
        "self_debuff": False,
        "target_debuff": False,
        "status_inflict": False,
        "status_remove": False,
        "flinch": False,
        "drain": False,
        "trapping": False,
        "pp_control": False,
        "heal_block": False,
        "recharge": False,
    }

    target = str(
        move.get("target_expr", "")
    ).upper()

    for add in move.get("additional_effects", []) or []:
        b = blob(add)

        is_self = truthy(
            add.get("self")
        )

        if (
            "self" not in add
            and target == "TARGET_USER"
        ):
            is_self = True

        if any(x in b for x in (
            "STAT_PLUS",
            "STAT_CHANGE_EFFECT_PLUS",
        )):
            if is_self:
                result["self_boost"] = True
            else:
                result["target_boost"] = True

        if any(x in b for x in (
            "STAT_MINUS",
            "STAT_CHANGE_EFFECT_MINUS",
        )):
            if is_self:
                result["self_debuff"] = True
            else:
                result["target_debuff"] = True

        if "REMOVE_STATUS" in b:
            result["status_remove"] = True

        elif any(term in b for term in STATUS_TERMS):
            result["status_inflict"] = True

        if "FLINCH" in b:
            result["flinch"] = True

        if "ABSORB" in b:
            result["drain"] = True

        if "WRAP" in b:
            result["trapping"] = True

        if "EERIE_SPELL" in b:
            result["pp_control"] = True

        if "PSYCHIC_NOISE" in b:
            result["heal_block"] = True

        if "RECHARGE" in b:
            result["recharge"] = True

    return result


# ======================================================================
# PRIMARY FAMILY CLASSIFICATION
# ======================================================================

def classify_move(move):
    effect = str(
        move.get("effect", "")
    ).upper()

    category = str(
        move.get("category_expr", "")
    ).upper()

    target = str(
        move.get("target_expr", "")
    ).upper()

    props = move.get(
        "properties",
        {},
    ) or {}

    extra = additional_semantics(move)

    power = resolve_scalar(
        move.get("power_expr")
    )

    accuracy = resolve_scalar(
        move.get("accuracy_expr")
    )

    priority = resolve_scalar(
        move.get("priority_expr")
    )

    strike_count = resolve_scalar(
        props.get("strikeCount")
    )

    damaging = (
        category != "DAMAGE_CATEGORY_STATUS"
    )

    tags = set()

    if damaging:
        tags.add("damaging_move")
    else:
        tags.add("status_move")

    # ------------------------------------------------------------------
    # Target semantics
    # ------------------------------------------------------------------

    if target in {
        "TARGET_BOTH",
        "TARGET_FOES_AND_ALLY",
        "TARGET_ALL_BATTLERS",
        "TARGET_USER_AND_ALLY",
    }:
        tags.add("multi_target")

    if target == "TARGET_ALLY":
        tags.add("ally_target")

    if target == "TARGET_FIELD":
        tags.add("field_target")

    # ------------------------------------------------------------------
    # Priority
    # ------------------------------------------------------------------

    if priority is not None:
        if priority > 0:
            tags.add("positive_priority")
        elif priority < 0:
            tags.add("negative_priority")

    # ------------------------------------------------------------------
    # Additional-effect semantics
    # ------------------------------------------------------------------

    for key, active in extra.items():
        if active:
            tags.add(key)

    # ------------------------------------------------------------------
    # Explicit move properties
    # ------------------------------------------------------------------

    property_tags = {
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

    for prop, tag in property_tags.items():
        if truthy(props.get(prop)):
            tags.add(tag)

    # ==================================================================
    # DAMAGING MOVES
    # ==================================================================

    if damaging:
        tags.add("direct_damage")

        # Scaling damage based on defeated allies.
        if effect == "EFFECT_LAST_RESPECTS":
            tags.add("scaling_power")
            family = "special_damage_formula"

        # Recharge / self-sacrifice
        elif (
            extra["recharge"]
            or "RECHARGE" in effect
        ):
            family = "recharge_damage"

        elif any(x in effect for x in (
            "EXPLOSION",
            "SELF_DESTRUCT",
            "FINAL_GAMBIT",
            "MIND_BLOWN",
            "CHLOROBLAST",
        )):
            family = "sacrifice_damage"

        # Damage based on damage received.
        elif "REFLECT_DAMAGE" in effect:
            family = "counter_damage"

        # Delayed resolution.
        elif "FUTURE_SIGHT" in effect:
            family = "delayed_damage"

        # Free/forced continuation.
        elif any(x in effect for x in (
            "ROLLOUT",
            "RAMPAGE",
        )) or "THRASH" in blob(
            move.get("additional_effects", [])
        ):
            family = "forced_multiturn"

        # Two-turn commitment.
        elif (
            "TWO_TURNS" in effect
            or "SEMI_INVULNERABLE" in effect
            or props.get("twoTurnAttack")
        ):
            family = "two_turn"

        # Attack then switch.
        elif "HIT_ESCAPE" in effect:
            tags.add("pivot")
            family = "pivot_damage"

        # Attack then force target switch.
        elif "HIT_SWITCH_TARGET" in effect:
            tags.add("phazing")
            family = "phazing_damage"

        # Binding/trapping damage.
        elif (
            extra["trapping"]
            or "BIND" in effect
        ):
            family = "trapping_damage"

        # Terrain-dependent offensive moves.
        elif any(x in effect for x in (
            "TERRAIN_BOOST",
            "TERRAIN_PULSE",
        )):
            family = "terrain_damage"

        # PP manipulation attached to damage.
        elif extra["pp_control"]:
            family = "pp_control_damage"

        # Healing prevention attached to damage.
        elif extra["heal_block"]:
            family = "heal_block_damage"

        # Removes an existing status as part of damage.
        elif extra["status_remove"]:
            family = "status_removal_damage"

        # Variable/custom formula.
        elif (
            power == 1
            and effect != "EFFECT_HIT"
        ) or any(x in effect for x in (
            "GYRO_BALL",
            "ELECTRO_BALL",
            "PSYWAVE",
            "LEVEL_DAMAGE",
            "FIXED_DAMAGE",
            "SUPER_FANG",
            "ENDEAVOR",
            "WRING_OUT",
            "CRUSH_GRIP",
            "STORED_POWER",
            "PUNISHMENT",
        )):
            family = "special_damage_formula"

        # Explicit conditional-damage effects.
        elif any(x in effect for x in (
            "ASSURANCE",
            "PAYBACK",
            "REVENGE",
            "AVALANCHE",
            "DOUBLE_POWER",
            "BOLT_BEAK",
            "BRINE",
            "VENOSHOCK",
            "HEX",
            "ACROBATICS",
            "FACADE",
            "LAST_RESORT",
            "STEEL_ROLLER",
            "BELCH",
            "SUCKER_PUNCH",
            "FIRST_TURN_ONLY",
            "UPPER_HAND",
        )):
            family = "conditional_damage"

        elif "OHKO" in effect:
            family = "ohko"

        elif "RECOIL" in effect:
            family = "recoil_damage"

        elif extra["drain"]:
            family = "drain_damage"

        elif (
            truthy(props.get("multiHit"))
            or (
                strike_count is not None
                and strike_count > 1
            )
        ):
            tags.add("multi_hit")
            family = "multi_hit_damage"

        elif (
            priority is not None
            and priority > 0
        ):
            family = "priority_damage"

        elif extra["self_debuff"]:
            family = "self_debuff_damage"

        elif extra["self_boost"]:
            family = "boosting_damage"

        elif extra["target_debuff"]:
            family = "target_debuff_damage"

        elif extra["status_inflict"]:
            family = "status_damage"

        else:
            family = "direct_damage"

    # ==================================================================
    # STATUS MOVES
    # ==================================================================

    else:
        # --------------------------------------------------------------
        # Exact modern status identities
        # --------------------------------------------------------------

        if effect == "EFFECT_POWER_TRICK":
            family = "stat_control"

        elif effect == "EFFECT_REFLECT_TYPE":
            family = "type_control"

        elif effect == "EFFECT_MAT_BLOCK":
            family = "protection"

        elif effect in {
            "EFFECT_HEALING_WISH",
            "EFFECT_LUNAR_DANCE",
        }:
            family = "sacrifice_support"

        elif effect == "EFFECT_REVIVAL_BLESSING":
            family = "revival_support"

        elif "OVERWRITE_ABILITY" in effect:
            family = "ability_control"

        elif "THIRD_TYPE" in effect:
            family = "type_control"

        elif "HEAL_PULSE" in effect:
            family = "healing"

        elif "AQUA_RING" in effect:
            family = "healing"

        elif any(x in effect for x in (
            "AFTER_YOU",
            "QUASH",
        )):
            family = "turn_order_control"

        elif any(x in effect for x in (
            "POWER_SWAP",
            "GUARD_SWAP",
            "HEART_SWAP",
            "GUARD_SPLIT",
            "POWER_SPLIT",
            "TOPSY_TURVY",
        )):
            family = "stat_control"

        elif any(x in effect for x in (
            "ACUPRESSURE",
            "GEOMANCY",
            "AUTOTOMIZE",
        )):
            family = "setup"

        elif any(x in effect for x in (
            "ROTOTILLER",
            "FLOWER_SHIELD",
            "MAGNETIC_FLUX",
            "AROMATIC_MIST",
        )):
            family = "ally_support"

        elif any(x in effect for x in (
            "LUCKY_CHANT",
            "MAGNET_RISE",
            "TELEKINESIS",
        )):
            family = "field_control"

        elif any(x in effect for x in (
            "ELECTRIFY",
            "ION_DELUGE",
            "POWDER",
        )):
            family = "move_control"

        elif "FAIRY_LOCK" in effect:
            family = "trapping_status"

        elif "DARK_VOID" in effect:
            family = "status_control"

        elif any(x in effect for x in (
            "HAPPY_HOUR",
            "CELEBRATE",
            "HOLD_HANDS",
        )):
            family = "noncombat_utility"

        # Pivot / switching
        elif any(x in effect for x in (
            "PARTING_SHOT",
            "SHED_TAIL",
            "WEATHER_AND_SWITCH",
            "TELEPORT",
            "BATON_PASS",
        )):
            tags.add("pivot")
            family = "pivot_support"

        elif "ALLY_SWITCH" in effect:
            family = "reposition"

        # Protection
        elif any(x in effect for x in (
            "PROTECT",
            "ENDURE",
            "KING_SHIELD",
            "SPIKY_SHIELD",
            "BANEFUL_BUNKER",
            "SILK_TRAP",
            "BURNING_BULWARK",
            "OBSTRUCT",
        )):
            family = "protection"

        # Direct recovery
        elif (
            truthy(props.get("healingMove"))
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
                "WISH",
            ))
        ):
            family = "healing"

        # Self-sacrifice support
        elif any(x in effect for x in (
            "HEALING_WISH",
            "LUNAR_DANCE",
            "MEMENTO",
        )):
            family = "sacrifice_support"

        # Hazards
        elif any(x in effect for x in (
            "SPIKES",
            "STEALTH_ROCK",
            "TOXIC_SPIKES",
            "STICKY_WEB",
        )):
            family = "hazard"

        elif any(x in effect for x in (
            "DEFOG",
            "RAPID_SPIN",
            "TIDY_UP",
            "MORTAL_SPIN",
        )):
            family = "hazard_control"

        # Weather / terrain / rooms
        elif "WEATHER" in effect:
            family = "weather"

        elif "TERRAIN" in effect:
            family = "terrain"

        elif any(x in effect for x in (
            "TRICK_ROOM",
            "WONDER_ROOM",
            "MAGIC_ROOM",
            "GRAVITY",
            "TAILWIND",
            "AURORA_VEIL",
            "REFLECT",
            "LIGHT_SCREEN",
            "SAFEGUARD",
            "MIST",
        )):
            family = "field_control"

        # Redirection / ally support
        elif any(x in effect for x in (
            "FOLLOW_ME",
            "RAGE_POWDER",
        )):
            family = "redirection"

        elif any(x in effect for x in (
            "HELPING_HAND",
            "COACHING",
            "DECORATE",
        )):
            family = "ally_support"

        # Move denial/control
        elif any(x in effect for x in (
            "DISABLE",
            "ENCORE",
            "TAUNT",
            "TORMENT",
            "IMPRISON",
            "HEAL_BLOCK",
            "THROAT_CHOP",
        )):
            family = "move_control"

        # PP manipulation
        elif any(x in effect for x in (
            "SPITE",
            "GRUDGE",
        )):
            family = "pp_control"

        # Status curing / transfer
        elif any(x in effect for x in (
            "REFRESH",
            "HEAL_BELL",
            "AROMATHERAPY",
            "PSYCHO_SHIFT",
        )):
            family = "status_utility"

        # Type manipulation
        elif any(x in effect for x in (
            "CONVERSION",
            "CAMOUFLAGE",
            "REFLECT_TYPE",
            "SOAK",
            "MAGIC_POWDER",
            "FORESTS_CURSE",
            "TRICK_OR_TREAT",
        )):
            family = "type_control"

        # Item interaction
        elif any(x in effect for x in (
            "TRICK",
            "BESTOW",
            "RECYCLE",
            "EMBARGO",
        )):
            family = "item_control"

        # Ability interaction
        elif any(x in effect for x in (
            "SKILL_SWAP",
            "ROLE_PLAY",
            "WORRY_SEED",
            "GASTRO_ACID",
            "ENTRAINMENT",
            "SIMPLE_BEAM",
        )):
            family = "ability_control"

        # Trap without damage
        elif any(x in effect for x in (
            "MEAN_LOOK",
            "BLOCK",
            "SPIDER_WEB",
        )):
            family = "trapping_status"

        # Called/copied result
        elif any(x in effect for x in (
            "METRONOME",
            "COPYCAT",
            "ASSIST",
            "SLEEP_TALK",
            "NATURE_POWER",
            "MIRROR_MOVE",
            "MIMIC",
            "ME_FIRST",
        )):
            family = "called_or_copied"

        # Stat manipulation
        elif (
            extra["self_boost"]
            and target == "TARGET_USER"
        ):
            family = "setup"

        elif (
            extra["target_boost"]
            and target in {
                "TARGET_ALLY",
                "TARGET_USER_AND_ALLY",
                "TARGET_USER_OR_ALLY",
            }
        ):
            family = "ally_support"

        elif extra["target_debuff"]:
            family = "debuff"

        # Direct status
        elif extra["status_inflict"] or any(x in effect for x in (
            "NON_VOLATILE_STATUS",
            "CONFUSE",
            "YAWN",
        )):
            family = "status_control"

        else:
            family = "utility_status"

    return {
        "family": family,
        "tags": sorted(tags),

        "resolved": {
            "power": power,
            "accuracy": accuracy,
            "priority": priority,
        },

        "additional_semantics": extra,
    }


# ======================================================================
# ANCHOR RELATIONSHIPS
# ======================================================================

RELATED = {
    "direct_damage": {
        "direct_damage",
        "conditional_damage",
        "status_damage",
        "target_debuff_damage",
        "boosting_damage",
        "self_debuff_damage",
    },

    "conditional_damage": {
        "conditional_damage",
        "direct_damage",
    },

    "priority_damage": {
        "priority_damage",
        "direct_damage",
    },

    "status_damage": {
        "status_damage",
        "target_debuff_damage",
        "direct_damage",
    },

    "target_debuff_damage": {
        "target_debuff_damage",
        "status_damage",
        "direct_damage",
    },

    "boosting_damage": {
        "boosting_damage",
        "direct_damage",
    },

    "self_debuff_damage": {
        "self_debuff_damage",
        "recoil_damage",
        "direct_damage",
    },

    "terrain_damage": {
        "terrain_damage",
        "conditional_damage",
        "direct_damage",
    },

    "pivot_damage": {
        "pivot_damage",
        "direct_damage",
        "pivot_support",
    },

    "phazing_damage": {
        "phazing_damage",
        "direct_damage",
        "trapping_status",
    },

    "pp_control_damage": {
        "pp_control_damage",
        "status_damage",
        "direct_damage",
    },

    "heal_block_damage": {
        "heal_block_damage",
        "status_damage",
        "direct_damage",
    },

    "status_removal_damage": {
        "status_removal_damage",
        "conditional_damage",
        "direct_damage",
    },
}


# ======================================================================
# ANCHOR SCORING
# ======================================================================

def power_score(a, b):
    if a is None or b is None:
        return 0.0

    # Sentinel/custom-formula power should not be compared
    # numerically as ordinary base power.
    if a == 1 or b == 1:
        return 0.0

    d = abs(a - b)

    if d <= 5:
        return 6.0
    if d <= 10:
        return 5.0
    if d <= 20:
        return 3.5
    if d <= 30:
        return 2.0
    if d <= 50:
        return 0.8

    return 0.0


def accuracy_score(a, b):
    if a is None or b is None:
        return 0.0

    # 0 is no-normal-accuracy-check semantics.
    if a == 0 or b == 0:
        return 1.0 if a == b else 0.0

    d = abs(a - b)

    if d == 0:
        return 1.5
    if d <= 5:
        return 1.0
    if d <= 10:
        return 0.5

    return 0.0


def priority_score(a, b):
    if a is None or b is None:
        return 0.0

    if a == b:
        return 2.0

    if (
        (a > 0 and b > 0)
        or
        (a < 0 and b < 0)
    ):
        return 0.8

    return 0.0


def anchor_score(move, sem, anchor):
    other = anchor["sem"]

    score = 0.0

    # Family dominates.
    if sem["family"] == other["family"]:
        score += 12.0

    elif other["family"] in RELATED.get(
        sem["family"],
        set(),
    ):
        score += 4.0

    # Exact non-generic effect identity is useful,
    # but generic EFFECT_HIT should not dominate.
    effect_a = move["effect"]
    effect_b = anchor["move"]["effect"]

    if effect_a == effect_b:
        if effect_a == "EFFECT_HIT":
            score += 1.0
        else:
            score += 5.0

    if (
        move["category_expr"]
        == anchor["move"]["category_expr"]
    ):
        score += 2.0

    if (
        move["target_expr"]
        == anchor["move"]["target_expr"]
    ):
        score += 1.5

    score += power_score(
        sem["resolved"]["power"],
        other["resolved"]["power"],
    )

    score += accuracy_score(
        sem["resolved"]["accuracy"],
        other["resolved"]["accuracy"],
    )

    score += priority_score(
        sem["resolved"]["priority"],
        other["resolved"]["priority"],
    )

    tags_a = set(sem["tags"])
    tags_b = set(other["tags"])

    if tags_a or tags_b:
        union = tags_a | tags_b
        inter = tags_a & tags_b

        score += (
            len(inter) / len(union)
        ) * 4.0

    # Strong signal for structured secondary semantics.
    sa = sem["additional_semantics"]
    sb = other["additional_semantics"]

    for key in sa:
        if sa[key] and sb.get(key):
            score += 1.2

    return round(score, 4)


# ======================================================================
# BUILD LEGACY ANCHORS
# ======================================================================

legacy_anchors = []

for name, cost_row in legacy_cost_by_name.items():
    move = source_by_name[name]
    sem = classify_move(move)

    legacy_anchors.append({
        "constant": name,
        "name": move["name"],
        "cost":
            cost_row["v2_candidate_cost"],
        "move": move,
        "sem": sem,
    })


legacy_by_family = defaultdict(list)

for anchor in legacy_anchors:
    legacy_by_family[
        anchor["sem"]["family"]
    ].append(anchor)


# ======================================================================
# BUILD NEW MOVE DATASET
# ======================================================================

new_moves = [
    x for x in all_moves
    if 355 <= x["id"] <= 847
]

assert len(new_moves) == 493


rows = []

unresolved_power = []
unresolved_accuracy = []
unresolved_priority = []


for move in new_moves:
    sem = classify_move(move)
    family = sem["family"]

    if (
        sem["resolved"]["power"] is None
        and move.get("power_expr") is not None
    ):
        unresolved_power.append(
            move["constant"]
        )

    if (
        sem["resolved"]["accuracy"] is None
        and move.get("accuracy_expr") is not None
    ):
        unresolved_accuracy.append(
            move["constant"]
        )

    if (
        sem["resolved"]["priority"] is None
        and move.get("priority_expr") is not None
    ):
        unresolved_priority.append(
            move["constant"]
        )

    # --------------------------------------------------------------
    # Candidate anchor pool
    # --------------------------------------------------------------

    exact_pool = list(
        legacy_by_family.get(
            family,
            [],
        )
    )

    if len(exact_pool) >= 3:
        pool = exact_pool
        scope = "SAME_FAMILY"

    else:
        related_families = RELATED.get(
            family,
            {family},
        )

        pool = [
            x
            for x in legacy_anchors
            if x["sem"]["family"]
               in related_families
        ]

        if exact_pool:
            scope = "SAME_PLUS_RELATED"
        else:
            scope = "RELATED_FAMILY"

        # Rare family with no useful mapping.
        if len(pool) < 3:
            pool = legacy_anchors
            scope = "GLOBAL_FALLBACK"

    scored = []

    for anchor in pool:
        score = anchor_score(
            move,
            sem,
            anchor,
        )

        scored.append({
            "constant":
                anchor["constant"],

            "name":
                anchor["name"],

            "cost":
                anchor["cost"],

            "family":
                anchor["sem"]["family"],

            "score":
                score,

            "resolved_power":
                anchor["sem"][
                    "resolved"
                ]["power"],
        })

    scored.sort(
        key=lambda x: (
            -x["score"],
            x["constant"],
        )
    )

    top = scored[:5]
    top3 = top[:3]

    top3_costs = [
        x["cost"]
        for x in top3
    ]

    ctx = context_by_name[
        move["constant"]
    ]

    rows.append({
        "numeric_id":
            move["id"],

        "constant":
            move["constant"],

        "name":
            move["name"],

        "primary_family":
            family,

        "semantic_tags":
            sem["tags"],

        "resolved_mechanics":
            sem["resolved"],

        "additional_semantics":
            sem["additional_semantics"],

        "mechanics": {
            "effect":
                move["effect"],

            "power_expr":
                move["power_expr"],

            "accuracy_expr":
                move["accuracy_expr"],

            "priority_expr":
                move["priority_expr"],

            "type_expr":
                move["type_expr"],

            "target_expr":
                move["target_expr"],

            "category_expr":
                move["category_expr"],

            "additional_effects":
                move.get(
                    "additional_effects",
                    [],
                ),

            "properties":
                move.get(
                    "properties",
                    {},
                ),
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
                ctx["learnability"][
                    "is_current_tm"
                ],

            "is_current_hm":
                ctx["learnability"][
                    "is_current_hm"
                ],

            "explicit_frlg_trainer_move_count":
                ctx["campaign_context"][
                    "explicit_frlg_trainer_move_count"
                ],
        },

        "legacy_anchor_evidence": {
            "scope":
                scope,

            "same_family_anchor_count":
                len(exact_pool),

            "top_anchors":
                top,

            "top3_costs":
                top3_costs,

            "cost_min":
                min(top3_costs)
                if top3_costs
                else None,

            "cost_max":
                max(top3_costs)
                if top3_costs
                else None,
        },

        "classification_status":
            "UNREVIEWED",
    })


rows.sort(
    key=lambda x: x["numeric_id"]
)


# ======================================================================
# SANITY ASSERTIONS
#
# These were concrete failures in v2a.
# If one regresses, stop immediately.
# ======================================================================

by_name = {
    x["constant"]: x
    for x in rows
}


def require(name, family):
    actual = by_name[name][
        "primary_family"
    ]

    assert actual == family, (
        f"{name}: expected {family}, "
        f"got {actual}"
    )


require(
    "MOVE_U_TURN",
    "pivot_damage",
)

require(
    "MOVE_VOLT_SWITCH",
    "pivot_damage",
)

require(
    "MOVE_FLIP_TURN",
    "pivot_damage",
)

require(
    "MOVE_METAL_BURST",
    "counter_damage",
)

require(
    "MOVE_CLOSE_COMBAT",
    "self_debuff_damage",
)

require(
    "MOVE_HAMMER_ARM",
    "self_debuff_damage",
)

require(
    "MOVE_CHARGE_BEAM",
    "boosting_damage",
)

require(
    "MOVE_WAKE_UP_SLAP",
    "status_removal_damage",
)

require(
    "MOVE_AURA_SPHERE",
    "direct_damage",
)

require(
    "MOVE_GLACIAL_LANCE",
    "direct_damage",
)

require("MOVE_ROCK_POLISH", "setup")
require("MOVE_NASTY_PLOT", "setup")
require("MOVE_QUIVER_DANCE", "setup")
require("MOVE_SHELL_SMASH", "setup")

require("MOVE_PLAY_NICE", "debuff")
require("MOVE_CONFIDE", "debuff")

require("MOVE_WORRY_SEED", "ability_control")
require("MOVE_SIMPLE_BEAM", "ability_control")

require("MOVE_TRICK_OR_TREAT", "type_control")
require("MOVE_FORESTS_CURSE", "type_control")

require("MOVE_HEAL_PULSE", "healing")

require("MOVE_AFTER_YOU", "turn_order_control")
require("MOVE_QUASH", "turn_order_control")

# Multi-hit representation probes
require("MOVE_DOUBLE_HIT", "multi_hit_damage")
require("MOVE_GEAR_GRIND", "multi_hit_damage")
require("MOVE_SCALE_SHOT", "multi_hit_damage")
require("MOVE_TRIPLE_AXEL", "multi_hit_damage")
require("MOVE_SURGING_STRIKES", "multi_hit_damage")
require("MOVE_POPULATION_BOMB", "multi_hit_damage")
require("MOVE_DRAGON_DARTS", "multi_hit_damage")

# Recharge representation probes
require("MOVE_GIGA_IMPACT", "recharge_damage")
require("MOVE_ROAR_OF_TIME", "recharge_damage")
require("MOVE_PRISMATIC_LASER", "recharge_damage")
require("MOVE_ETERNABEAM", "recharge_damage")

assert (
    by_name[
        "MOVE_AURA_SPHERE"
    ]["resolved_mechanics"]["power"]
    == 80
)

assert (
    by_name[
        "MOVE_GLACIAL_LANCE"
    ]["resolved_mechanics"]["power"]
    == 120
)


# ======================================================================
# SUMMARY / DIAGNOSTICS
# ======================================================================

family_counts = Counter(
    x["primary_family"]
    for x in rows
)

scope_counts = Counter(
    x["legacy_anchor_evidence"]["scope"]
    for x in rows
)

same_cost = 0
span1 = 0
span2 = 0
span3plus = 0

for x in rows:
    e = x["legacy_anchor_evidence"]

    lo = e["cost_min"]
    hi = e["cost_max"]

    if lo is None or hi is None:
        continue

    span = hi - lo

    if span == 0:
        same_cost += 1
    elif span == 1:
        span1 += 1
    elif span == 2:
        span2 += 1
    else:
        span3plus += 1


output = {
    "schema":
        "firered-reimagined.stamina.new-move-semantics.v2d",

    "schema_version": 1,

    "status":
        "CLASSIFICATION_ONLY",

    "summary": {
        "move_count":
            len(rows),

        "family_counts":
            dict(
                family_counts.most_common()
            ),

        "anchor_scope_counts":
            dict(scope_counts),

        "anchor_cost_spans": {
            "same_cost":
                same_cost,

            "span_1":
                span1,

            "span_2":
                span2,

            "span_3plus":
                span3plus,
        },

        "unresolved_scalars": {
            "power":
                unresolved_power,

            "accuracy":
                unresolved_accuracy,

            "priority":
                unresolved_priority,
        },
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


# ======================================================================
# HUMAN REPORT
# ======================================================================

lines = [
    "# Stamina V2 — New Move Semantic Classification v2d",
    "",
    "Status: **CLASSIFICATION ONLY**",
    "",
    f"- Moves: **{len(rows)}**",
    f"- Unresolved power scalars: **{len(unresolved_power)}**",
    f"- Unresolved accuracy scalars: **{len(unresolved_accuracy)}**",
    f"- Unresolved priority scalars: **{len(unresolved_priority)}**",
    "",
    "## Families",
    "",
]

for family, count in family_counts.most_common():
    lines.append(
        f"- `{family}`: **{count}**"
    )


lines += [
    "",
    "## Anchor scopes",
    "",
]

for scope, count in scope_counts.most_common():
    lines.append(
        f"- `{scope}`: **{count}**"
    )


lines += [
    "",
    "## Anchor cost disagreement",
    "",
    f"- same cost: **{same_cost}**",
    f"- span 1: **{span1}**",
    f"- span 2: **{span2}**",
    f"- span >= 3: **{span3plus}**",
    "",
]


by_family = defaultdict(list)

for x in rows:
    by_family[
        x["primary_family"]
    ].append(x)


for family, members in sorted(
    by_family.items(),
    key=lambda kv: (
        -len(kv[1]),
        kv[0],
    ),
):
    lines += [
        f"## {family}",
        "",
    ]

    for x in members:
        p = x[
            "resolved_mechanics"
        ]["power"]

        anchors = ", ".join(
            f"{a['constant']}:{a['cost']}"
            f"/{a['score']:.1f}"
            for a in
            x[
                "legacy_anchor_evidence"
            ]["top_anchors"][:3]
        )

        lines.append(
            f"- `{x['constant']}` "
            f"P={p} — {anchors}"
        )

    lines.append("")


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


print("New-move semantic classifier v2d complete.")
print()
print("MOVES:", len(rows))
print()

print("Unresolved active scalars:")
print("  power   :", len(unresolved_power))
print("  accuracy:", len(unresolved_accuracy))
print("  priority:", len(unresolved_priority))
print()

print("Families:")

for family, count in family_counts.most_common():
    print(
        f"  {family:<24} {count}"
    )

print()
print("Anchor scopes:")

for scope, count in scope_counts.most_common():
    print(
        f"  {scope:<20} {count}"
    )

print()
print("Anchor cost spans:")
print("  same      :", same_cost)
print("  span 1    :", span1)
print("  span 2    :", span2)
print("  span >= 3 :", span3plus)

print()
print("Sanity probes:")
for name in (
    "MOVE_U_TURN",
    "MOVE_METAL_BURST",
    "MOVE_WAKE_UP_SLAP",
    "MOVE_CLOSE_COMBAT",
    "MOVE_CHARGE_BEAM",
    "MOVE_AURA_SPHERE",
    "MOVE_GLACIAL_LANCE",
):
    x = by_name[name]

    print(
        f"  {name:<26} "
        f"{x['primary_family']:<24} "
        f"P={x['resolved_mechanics']['power']}"
    )

print()
print("Wrote:")
print(" ", OUT_JSON.relative_to(ROOT))
print(" ", OUT_MD.relative_to(ROOT))
