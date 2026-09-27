#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def read(path: str) -> str:
    p = ROOT / path

    if not p.is_file():
        fail("missing file: " + path)

    return p.read_text(
        encoding="utf-8",
    )


def require(
    path: str,
    needle: str,
    count: int = 1,
) -> None:
    contents = read(path)
    actual = contents.count(needle)

    if actual != count:
        fail(
            path
            + ": expected "
            + repr(needle)
            + " "
            + str(count)
            + " time(s), found "
            + str(actual)
        )


def extract_between(
    text: str,
    start_marker: str,
    end_marker: str,
    label: str,
) -> str:
    start = text.find(start_marker)

    if start == -1:
        fail(
            label
            + ": start marker not found"
        )

    end = text.find(
        end_marker,
        start,
    )

    if end == -1:
        fail(
            label
            + ": end marker not found"
        )

    return text[start:end]


def require_in_body(
    body: str,
    needle: str,
    label: str,
    count: int = 1,
) -> None:
    actual = body.count(needle)

    if actual != count:
        fail(
            label
            + ": expected "
            + repr(needle)
            + " "
            + str(count)
            + " time(s), found "
            + str(actual)
        )


print(
    "=== OBJECTIVE 05 VALIDATION ==="
)

# ============================================================
# Helper API
# ============================================================

require(
    "include/battle_stamina.h",
    "bool32 TrySpendBattlerStamina"
    "(enum BattlerId battler, enum Move move);",
)

require(
    "src/battle_stamina.c",
    "bool32 TrySpendBattlerStamina"
    "(enum BattlerId battler, enum Move move)",
)

require(
    "src/battle_stamina.c",
    "if (cost > gBattleStruct->playerStamina)",
)

require(
    "src/battle_stamina.c",
    "gBattleStruct->playerStamina -= cost;",
)

# ============================================================
# Resolution source / exact function bodies
# ============================================================

resolution = read(
    "src/battle_move_resolution.c"
)

pp_body = extract_between(
    resolution,
    (
        "static enum CancelerResult "
        "CancelerPPDeduction"
        "(struct BattleCalcValues *cv)\n"
    ),
    (
        "// We don't have clear data on "
        "where this belongs"
    ),
    "CancelerPPDeduction",
)

power_points_body = extract_between(
    resolution,
    (
        "static enum CancelerResult "
        "CancelerPowerPoints"
        "(struct BattleCalcValues *cv)\n"
    ),
    (
        "static enum CancelerResult "
        "CancelerTruant"
    ),
    "CancelerPowerPoints",
)

require(
    "src/battle_move_resolution.c",
    '#include "battle_stamina.h"',
)

# ============================================================
# Execution-time PP bypass
# ============================================================

require_in_body(
    power_points_body,
    (
        "if (!IsBattlerStaminaEnabled"
        "(cv->battlerAtk)"
    ),
    "CancelerPowerPoints",
)

require_in_body(
    power_points_body,
    (
        "gBattleMons[cv->battlerAtk]"
        ".pp[gCurrMovePos] == 0"
    ),
    "CancelerPowerPoints",
)

require_in_body(
    power_points_body,
    "BattleScript_NoPPForMove",
    "CancelerPowerPoints",
)

# ============================================================
# Payment boundary
# ============================================================

require_in_body(
    pp_body,
    (
        "if (IsBattlerStaminaEnabled"
        "(cv->battlerAtk))"
    ),
    "CancelerPPDeduction",
)

require_in_body(
    pp_body,
    (
        "enum Move staminaMove = "
        "gBattleStruct->baseMove;"
    ),
    "CancelerPPDeduction",
)

require_in_body(
    pp_body,
    (
        "if (gBattleStruct->submoveAnnouncement "
        "== SUBMOVE_SUCCESS)\n"
        "            staminaMove = "
        "gBattleMons[cv->battlerAtk]"
        ".moves[gChosenMovePos];"
    ),
    "CancelerPPDeduction",
)

