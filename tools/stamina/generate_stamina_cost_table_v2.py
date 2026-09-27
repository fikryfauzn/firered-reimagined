#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(".").resolve()

SOURCE = (
    ROOT
    / "tools/stamina/data/stamina_moves_v2.json"
)

MOVES_H = (
    ROOT
    / "include/constants/moves.h"
)

OUTPUT = (
    ROOT
    / "src/data/stamina_move_costs.h"
)

MANIFEST = (
    ROOT
    / "tools/stamina/data/"
      "stamina_cost_table_manifest_v2.json"
)

EXPECTED_MOVE_COUNT = 848

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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    tmp.write_text(
        text,
        encoding="utf-8",
    )

    tmp.replace(path)


def load_source():
    if not SOURCE.is_file():
        die(
            "canonical V2 dataset missing: "
            + str(SOURCE)
        )

    data = json.loads(
        SOURCE.read_text(
            encoding="utf-8",
        )
    )

    if data.get("status") != "FROZEN_V2":
        die(
            "canonical dataset is not FROZEN_V2"
        )

    moves = data.get("moves")

    if not isinstance(moves, dict):
        die(
            "canonical dataset has no moves object"
        )

    if len(moves) != EXPECTED_MOVE_COUNT:
        die(
            "canonical move count is "
            + str(len(moves))
            + ", expected "
            + str(EXPECTED_MOVE_COUNT)
        )

    return data, moves


def validate_canonical_moves(moves):
    by_id = {}

    for constant, entry in moves.items():
        if not re.fullmatch(
            r"MOVE_[A-Z0-9_]+",
            constant,
        ):
            die(
                "invalid move constant: "
                + repr(constant)
            )

        numeric_id = entry.get(
            "numeric_id"
        )

        cost = entry.get("cost")

        if (
            not isinstance(numeric_id, int)
            or isinstance(numeric_id, bool)
        ):
            die(
                constant
                + ": invalid numeric_id "
                + repr(numeric_id)
            )

        if (
            not isinstance(cost, int)
            or isinstance(cost, bool)
            or cost < 0
            or cost > 6
        ):
            die(
                constant
                + ": invalid cost "
                + repr(cost)
            )

        if numeric_id in by_id:
            die(
                "duplicate numeric ID "
                + str(numeric_id)
                + ": "
                + by_id[numeric_id][0]
                + " and "
                + constant
            )

        by_id[numeric_id] = (
            constant,
            entry,
        )

    expected_ids = set(
        range(EXPECTED_MOVE_COUNT)
    )

    actual_ids = set(by_id)

    if actual_ids != expected_ids:
        die(
            "canonical IDs are not exactly 0..847; "
            "missing="
            + repr(
                sorted(
                    expected_ids
                    - actual_ids
                )
            )
            + " extra="
            + repr(
                sorted(
                    actual_ids
                    - expected_ids
                )
            )
        )

    distribution = Counter(
        entry["cost"]
        for _, entry in by_id.values()
    )

    actual_distribution = {
        cost: distribution.get(
            cost,
            0,
        )
        for cost in range(7)
    }

    if (
        actual_distribution
        != EXPECTED_DISTRIBUTION
    ):
        die(
            "canonical distribution mismatch: "
            + repr(actual_distribution)
        )

    if by_id[0][0] != "MOVE_NONE":
        die(
            "numeric ID 0 must be MOVE_NONE"
        )

    if by_id[0][1]["cost"] != 0:
        die(
            "MOVE_NONE must cost 0"
        )

    if (
        moves["MOVE_STRUGGLE"][
            "numeric_id"
        ]
        != 165
    ):
        die(
            "MOVE_STRUGGLE must remain ID 165"
        )

    if (
        moves["MOVE_STRUGGLE"]["cost"]
        != 0
    ):
        die(
            "MOVE_STRUGGLE must cost 0"
        )

    return by_id


