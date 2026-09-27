#!/usr/bin/env python3

from pathlib import Path
import re

ROOT = Path(".").resolve()

CONSTANTS_H = ROOT / "include/constants/battle.h"
BATTLE_H = ROOT / "include/battle.h"
UTIL2_C = ROOT / "src/battle_util2.c"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def require_exact_count(
    text: str,
    needle: str,
    expected: int,
    label: str,
) -> None:
    actual = text.count(needle)

    if actual != expected:
        fail(
            label
            + ": expected "
            + str(expected)
            + ", found "
            + str(actual)
        )


print("=== OBJECTIVE 03 VALIDATION ===")

constants = CONSTANTS_H.read_text(
    encoding="utf-8"
)

battle = BATTLE_H.read_text(
    encoding="utf-8"
)

util2 = UTIL2_C.read_text(
    encoding="utf-8"
)

# -------------------------------------------------------------
# Constants
# -------------------------------------------------------------

max_match = re.search(
    r"^#define\s+BATTLE_STAMINA_MAX\s+(\d+)\s*$",
    constants,
    re.MULTILINE,
)

regen_match = re.search(
    r"^#define\s+BATTLE_STAMINA_REGEN\s+(\d+)\s*$",
    constants,
    re.MULTILINE,
)

if max_match is None:
    fail("BATTLE_STAMINA_MAX missing")

if regen_match is None:
    fail("BATTLE_STAMINA_REGEN missing")

max_value = int(max_match.group(1))
regen_value = int(regen_match.group(1))

if max_value != 6:
    fail(
        "BATTLE_STAMINA_MAX="
        + str(max_value)
        + ", expected 6"
    )

if regen_value != 2:
    fail(
        "BATTLE_STAMINA_REGEN="
        + str(regen_value)
        + ", expected 2"
    )

if max_value > 15:
    fail(
        "BATTLE_STAMINA_MAX does not fit "
        "playerStamina:4"
    )

require_exact_count(
    constants,
    "BATTLE_STAMINA_MAX",
    1,
    "BATTLE_STAMINA_MAX definition",
)

require_exact_count(
    constants,
    "BATTLE_STAMINA_REGEN",
    1,
    "BATTLE_STAMINA_REGEN definition",
)

# -------------------------------------------------------------
# BattleStruct
# -------------------------------------------------------------

expected_struct = (
    "    u8 numSpreadTargets:3;\n"
    "    u8 moldBreakerActive:1;\n"
    "    u8 playerStamina:4;\n"
)

require_exact_count(
    battle,
    expected_struct,
    1,
    "BattleStruct Stamina nibble",
)

if (
    "    u8 numSpreadTargets:3;\n"
    "    u8 moldBreakerActive:1;\n"
    "    u8 unused4:4;\n"
    in battle
):
    fail(
        "old BattleStruct unused4 nibble "
        "still present"
    )

require_exact_count(
    battle,
    "playerStamina",
    1,
    "BattleStruct playerStamina field",
)

# -------------------------------------------------------------
# Initialization
# -------------------------------------------------------------

expected_init = (
    "    gBattleStruct = AllocZeroed(sizeof(*gBattleStruct));\n"
    "    gBattleStruct->playerStamina = BATTLE_STAMINA_MAX;\n"
    "    gAiBattleData = AllocZeroed(sizeof(*gAiBattleData));\n"
)

require_exact_count(
    util2,
    expected_init,
    1,
    "battle allocation / Stamina initialization",
)

require_exact_count(
    util2,
    "gBattleStruct->playerStamina = BATTLE_STAMINA_MAX;",
    1,
    "Stamina initialization",
)

print("BATTLE_STAMINA_MAX     : PASS (6)")
print("BATTLE_STAMINA_REGEN   : PASS (2)")
print("playerStamina width    : PASS (4 bits)")
print("BattleStruct reuse     : PASS")
print("Initialization         : PASS")
print("Additional state bytes : 0")
print()
print("OBJECTIVE 03 VALIDATION: PASS")
