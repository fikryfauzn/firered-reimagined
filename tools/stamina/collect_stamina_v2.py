#!/usr/bin/env python3
"""
FireRed Reimagined — Stamina V2 source/context collector

Run from the pokeemerald-expansion / firered-reimagined repository root:

    python3 tools/stamina/collect_stamina_v2.py

Outputs:
    tools/stamina/data/moves_source_v2.json
    tools/stamina/data/move_context_v2.json
    tools/stamina/reports/collection_validation_v2.md

This collector performs DATA COLLECTION ONLY.
It does not assign Stamina costs and does not modify battle runtime code.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path.cwd()

MOVES_H = ROOT / "include/constants/moves.h"
MOVES_INFO_H = ROOT / "src/data/moves_info.h"
GENERAL_CONFIG_H = ROOT / "include/config/general.h"
POKEMON_CONFIG_H = ROOT / "include/config/pokemon.h"
ALL_LEARNABLES_JSON = ROOT / "src/data/pokemon/all_learnables.json"
EGG_MOVES_H = ROOT / "src/data/pokemon/egg_moves.h"
TMS_HMS_H = ROOT / "include/constants/tms_hms.h"
TRAINERS_FRLG_PARTY = ROOT / "src/data/trainers_frlg.party"

OUT_DATA = ROOT / "tools/stamina/data"
OUT_REPORTS = ROOT / "tools/stamina/reports"
OUT_SOURCE = OUT_DATA / "moves_source_v2.json"
OUT_CONTEXT = OUT_DATA / "move_context_v2.json"
OUT_REPORT = OUT_REPORTS / "collection_validation_v2.md"


REQUIRED = [
    MOVES_H,
    MOVES_INFO_H,
    GENERAL_CONFIG_H,
    POKEMON_CONFIG_H,
    ALL_LEARNABLES_JSON,
    EGG_MOVES_H,
    TMS_HMS_H,
    TRAINERS_FRLG_PARTY,
]


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_c_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*?$", "", text, flags=re.M)
    return text


def parse_move_enum(text: str) -> dict[str, Any]:
    m = re.search(
        r"enum\s+__attribute__\s*\(\(packed\)\)\s+Move\s*\{(?P<body>.*?)\n\};",
        text,
        flags=re.S,
    )
    if not m:
        die("Could not locate packed enum Move in include/constants/moves.h")

    body = strip_c_comments(m.group("body"))
    values: dict[str, int] = {}
    canonical_by_id: dict[int, str] = {}
    aliases_by_id: dict[int, list[str]] = defaultdict(list)
    current = -1

    for raw in body.splitlines():
        line = raw.strip().rstrip(",")
        if not line or line.startswith("#"):
            continue

        mm = re.match(r"^([A-Z][A-Z0-9_]*)(?:\s*=\s*(.+))?$", line)
        if not mm:
            continue

        name, expr = mm.group(1), mm.group(2)

        if expr is None:
            current += 1
        else:
            expr = expr.strip()
            if re.fullmatch(r"\d+", expr):
                current = int(expr)
            elif re.fullmatch(r"0x[0-9A-Fa-f]+", expr):
                current = int(expr, 16)
            elif expr in values:
                current = values[expr]
            else:
                plus = re.fullmatch(r"([A-Z][A-Z0-9_]*)\s*\+\s*(\d+)", expr)
                if plus and plus.group(1) in values:
                    current = values[plus.group(1)] + int(plus.group(2))
                else:
                    # Unknown preprocessor expression: not needed for canonical Move IDs.
                    continue

        values[name] = current

        if name.startswith("MOVE_"):
            aliases_by_id[current].append(name)
            canonical_by_id.setdefault(current, name)

    required_markers = [
        "MOVES_COUNT",
        "FIRST_Z_MOVE",
        "LAST_Z_MOVE",
        "MOVES_COUNT_Z",
        "FIRST_MAX_MOVE",
        "LAST_MAX_MOVE",
        "MOVES_COUNT_DYNAMAX",
        "MOVES_COUNT_ALL",
    ]
    missing = [x for x in required_markers if x not in values]
    if missing:
        die(f"Missing Move enum markers: {', '.join(missing)}")

    return {
        "values": values,
        "canonical_by_id": canonical_by_id,
        "aliases_by_id": aliases_by_id,
    }


def balanced_block(text: str, open_pos: int) -> tuple[str, int]:
    if text[open_pos] != "{":
        raise ValueError("balanced_block must start at '{'")

    depth = 1
    i = open_pos + 1
    in_string = False
    escaped = False

    while i < len(text) and depth:
        ch = text[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1

        i += 1

    if depth:
        raise ValueError("Unterminated brace block")

    return text[open_pos + 1 : i - 1], i



def read_active_moves_info() -> str:
    """
    Return moves_info.h after resolving active FireRed #if/#else branches.

    - Uses the FireRed build target.
    - Removes inactive preprocessor branches.
    - Preserves ordinary C expressions such as generation ternaries.
    """
    cmd = [
        "arm-none-eabi-cpp",
        "-fdirectives-only",
        "-P",
        "-iquote", "include",
        "-Wno-trigraphs",
        "-DMODERN=1",
        "-DTESTING=0",
        "-DFIRERED",
        "-std=gnu17",
        str(MOVES_INFO_H),
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        die("arm-none-eabi-cpp not found")
    except subprocess.CalledProcessError as exc:
        die(
            "Failed to preprocess moves_info.h:\n"
            + exc.stderr
        )

    return result.stdout


def parse_designated_blocks(text: str) -> dict[str, str]:
    anchor = text.find("const struct MoveInfo gMovesInfo")
    if anchor < 0:
        die("Could not locate gMovesInfo in src/data/moves_info.h")

    start = text.find("{", anchor)
    if start < 0:
        die("Could not locate gMovesInfo opening brace")

    blocks: dict[str, str] = {}
    pos = start + 1
    pat = re.compile(r"\[\s*(MOVE_[A-Z0-9_]+)\s*\]\s*=\s*\{")

    while True:
        m = pat.search(text, pos)
        if not m:
            break

        constant = m.group(1)
        brace = text.find("{", m.start())
        block, end = balanced_block(text, brace)
        blocks[constant] = block
        pos = end

    return blocks


def split_top_level_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i = 0
    n = len(block)

    while i < n:
        brace = paren = bracket = 0
        in_string = False
        escaped = False
        found = -1

        while i < n:
            ch = block[i]

            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                i += 1
                continue

            if ch == '"':
                in_string = True
            elif ch == "{":
                brace += 1
            elif ch == "}":
                brace -= 1
            elif ch == "(":
                paren += 1
            elif ch == ")":
                paren -= 1
            elif ch == "[":
                bracket += 1
            elif ch == "]":
                bracket -= 1
            elif ch == "." and brace == 0 and paren == 0 and bracket == 0:
                found = i
                break
            i += 1

        if found < 0:
            break

        m = re.match(r"\.([A-Za-z0-9_]+)\s*=", block[found:])
        if not m:
            i = found + 1
            continue

        name = m.group(1)
        i = found + m.end()
        value_start = i

        brace = paren = bracket = 0
        in_string = False
        escaped = False

        while i < n:
            ch = block[i]

            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                i += 1
                continue

            if ch == '"':
                in_string = True
            elif ch == "{":
                brace += 1
            elif ch == "}":
                brace -= 1
            elif ch == "(":
                paren += 1
            elif ch == ")":
                paren -= 1
            elif ch == "[":
                bracket += 1
            elif ch == "]":
                bracket -= 1
            elif ch == "," and brace == 0 and paren == 0 and bracket == 0:
                break

            i += 1

        fields[name] = block[value_start:i].strip()
        i += 1

    return fields


def compact(expr: str | None) -> str | None:
    if expr is None:
        return None
    return re.sub(r"\s+", " ", expr).strip()


def extract_simple_field(block: str, name: str) -> str | None:
    """
    Extract scalar top-level MoveInfo fields directly from their source line.

    This intentionally bypasses the generic structural parser because RHH
    descriptions can contain #if/#else branches with mutually exclusive
    closing parentheses. In raw, un-preprocessed source those branches can
    confuse generic delimiter-depth parsing even though the C is valid after
    preprocessing.
    """
    m = re.search(
        rf"(?m)^\s*\.{re.escape(name)}\s*=\s*([^,\n]+),\s*(?://.*)?$",
        block,
    )
    if not m:
        return None
    return m.group(1).strip()


def extract_additional_effects_expr(block: str) -> str | None:
    """
    Extract ADDITIONAL_EFFECTS(...) independently of preceding description
    conditionals.
    """
    m = re.search(
        r"(?m)^\s*\.additionalEffects\s*=\s*ADDITIONAL_EFFECTS\s*\(",
        block,
    )
    if not m:
        return None

    expr_start = block.find("ADDITIONAL_EFFECTS", m.start())
    open_pos = block.find("(", expr_start)

    depth = 1
    i = open_pos + 1
    in_string = False
    escaped = False

    while i < len(block) and depth:
        ch = block[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        i += 1

    if depth:
        return None

    return block[expr_start:i].strip()


def extract_c_string(expr: str | None) -> str | None:
    if not expr:
        return None

    pieces = re.findall(r'"((?:\\.|[^"\\])*)"', expr)
    if not pieces:
        return None

    joined = "".join(pieces)
    return bytes(joined, "utf-8").decode("unicode_escape")


def parse_additional_effects(expr: str | None) -> list[dict[str, str]]:
    if not expr:
        return []

    effects: list[dict[str, str]] = []
    pos = 0

    while True:
        open_pos = expr.find("{", pos)
        if open_pos < 0:
            break

        block, end = balanced_block(expr, open_pos)
        fields = split_top_level_fields(block)

        if fields:
            effects.append({k: compact(v) or "" for k, v in fields.items()})

        pos = end

    return effects


def resolve_active_levelup_generation(general_cfg: str, pokemon_cfg: str) -> int:
    latest_m = re.search(r"^\s*#define\s+GEN_LATEST\s+GEN_(\d+)\s*$", general_cfg, re.M)
    if not latest_m:
        die("Could not resolve GEN_LATEST from include/config/general.h")
    latest = int(latest_m.group(1))

    p_m = re.search(
        r"^\s*#define\s+P_LVL_UP_LEARNSETS\s+([A-Z0-9_]+)\b",
        pokemon_cfg,
        re.M,
    )
    if not p_m:
        die("Could not resolve P_LVL_UP_LEARNSETS from include/config/pokemon.h")

    token = p_m.group(1)
    if token == "GEN_LATEST":
        return latest

    explicit = re.fullmatch(r"GEN_(\d+)", token)
    if explicit:
        return int(explicit.group(1))

    die(f"Unsupported P_LVL_UP_LEARNSETS expression: {token}")


def parse_levelup(path: Path) -> dict[str, Any]:
    text = read(path)
    species_to_entries: dict[str, list[dict[str, Any]]] = {}
    move_species: dict[str, set[str]] = defaultdict(set)
    move_occurrences: Counter[str] = Counter()

    pat = re.compile(
        r"static const struct LevelUpMove s([A-Za-z0-9_]+)LevelUpLearnset\[\]\s*=\s*\{"
        r"(?P<body>.*?)\n\};",
        re.S,
    )

    for m in pat.finditer(text):
        species = m.group(1)
        entries: list[dict[str, Any]] = []

        for mm in re.finditer(
            r"LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*(MOVE_[A-Z0-9_]+)\s*\)",
            m.group("body"),
        ):
            level = int(mm.group(1))
            move = mm.group(2)
            entries.append({"level": level, "move": move})
            move_species[move].add(species)
            move_occurrences[move] += 1

        species_to_entries[species] = entries

    return {
        "species_to_entries": species_to_entries,
        "move_species": move_species,
        "move_occurrences": move_occurrences,
    }


def parse_egg_moves(text: str) -> dict[str, Any]:
    species_to_moves: dict[str, list[str]] = {}
    move_species: dict[str, set[str]] = defaultdict(set)

    pat = re.compile(
        r"static const u16 s([A-Za-z0-9_]+)EggMoveLearnset\[\]\s*=\s*\{"
        r"(?P<body>.*?)\n\};",
        re.S,
    )

    for m in pat.finditer(text):
        species = m.group(1)
        moves = [
            x
            for x in re.findall(r"\b(MOVE_[A-Z0-9_]+)\b", m.group("body"))
            if x != "MOVE_UNAVAILABLE"
        ]
        species_to_moves[species] = moves
        for move in set(moves):
            move_species[move].add(species)

    return {
        "species_to_moves": species_to_moves,
        "move_species": move_species,
    }


def parse_tm_hm(text: str) -> dict[str, Any]:
    tm_block = re.search(
        r"#define\s+FOREACH_TM\(F\)\s*\\(?P<body>.*?)\n\n#define\s+FOREACH_HM",
        text,
        re.S,
    )
    hm_block = re.search(
        r"#define\s+FOREACH_HM\(F\)\s*\\(?P<body>.*?)\n\n#define\s+FOREACH_TMHM",
        text,
        re.S,
    )

    if not tm_block or not hm_block:
        die("Could not parse FOREACH_TM / FOREACH_HM")

    tms = [f"MOVE_{x}" for x in re.findall(r"F\(([A-Z0-9_]+)\)", tm_block.group("body"))]
    hms = [f"MOVE_{x}" for x in re.findall(r"F\(([A-Z0-9_]+)\)", hm_block.group("body"))]

    return {"tms": tms, "hms": hms}


def parse_trainer_explicit_moves(
    text: str, move_name_to_constant: dict[str, str]
) -> dict[str, Any]:
    usage: Counter[str] = Counter()
    unresolved: Counter[str] = Counter()

    for m in re.finditer(r"^\-\s+(.+?)\s*$", text, re.M):
        human_name = m.group(1).strip()
        constant = move_name_to_constant.get(human_name.casefold())

        if constant:
            usage[constant] += 1
        else:
            unresolved[human_name] += 1

    return {
        "usage": usage,
        "unresolved": unresolved,
    }


def main() -> None:
    if not (ROOT / ".git").exists():
        die("Run this script from the repository root.")

    missing_files = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    if missing_files:
        die("Missing required files:\n  " + "\n  ".join(missing_files))

    commit = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status = git("status", "--short")

    moves_h_text = read(MOVES_H)
    moves_info_text = read_active_moves_info()

    enum = parse_move_enum(moves_h_text)
    values: dict[str, int] = enum["values"]
    canonical_by_id: dict[int, str] = enum["canonical_by_id"]
    aliases_by_id: dict[int, list[str]] = enum["aliases_by_id"]

    normal_count = values["MOVES_COUNT"]
    blocks = parse_designated_blocks(moves_info_text)

    core_fields = {
        "name",
        "description",
        "effect",
        "power",
        "type",
        "accuracy",
        "pp",
        "target",
        "priority",
        "category",
        "additionalEffects",
    }

    ignored_nonbattle_fields = {
        "contestEffect",
        "contestCategory",
        "contestComboStarterId",
        "contestComboMoves",
        "battleAnimScript",
    }

    moves: list[dict[str, Any]] = []
    missing_records: list[dict[str, Any]] = []

    for move_id in range(normal_count):
        constant = canonical_by_id.get(move_id)
        if constant is None:
            missing_records.append({"id": move_id, "reason": "no canonical constant"})
            continue

        block = blocks.get(constant)
        if block is None:
            missing_records.append(
                {"id": move_id, "constant": constant, "reason": "missing gMovesInfo record"}
            )
            continue

        fields = split_top_level_fields(block)

        # Repair canonical battle fields directly from their initializer lines.
        # This makes extraction robust against #if branches inside descriptions.
        for field_name in (
            "effect",
            "power",
            "type",
            "accuracy",
            "pp",
            "target",
            "priority",
            "category",
        ):
            direct_value = extract_simple_field(block, field_name)
            if direct_value is not None:
                fields[field_name] = direct_value

        direct_additional = extract_additional_effects_expr(block)
        if direct_additional is not None:
            fields["additionalEffects"] = direct_additional

        properties = {
            k: compact(v)
            for k, v in fields.items()
            if k not in core_fields and k not in ignored_nonbattle_fields
        }

        moves.append(
            {
                "id": move_id,
                "constant": constant,
                "aliases": [
                    x for x in aliases_by_id.get(move_id, []) if x != constant
                ],
                "name": extract_c_string(fields.get("name")),
                "description": extract_c_string(fields.get("description")),
                "effect": compact(fields.get("effect")),
                "power_expr": compact(fields.get("power")),
                "type_expr": compact(fields.get("type")),
                "accuracy_expr": compact(fields.get("accuracy")),
                "pp_expr": compact(fields.get("pp")),
                "target_expr": compact(fields.get("target")),
                "priority_expr": compact(fields.get("priority")),
                "category_expr": compact(fields.get("category")),
                "additional_effects": parse_additional_effects(
                    fields.get("additionalEffects")
                ),
                "properties": properties,
            }
        )

    if missing_records:
        die(
            "Canonical move extraction incomplete:\n"
            + json.dumps(missing_records[:20], indent=2)
        )

    if len(moves) != normal_count:
        die(f"Expected {normal_count} normal records, got {len(moves)}")

    # Active level-up generation.
    general_cfg = read(GENERAL_CONFIG_H)
    pokemon_cfg = read(POKEMON_CONFIG_H)
    active_gen = resolve_active_levelup_generation(general_cfg, pokemon_cfg)

    levelup_path = ROOT / f"src/data/pokemon/level_up_learnsets/gen_{active_gen}.h"
    if not levelup_path.exists():
        die(f"Active level-up file does not exist: {levelup_path.relative_to(ROOT)}")

    levelup = parse_levelup(levelup_path)
    egg = parse_egg_moves(read(EGG_MOVES_H))
    tmhm = parse_tm_hm(read(TMS_HMS_H))

    # all_learnables.json = union of Level/TM/Egg/Tutor learnability over all
    # Expansion-supported games. This is useful context, NOT current-campaign access.
    with ALL_LEARNABLES_JSON.open("r", encoding="utf-8") as fp:
        all_learnables: dict[str, list[str]] = json.load(fp)

    all_learnable_species: dict[str, set[str]] = defaultdict(set)
    for species, learnable_moves in all_learnables.items():
        for move in set(learnable_moves):
            all_learnable_species[move].add(species)

    move_name_to_constant = {
        (m["name"] or "").casefold(): m["constant"]
        for m in moves
        if m["name"]
    }
    trainer_explicit = parse_trainer_explicit_moves(
        read(TRAINERS_FRLG_PARTY),
        move_name_to_constant,
    )

    tm_set = set(tmhm["tms"])
    hm_set = set(tmhm["hms"])

    context_rows: list[dict[str, Any]] = []
    for m in moves:
        move = m["constant"]
        context_rows.append(
            {
                "id": m["id"],
                "constant": move,
                "name": m["name"],
                "learnability": {
                    "any_supported_game_species_count": len(
                        all_learnable_species.get(move, set())
                    ),
                    "active_levelup_generation": active_gen,
                    "active_levelup_species_count": len(
                        levelup["move_species"].get(move, set())
                    ),
                    "active_levelup_occurrences": levelup["move_occurrences"].get(
                        move, 0
                    ),
                    "active_levelup_species": sorted(
                        levelup["move_species"].get(move, set())
                    ),
                    "egg_species_count": len(egg["move_species"].get(move, set())),
                    "egg_species": sorted(egg["move_species"].get(move, set())),
                    "is_current_tm": move in tm_set,
                    "is_current_hm": move in hm_set,
                },
                "campaign_context": {
                    # Only moves written explicitly in trainers_frlg.party.
                    # Most vanilla FRLG trainer mons omit their move list and
                    # receive level-up moves at runtime, so this is intentionally
                    # NOT called complete trainer usage.
                    "explicit_frlg_trainer_move_count": trainer_explicit[
                        "usage"
                    ].get(move, 0),
                },
            }
        )

    source_doc = {
        "schema": "firered-reimagined.stamina.moves_source.v2",
        "schema_version": 1,
        "source": {
            "repository": "rh-hideout/pokeemerald-expansion",
            "git_commit": commit,
            "git_branch_when_collected": branch,
            "working_tree_dirty_when_collected": bool(status),
            "files": [
                "include/constants/moves.h",
                "src/data/moves_info.h",
            ],
            "note": (
                "Compile-time expressions are intentionally preserved. "
                "This is canonical source extraction, not a flattened "
                "generation-config snapshot."
            ),
        },
        "move_universe": {
            "normal": {
                "first_id": 0,
                "last_id": normal_count - 1,
                "count": normal_count,
            },
            "z_moves": {
                "first_id": values["FIRST_Z_MOVE"],
                "last_id": values["LAST_Z_MOVE"],
                "count": values["MOVES_COUNT_Z"] - values["FIRST_Z_MOVE"],
            },
            "max_and_gmax": {
                "first_id": values["FIRST_MAX_MOVE"],
                "last_id": values["LAST_MAX_MOVE"],
                "count": values["MOVES_COUNT_DYNAMAX"] - values["FIRST_MAX_MOVE"],
            },
            "all_move_slots": {"count": values["MOVES_COUNT_ALL"]},
        },
        "moves": moves,
    }

    context_doc = {
        "schema": "firered-reimagined.stamina.move_context.v2",
        "schema_version": 1,
        "source": {
            "git_commit": commit,
            "active_levelup_generation": active_gen,
            "files": [
                str(levelup_path.relative_to(ROOT)),
                "src/data/pokemon/all_learnables.json",
                "src/data/pokemon/egg_moves.h",
                "include/constants/tms_hms.h",
                "src/data/trainers_frlg.party",
            ],
            "important_semantics": {
                "all_learnables": (
                    "Union of learnability across Expansion-supported games, "
                    "used by RHH learnset helper tooling. It is not equivalent "
                    "to current FireRed campaign availability."
                ),
                "trainer_usage": (
                    "Only explicit '- Move Name' entries from trainers_frlg.party "
                    "are counted here. Trainer mons without explicit moves use "
                    "runtime/default learnset logic and require a later campaign-menu pass."
                ),
            },
        },
        "summary": {
            "all_learnables_species_keys": len(all_learnables),
            "all_learnables_unique_moves": len(all_learnable_species),
            "all_learnables_species_move_links": sum(
                len(v) for v in all_learnables.values()
            ),
            "active_levelup_learnsets": len(levelup["species_to_entries"]),
            "active_levelup_unique_moves": len(levelup["move_species"]),
            "active_levelup_total_entries": sum(
                levelup["move_occurrences"].values()
            ),
            "egg_learnsets": len(egg["species_to_moves"]),
            "egg_unique_moves": len(egg["move_species"]),
            "egg_total_entries": sum(
                len(v) for v in egg["species_to_moves"].values()
            ),
            "current_tm_count": len(tmhm["tms"]),
            "current_hm_count": len(tmhm["hms"]),
            "frlg_explicit_trainer_move_lines": sum(
                trainer_explicit["usage"].values()
            ),
            "frlg_unresolved_explicit_move_lines": sum(
                trainer_explicit["unresolved"].values()
            ),
        },
        "current_tms": tmhm["tms"],
        "current_hms": tmhm["hms"],
        "moves": context_rows,
        "unresolved_explicit_trainer_move_names": dict(
            trainer_explicit["unresolved"].most_common()
        ),
    }

    OUT_DATA.mkdir(parents=True, exist_ok=True)
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    OUT_SOURCE.write_text(
        json.dumps(source_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OUT_CONTEXT.write_text(
        json.dumps(context_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    validation_lines = [
        "# Stamina V2 — Expansion Data Collection Validation",
        "",
        f"- Git commit: `{commit}`",
        f"- Branch at collection: `{branch}`",
        f"- Working tree dirty before collection: `{bool(status)}`",
        "",
        "## Canonical move universe",
        "",
        f"- Normal move slots: **{normal_count}** (`0..{normal_count - 1}`)",
        f"- Parsed normal `gMovesInfo` records: **{len(moves)}**",
        f"- Missing normal records: **0**",
        f"- Z-Move IDs: **{values['FIRST_Z_MOVE']}..{values['LAST_Z_MOVE']}**",
        f"- Max/G-Max IDs: **{values['FIRST_MAX_MOVE']}..{values['LAST_MAX_MOVE']}**",
        f"- All engine move slots: **{values['MOVES_COUNT_ALL']}**",
        "",
        "## Learnability/context",
        "",
        f"- Active level-up generation: **Gen {active_gen}**",
        f"- Active level-up learnsets: **{len(levelup['species_to_entries'])}**",
        f"- Unique moves in active level-up learnsets: **{len(levelup['move_species'])}**",
        f"- Active level-up entries: **{sum(levelup['move_occurrences'].values())}**",
        f"- `all_learnables.json` species keys: **{len(all_learnables)}**",
        f"- Unique moves in `all_learnables.json`: **{len(all_learnable_species)}**",
        f"- Egg-move learnsets: **{len(egg['species_to_moves'])}**",
        f"- Unique egg moves: **{len(egg['move_species'])}**",
        f"- Current TMs: **{len(tmhm['tms'])}**",
        f"- Current HMs: **{len(tmhm['hms'])}**",
        "",
        "## Trainer context",
        "",
        f"- Explicit move lines resolved in `trainers_frlg.party`: **{sum(trainer_explicit['usage'].values())}**",
        f"- Explicit move lines unresolved by move-name mapping: **{sum(trainer_explicit['unresolved'].values())}**",
        "",
        "> This trainer count is intentionally incomplete. Most vanilla FRLG trainer Pokémon",
        "> omit explicit moves and receive moves from level-up/default logic. A later",
        "> campaign-menu collector must reconstruct those actual four-move menus.",
        "",
        "## Gate result",
        "",
        "**PASS — canonical Expansion move/source extraction and first availability/context layer are complete.**",
        "",
        "This is not yet the Stamina-cost freeze. No costs are assigned by this collector.",
        "",
    ]

    OUT_REPORT.write_text("\n".join(validation_lines), encoding="utf-8")

    print("Stamina V2 collection complete.")
    print(f"  canonical rows : {len(moves)}/{normal_count}")
    print(f"  active levelups: {len(levelup['species_to_entries'])}")
    print(f"  all learnables : {len(all_learnables)} species keys")
    print(f"  egg learnsets  : {len(egg['species_to_moves'])}")
    print(f"  current TM/HM  : {len(tmhm['tms'])}/{len(tmhm['hms'])}")
    print()
    print(f"Wrote: {OUT_SOURCE.relative_to(ROOT)}")
    print(f"Wrote: {OUT_CONTEXT.relative_to(ROOT)}")
    print(f"Wrote: {OUT_REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