def resolve_current_move_ids(constants):
    """
    Compile the canonical constants against the
    current Expansion moves.h.

    This catches:
      - removed/renamed constants
      - numeric ID drift
      - MOVES_COUNT drift
      - aliases entering the canonical roster
    """

    source = [
        "#include <stdio.h>",
        '#include "constants/moves.h"',
        "",
        "int main(void)",
        "{",
        (
            '    printf("__MOVES_COUNT__ %d\\n", '
            'MOVES_COUNT);'
        ),
    ]

    for constant in constants:
        source.append(
            '    printf("'
            + constant
            + ' %d\\n", '
            + constant
            + ");"
        )

    source += [
        "    return 0;",
        "}",
        "",
    ]

    with tempfile.TemporaryDirectory() as d:
        temp = Path(d)

        c_path = (
            temp
            / "verify_stamina_move_ids.c"
        )

        exe_path = (
            temp
            / "verify_stamina_move_ids"
        )

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
            print(
                compile_result.stdout
            )
            print(
                compile_result.stderr
            )

            die(
                "failed to compile current "
                "move-ID verifier"
            )

        run_result = subprocess.run(
            [str(exe_path)],
            capture_output=True,
            text=True,
        )

        if run_result.returncode != 0:
            print(run_result.stdout)
            print(run_result.stderr)

            die(
                "current move-ID verifier "
                "failed"
            )

    mapping = {}
    moves_count = None

    for line in (
        run_result.stdout.splitlines()
    ):
        name, value_text = line.split()

        value = int(value_text)

        if name == "__MOVES_COUNT__":
            moves_count = value
        else:
            mapping[name] = value

    if moves_count != EXPECTED_MOVE_COUNT:
        die(
            "current MOVES_COUNT="
            + str(moves_count)
            + ", expected "
            + str(EXPECTED_MOVE_COUNT)
        )

    if len(mapping) != EXPECTED_MOVE_COUNT:
        die(
            "current resolved map has "
            + str(len(mapping))
            + " entries"
        )

    return mapping


def validate_source_identity(
    by_id,
    current_ids,
):
    reverse = {}

    for constant, numeric_id in (
        current_ids.items()
    ):
        reverse.setdefault(
            numeric_id,
            [],
        ).append(constant)

    aliases = {
        numeric_id: names
        for numeric_id, names
        in reverse.items()
        if len(names) != 1
    }

    if aliases:
        die(
            "canonical runtime constants "
            "contain numeric aliases: "
            + repr(aliases)
        )

    for numeric_id in range(
        EXPECTED_MOVE_COUNT
    ):
        constant, _ = by_id[numeric_id]

        current_id = current_ids.get(
            constant
        )

        if current_id is None:
            die(
                constant
                + ": absent from current "
                "moves.h"
            )

        if current_id != numeric_id:
            die(
                constant
                + ": canonical ID "
                + str(numeric_id)
                + " != current ID "
                + str(current_id)
            )


def render_header(by_id):
    source_hash = sha256_file(SOURCE)

    lines = [
        (
            "#ifndef "
            "GUARD_DATA_STAMINA_MOVE_COSTS_H"
        ),
        (
            "#define "
            "GUARD_DATA_STAMINA_MOVE_COSTS_H"
        ),
        "",
        (
            "// Auto-generated by "
            "tools/stamina/"
            "generate_stamina_cost_table_v2.py."
        ),
        (
            "// Source: "
            "tools/stamina/data/"
            "stamina_moves_v2.json "
            "(FROZEN_V2)."
        ),
        (
            "// Source SHA256: "
            + source_hash
        ),
        "//",
        (
            "// Do not edit this table manually."
        ),
        (
            "// Regenerate it from the "
            "frozen V2 JSON instead."
        ),
        "",
        (
            "const u8 "
            "gStaminaMoveCosts[MOVES_COUNT] ="
        ),
        "{",
    ]

    for numeric_id in range(
        EXPECTED_MOVE_COUNT
    ):
        constant, entry = by_id[
            numeric_id
        ]

        lines.append(
            "    ["
            + constant
            + "] = "
            + str(entry["cost"])
            + ",  // "
            + str(numeric_id)
        )

    lines += [
        "};",
        "",
        (
            "#endif // "
            "GUARD_DATA_STAMINA_MOVE_COSTS_H"
        ),
        "",
    ]

    return "\n".join(lines)