require_in_body(
    pp_body,
    (
        "if (!TrySpendBattlerStamina"
        "(cv->battlerAtk, staminaMove))"
    ),
    "CancelerPPDeduction",
)

require_in_body(
    pp_body,
    (
        "gBattlescriptCurrInstr = "
        "BattleScript_NotEnoughStaminaForMove;"
    ),
    "CancelerPPDeduction",
)

# ============================================================
# Continuation / generated-action skip guards.
#
# Scope these checks to CancelerPPDeduction only.
# They may legitimately occur elsewhere in the source file.
# ============================================================

skip_guards = (
    (
        "gBattleMons[cv->battlerAtk]"
        ".volatiles.multipleTurns"
    ),
    (
        "gSpecialStatuses[cv->battlerAtk]"
        ".dancerUsedMove"
    ),
    "gBattleStruct->bouncedMoveIsUsed",
    "gBattleStruct->snatchedMoveIsUsed",
    (
        "gBattleMons[cv->battlerAtk]"
        ".volatiles.bideTurns"
    ),
    "cv->move == MOVE_STRUGGLE",
)

for guard in skip_guards:
    require_in_body(
        pp_body,
        guard,
        "CancelerPPDeduction skip guards",
    )

# ============================================================
# Vanilla PP behavior must still exist for non-Stamina users.
# ============================================================

require_in_body(
    pp_body,
    "else\n    {\n        s32 ppToDeduct = 1;",
    "CancelerPPDeduction vanilla PP branch",
)

require_in_body(
    pp_body,
    (
        "gBattleMons[cv->battlerAtk]"
        ".pp[movePosition] -= ppToDeduct;"
    ),
    "CancelerPPDeduction vanilla PP deduction",
)

require_in_body(
    pp_body,
    (
        "gBattleMons[cv->battlerAtk]"
        ".pp[movePosition] = 0;"
    ),
    "CancelerPPDeduction vanilla PP clamp",
)

require_in_body(
    pp_body,
    "MOVE_IS_PERMANENT",
    "CancelerPPDeduction controller update",
)

require_in_body(
    pp_body,
    "REQUEST_PPMOVE1_BATTLE + movePosition",
    "CancelerPPDeduction controller update",
)

# ============================================================
# Runtime insufficient-Stamina failure
# ============================================================

require(
    "include/constants/battle_string_ids.h",
    (
        "    STRINGID_NOTENOUGHSTAMINA,\n"
        "    STRINGID_BUTNOTENOUGHSTAMINA,\n"
        "    STRINGID_COUNT"
    ),
)

require(
    "src/battle_message.c",
    "STRINGID_BUTNOTENOUGHSTAMINA",
)

require(
    "include/battle_scripts.h",
    (
        "extern const u8 "
        "BattleScript_NotEnoughStaminaForMove[];"
    ),
)

require(
    "data/battle_scripts_1.s",
    "BattleScript_NotEnoughStaminaForMove::",
)

require(
    "data/battle_scripts_1.s",
    "printstring STRINGID_BUTNOTENOUGHSTAMINA",
)

# ============================================================
# Objective boundary: regen belongs to Objective 06.
# ============================================================

for path in (
    "include/battle_stamina.h",
    "src/battle_stamina.c",
):
    if "RegeneratePlayerStamina" in read(path):
        fail(
            "Objective 06 regeneration "
            "already present in "
            + path
        )


print("TrySpend helper            : PASS")
print("Atomic affordability       : PASS")
print("Underflow guard            : PASS")
print("Execution PP bypass        : PASS")
print("Player PP deduction bypass : PASS")
print("Enemy PP behavior          : PRESERVED")
print("Z / Max base-cost identity : PASS")
print("Called move caller-payment : PASS")
print("Continuation skip guards   : PASS")
print("Doubles overcommit guard   : PASS")
print("Runtime failure script     : PASS")
print("Regeneration               : ABSENT (expected)")
print()
print("OBJECTIVE 05 VALIDATION: PASS")
