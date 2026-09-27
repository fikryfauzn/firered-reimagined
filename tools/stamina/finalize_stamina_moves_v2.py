#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(".").resolve()

MOVES_H = ROOT / "include/constants/moves.h"

LEGACY_PATH = (
    ROOT
    / "tools/stamina/legacy_v1/stamina_moves.json"
)

NEW_PATH = (
    ROOT
    / "tools/stamina/data/"
      "new_move_review_decisions_v2.json"
)

OUT_PATH = (
    ROOT
    / "tools/stamina/data/stamina_moves_v2.json"
)

EXPECTED_MOVES = 848
EXPECTED_LEGACY = 355
EXPECTED_NEW = 493

LEGACY_SYMBOL_ALIASES = {
    "MOVE_SMELLING_SALT": "MOVE_SMELLINGSALT",
}

EXPECTED_DISTRIBUTION = {
    0: 2,
    1: 41,
    2: 136,
    3: 319,
    4: 251,
    5: 91,
    6: 8,
}


def die(message: str) -> None:
    raise SystemExit("ERROR: " + message)


def load_json(path: Path):
    if not path.is_file():
        die("missing required file: " + str(path))

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def get_current_move_ids(names):
    """
    Resolve the reviewed ordinary-move constants against the current
    Expansion header.

    pokeemerald-expansion contains symbolic aliases in moves.h, so the
    number of MOVE_* symbol names is intentionally NOT used as the move
    count invariant.

    The invariant we care about is:

        848 reviewed constants
        -> 848 unique numeric IDs
        -> exactly IDs 0..847
    """

    names = sorted(set(names))

    if len(names) != EXPECTED_MOVES:
        die(
            "expected "
            + str(EXPECTED_MOVES)
            + " reviewed move constants, got "
            + str(len(names))
        )

    source = [
        "#include <stdio.h>",
        '#include "constants/moves.h"',
        "",
        "int main(void)",
        "{",
        '    printf("__MOVES_COUNT__ %d\\n", MOVES_COUNT);',
    ]

    for name in names:
        source.append(
            '    printf("'
            + name
            + ' %d\\n", '
            + name
            + ");"
        )

    source += [
        "    return 0;",
        "}",
        "",
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)

        c_path = temp / "stamina_move_ids.c"
        exe_path = temp / "stamina_move_ids"

        c_path.write_text(
            "\n".join(source),
            encoding="utf-8",
        )

        compile_result = subprocess.run(
            [
                "cc",
                "-I",
                str(ROOT / "include"),
                str(c_path),
                "-o",
                str(exe_path),
            ],
            capture_output=True,
            text=True,
        )

        if compile_result.returncode != 0:
            print(compile_result.stdout)
            print(compile_result.stderr)

            die(
                "failed to compile temporary "
                "move-ID verifier"
            )

        result = subprocess.run(
            [str(exe_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            die(
                "temporary move-ID verifier failed"
            )

    mapping = {}
    moves_count = None

    for line in result.stdout.splitlines():
        name, value_text = line.split()
        value = int(value_text)

        if name == "__MOVES_COUNT__":
            moves_count = value
        else:
            mapping[name] = value

    if moves_count != EXPECTED_MOVES:
        die(
            "MOVES_COUNT is "
            + str(moves_count)
            + ", expected "
            + str(EXPECTED_MOVES)
        )

    if len(mapping) != EXPECTED_MOVES:
        die(
            "resolved reviewed move map has "
            + str(len(mapping))
            + " entries"
        )

    id_counts = Counter(mapping.values())

    duplicate_ids = {
        numeric_id: count
        for numeric_id, count in id_counts.items()
        if count != 1
    }

    if duplicate_ids:
        reverse = {}

        for name, numeric_id in mapping.items():
            reverse.setdefault(
                numeric_id,
                [],
            ).append(name)

        details = []

        for numeric_id in sorted(duplicate_ids):
            details.append(
                str(numeric_id)
                + "="
                + ",".join(
                    sorted(reverse[numeric_id])
                )
            )

        die(
            "reviewed constants contain numeric-ID aliases: "
            + "; ".join(details)
        )

    expected_ids = set(
        range(EXPECTED_MOVES)
    )

    actual_ids = set(
        mapping.values()
    )

    if actual_ids != expected_ids:
        missing_ids = sorted(
            expected_ids - actual_ids
        )

        extra_ids = sorted(
            actual_ids - expected_ids
        )

        die(
            "reviewed ordinary move IDs are not "
            "exactly 0..847; missing="
            + str(missing_ids)
            + " extra="
            + str(extra_ids)
        )

    return mapping


print(
    "=== OBJECTIVE 02A — "
    "FINALIZE STAMINA V2 DATASET ==="
)

legacy_doc = load_json(LEGACY_PATH)
new_doc = load_json(NEW_PATH)

legacy_moves = legacy_doc.get("moves")
new_decisions = new_doc.get("decisions")

if not isinstance(legacy_moves, dict):
    die(
        "legacy stamina_moves.json "
        "does not contain moves object"
    )

if not isinstance(new_decisions, dict):
    die(
        "new decision file does not "
        "contain decisions object"
    )

# Translate historical FireRed symbol names into the
# current Expansion repository naming scheme.
legacy_runtime_names = {
    LEGACY_SYMBOL_ALIASES.get(name, name): name
    for name in legacy_moves
}

if len(legacy_runtime_names) != len(legacy_moves):
    die(
        "legacy symbol aliasing created duplicate "
        "runtime constants"
    )

new_runtime_names = set(new_decisions)

reviewed_constants = (
    set(legacy_runtime_names)
    | new_runtime_names
)

if len(reviewed_constants) != EXPECTED_MOVES:
    die(
        "combined reviewed symbol count is "
        + str(len(reviewed_constants))
        + ", expected "
        + str(EXPECTED_MOVES)
    )

current_ids = get_current_move_ids(
    reviewed_constants
)

print("MOVES_COUNT        :", len(current_ids))
print("Legacy V1 entries  :", len(legacy_moves))
print("New V2 decisions   :", len(new_decisions))

if len(legacy_moves) != EXPECTED_LEGACY:
    die(
        "legacy count is "
        + str(len(legacy_moves))
        + ", expected "
        + str(EXPECTED_LEGACY)
    )

if len(new_decisions) != EXPECTED_NEW:
    die(
        "new decision count is "
        + str(len(new_decisions))
        + ", expected "
        + str(EXPECTED_NEW)
    )

legacy_set = set(legacy_runtime_names)
new_set = set(new_decisions)
current_set = set(current_ids)

overlap = sorted(
    legacy_set & new_set
)

missing_current_legacy = sorted(
    legacy_set - current_set
)

missing_current_new = sorted(
    new_set - current_set
)

uncovered = sorted(
    current_set
    - legacy_set
    - new_set
)

unexpected = sorted(
    (legacy_set | new_set)
    - current_set
)

print("Legacy/New overlap :", len(overlap))
print("Uncovered moves    :", len(uncovered))
print("Unexpected moves   :", len(unexpected))

if overlap:
    die(
        "legacy/new overlap: "
        + ", ".join(overlap)
    )

if missing_current_legacy:
    die(
        "legacy constants absent from "
        "current source: "
        + ", ".join(
            missing_current_legacy
        )
    )

if missing_current_new:
    die(
        "new constants absent from "
        "current source: "
        + ", ".join(
            missing_current_new
        )
    )

if uncovered:
    die(
        "current ordinary moves without "
        "reviewed Stamina decision: "
        + ", ".join(uncovered)
    )

if unexpected:
    die(
        "reviewed constants outside "
        "ordinary current move space: "
        + ", ".join(unexpected)
    )

if legacy_set | new_set != current_set:
    die(
        "combined reviewed set does not "
        "equal current ordinary move set"
    )

# ------------------------------------------------------------
# Verify legacy numeric identities survived Expansion unchanged.
# ------------------------------------------------------------

legacy_id_errors = []

for old_constant, entry in legacy_moves.items():
    runtime_constant = LEGACY_SYMBOL_ALIASES.get(
        old_constant,
        old_constant,
    )

    old_id = entry.get("numeric_id")

    if not isinstance(old_id, int):
        legacy_id_errors.append(
            old_constant + ": missing numeric_id"
        )
        continue

    current_id = current_ids[runtime_constant]

    if old_id != current_id:
        legacy_id_errors.append(
            old_constant
            + " -> "
            + runtime_constant
            + ": old="
            + str(old_id)
            + " current="
            + str(current_id)
        )

if legacy_id_errors:
    die(
        "legacy numeric identity drift: "
        + "; ".join(legacy_id_errors)
    )

print(
    "Legacy numeric IDs : PASS "
    "(355 unchanged)"
)

# ------------------------------------------------------------
# Validate review status and costs.
# ------------------------------------------------------------

for constant, entry in new_decisions.items():
    if entry.get("decision") != "APPROVED":
        die(
            constant
            + ": decision is not APPROVED"
        )

    cost = entry.get("cost")

    if (
        not isinstance(cost, int)
        or isinstance(cost, bool)
        or cost < 1
        or cost > 6
    ):
        die(
            constant
            + ": invalid new cost "
            + repr(cost)
        )

for constant, entry in legacy_moves.items():
    cost = entry.get("cost")

    if (
        not isinstance(cost, int)
        or isinstance(cost, bool)
        or cost < 0
        or cost > 6
    ):
        die(
            constant
            + ": invalid legacy cost "
            + repr(cost)
        )

# ------------------------------------------------------------
# Build canonical V2 roster.
# ------------------------------------------------------------

canonical_moves = {}

for constant, numeric_id in sorted(
    current_ids.items(),
    key=lambda pair: pair[1],
):
    if constant in legacy_runtime_names:
        old_constant = legacy_runtime_names[constant]
        old = legacy_moves[old_constant]

        canonical_moves[constant] = {
            "numeric_id": numeric_id,
            "cost": old["cost"],
            "origin": "legacy_v1",
            "review_status": "approved_v1",
            "primary_role": old.get(
                "primary_role"
            ),
            "mechanic_tags": old.get(
                "mechanic_tags",
                [],
            ),
            "review_flags": old.get(
                "review_flags",
                [],
            ),
            "stamina_rules": old.get(
                "stamina_rules",
                [],
            ),
            "notes": (
                old.get("design", {})
                .get("notes", "")
            ),
        }

    else:
        decision = new_decisions[constant]

        canonical_moves[constant] = {
            "numeric_id": numeric_id,
            "cost": decision["cost"],
            "origin": "expansion_review_v2",
            "review_status": "approved_v2",
            "review_packet": decision[
                "packet"
            ],
            "notes": decision.get(
                "notes",
                "",
            ),
            "special_case_flags":
                decision.get(
                    "special_case_flags",
                    [],
                ),
        }

if len(canonical_moves) != EXPECTED_MOVES:
    die(
        "canonical roster contains "
        + str(len(canonical_moves))
        + " moves"
    )

# ------------------------------------------------------------
# Strong identity invariant: numeric IDs 0..847 exactly once.
# ------------------------------------------------------------

numeric_ids = [
    entry["numeric_id"]
    for entry in canonical_moves.values()
]

if len(set(numeric_ids)) != EXPECTED_MOVES:
    die(
        "duplicate numeric IDs "
        "in canonical roster"
    )

if set(numeric_ids) != set(
    range(EXPECTED_MOVES)
):
    die(
        "canonical numeric IDs do not "
        "cover exactly 0..847"
    )

# ------------------------------------------------------------
# Distribution invariant.
# ------------------------------------------------------------

distribution = Counter(
    entry["cost"]
    for entry in canonical_moves.values()
)

print()
print("Final cost distribution:")

for cost in range(0, 7):
    print(
        "  cost "
        + str(cost)
        + ": "
        + str(distribution.get(cost, 0))
    )

actual_distribution = {
    cost: distribution.get(cost, 0)
    for cost in range(0, 7)
}

if actual_distribution != EXPECTED_DISTRIBUTION:
    die(
        "final distribution mismatch: "
        + repr(actual_distribution)
    )

# ------------------------------------------------------------
# Sentinel invariants.
# ------------------------------------------------------------

if canonical_moves["MOVE_NONE"]["cost"] != 0:
    die("MOVE_NONE must cost 0")

if (
    canonical_moves["MOVE_STRUGGLE"]["cost"]
    != 0
):
    die("MOVE_STRUGGLE must cost 0")

if (
    canonical_moves["MOVE_NONE"]["numeric_id"]
    != 0
):
    die("MOVE_NONE must remain ID 0")

if (
    canonical_moves[
        "MOVE_STRUGGLE"
    ]["numeric_id"]
    != 165
):
    die(
        "MOVE_STRUGGLE numeric ID "
        "changed unexpectedly"
    )

# ------------------------------------------------------------
# Output.
# ------------------------------------------------------------

output = {
    "schema": "firered_stamina_moves_v2",
    "schema_version": 2,
    "status": "FROZEN_V2",
    "economy": {
        "max_stamina": 6,
        "starting_stamina": 6,
        "regen_per_completed_turn": 2,
        "shared_player_side_pool": True,
        "switching_refills": False,
    },
    "execution_contract": {
        "ordinary_move_count": 848,
        "runtime_table_bound": "MOVES_COUNT",
        "z_moves_use_base_move_cost": True,
        "max_moves_use_base_move_cost": True,
        "struggle_cost": 0,
        "caller_pays_called_result_free": True,
        "multi_turn_initial_commitment_only": True,
        "recharge_turn_free": True,
    },
    "counts": {
        "moves": 848,
        "legacy_v1": 355,
        "expansion_review_v2": 493,
        "cost_distribution": {
            str(cost): count
            for cost, count
            in sorted(
                EXPECTED_DISTRIBUTION.items()
            )
        },
    },
    "sources": {
        "legacy": (
            "tools/stamina/legacy_v1/"
            "stamina_moves.json"
        ),
        "expansion_decisions": (
            "tools/stamina/data/"
            "new_move_review_decisions_v2.json"
        ),
        "move_identity": (
            "include/constants/moves.h"
        ),
    },
    "moves": canonical_moves,
}

tmp = OUT_PATH.with_name(
    OUT_PATH.name + ".tmp"
)

tmp.write_text(
    json.dumps(
        output,
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)

# Reload before publishing.
check = json.loads(
    tmp.read_text(
        encoding="utf-8",
    )
)

if check.get("status") != "FROZEN_V2":
    die(
        "temporary output failed "
        "status validation"
    )

if len(check.get("moves", {})) != 848:
    die(
        "temporary output failed "
        "move-count validation"
    )

tmp.replace(OUT_PATH)

print()
print("Wrote:")
print(
    " ",
    OUT_PATH.relative_to(ROOT),
)

print()
print(
    "OBJECTIVE 02A: PASS"
)

print(
    "848 / 848 ordinary move IDs "
    "have explicit frozen Stamina costs."
)