def validate_rendered_header(
    text,
    by_id,
):
    pattern = re.compile(
        r"^\s+\[(MOVE_[A-Z0-9_]+)\]"
        r"\s*=\s*([0-6]),\s*//\s*(\d+)$"
    )

    found = []

    for line in text.splitlines():
        match = pattern.match(line)

        if match:
            found.append(
                (
                    match.group(1),
                    int(match.group(2)),
                    int(match.group(3)),
                )
            )

    if len(found) != EXPECTED_MOVE_COUNT:
        die(
            "rendered table contains "
            + str(len(found))
            + " entries, expected "
            + str(EXPECTED_MOVE_COUNT)
        )

    seen_names = set()
    seen_ids = set()

    for constant, cost, numeric_id in found:
        if constant in seen_names:
            die(
                "rendered duplicate constant: "
                + constant
            )

        if numeric_id in seen_ids:
            die(
                "rendered duplicate ID: "
                + str(numeric_id)
            )

        seen_names.add(constant)
        seen_ids.add(numeric_id)

        expected_constant, entry = (
            by_id[numeric_id]
        )

        if constant != expected_constant:
            die(
                "rendered ID "
                + str(numeric_id)
                + " has "
                + constant
                + ", expected "
                + expected_constant
            )

        if cost != entry["cost"]:
            die(
                constant
                + ": rendered cost "
                + str(cost)
                + " != canonical "
                + str(entry["cost"])
            )

    if seen_ids != set(
        range(EXPECTED_MOVE_COUNT)
    ):
        die(
            "rendered table does not cover "
            "exactly IDs 0..847"
        )


def render_manifest(
    header_text,
    distribution,
):
    manifest = {
        "schema": (
            "firered_stamina_"
            "cost_table_manifest_v2"
        ),
        "schema_version": 2,
        "status": "PASS",
        "move_count": EXPECTED_MOVE_COUNT,
        "runtime_bound": "MOVES_COUNT",
        "sources": {
            "canonical_dataset": (
                "tools/stamina/data/"
                "stamina_moves_v2.json"
            ),
            "move_constants": (
                "include/constants/moves.h"
            ),
        },
        "hashes": {
            "canonical_dataset_sha256":
                sha256_file(SOURCE),
            "moves_h_sha256":
                sha256_file(MOVES_H),
            "generated_header_sha256":
                sha256_bytes(
                    header_text.encode(
                        "utf-8"
                    )
                ),
        },
        "cost_distribution": {
            str(cost): distribution[cost]
            for cost in range(7)
        },
        "checks": [
            (
                "canonical roster contains "
                "848 entries"
            ),
            (
                "canonical IDs cover "
                "exactly 0..847"
            ),
            (
                "current MOVES_COUNT is 848"
            ),
            (
                "all canonical constants "
                "compile against current "
                "moves.h"
            ),
            (
                "all current numeric IDs "
                "match frozen canonical IDs"
            ),
            (
                "runtime table has exactly "
                "848 explicit initializers"
            ),
            (
                "MOVE_NONE and "
                "MOVE_STRUGGLE cost 0"
            ),
            (
                "no runtime default is "
                "required for ordinary moves"
            ),
        ],
    }

    return (
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def main():
    print(
        "=== OBJECTIVE 02B — "
        "GENERATE STAMINA COST TABLE ==="
    )

    _, moves = load_source()

    by_id = validate_canonical_moves(
        moves
    )

    constants = [
        by_id[numeric_id][0]
        for numeric_id in range(
            EXPECTED_MOVE_COUNT
        )
    ]

    current_ids = (
        resolve_current_move_ids(
            constants
        )
    )

    validate_source_identity(
        by_id,
        current_ids,
    )

    print(
        "Canonical moves     :",
        len(by_id),
    )

    print(
        "Current MOVES_COUNT :",
        EXPECTED_MOVE_COUNT,
    )

    print(
        "Current ID mapping  : PASS"
    )

    header_text = render_header(
        by_id
    )

    validate_rendered_header(
        header_text,
        by_id,
    )

    distribution = Counter(
        entry["cost"]
        for _, entry in by_id.values()
    )

    manifest_text = render_manifest(
        header_text,
        distribution,
    )

    atomic_write(
        OUTPUT,
        header_text,
    )

    atomic_write(
        MANIFEST,
        manifest_text,
    )

    # Verify the bytes actually published.
    published = OUTPUT.read_text(
        encoding="utf-8",
    )

    if published != header_text:
        die(
            "published header differs from "
            "validated generated output"
        )

    validate_rendered_header(
        published,
        by_id,
    )

    print()
    print("Cost distribution:")

    for cost in range(7):
        print(
            "  cost "
            + str(cost)
            + ": "
            + str(distribution[cost])
        )

    print()
    print("Generated:")
    print(
        "  "
        + str(
            OUTPUT.relative_to(ROOT)
        )
    )

    print(
        "  "
        + str(
            MANIFEST.relative_to(ROOT)
        )
    )

    print()
    print("OBJECTIVE 02B: PASS")
    print(
        "848 / 848 explicit runtime "
        "Stamina table entries generated."
    )


if __name__ == "__main__":
    main()
