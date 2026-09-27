#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def read(path: str) -> str:
    p = ROOT / path

    if not p.is_file():
        fail(
            "missing file: "
            + path
        )

    return p.read_text(
        encoding="utf-8",
    )


def require(
    path: str,
    needle: str,
    count: int = 1,
) -> None:
    actual = read(path).count(
        needle
    )

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


print(
    "=== OBJECTIVE 06 VALIDATION ==="
)

# ------------------------------------------------------------
# API
# ------------------------------------------------------------

require(
    "include/battle_stamina.h",
    "void RegeneratePlayerStamina(void);",
)

require(
    "src/battle_stamina.c",
    "void RegeneratePlayerStamina(void)",
)

# ------------------------------------------------------------
# Regeneration semantics
# ------------------------------------------------------------

require(
    "src/battle_stamina.c",
    "if (!IsPlayerStaminaEnabled())",
)

require(
    "src/battle_stamina.c",
    (
        "stamina = "
        "gBattleStruct->playerStamina "
        "+ BATTLE_STAMINA_REGEN;"
    ),
)

require(
    "src/battle_stamina.c",
    "if (stamina > BATTLE_STAMINA_MAX)",
)

require(
    "src/battle_stamina.c",
    "stamina = BATTLE_STAMINA_MAX;",
)

require(
    "src/battle_stamina.c",
    "gBattleStruct->playerStamina = stamina;",
)

# ------------------------------------------------------------
# Hook location
# ------------------------------------------------------------

battle_main = read(
    "src/battle_main.c"
)

require(
    "src/battle_main.c",
    '#include "battle_stamina.h"',
)

require(
    "src/battle_main.c",
    "RegeneratePlayerStamina();",
)

start = battle_main.find(
    "bool32 EndTurnEvents(void)"
)

if start == -1:
    fail(
        "EndTurnEvents not found"
    )

end = battle_main.find(
    "\nu8 IsRunningFromBattleImpossible",
    start,
)

if end == -1:
    fail(
        "EndTurnEvents end boundary not found"
    )

body = battle_main[start:end]

if body.count(
    "RegeneratePlayerStamina();"
) != 1:
    fail(
        "EndTurnEvents must contain exactly "
        "one regeneration call"
    )

outcome_pos = body.find(
    "if (gBattleOutcome != 0)"
)

regen_pos = body.find(
    "RegeneratePlayerStamina();"
)

counter_pos = body.find(
    "if (gBattleResults.battleTurnCounter < 0xFF)"
)

cleanup_pos = body.find(
    "TurnValuesCleanUp(FALSE);"
)

if cleanup_pos == -1:
    fail(
        "TurnValuesCleanUp(FALSE) not found"
    )

if outcome_pos == -1:
    fail(
        "battle outcome check not found"
    )

if counter_pos == -1:
    fail(
        "battle turn counter block not found"
    )

if not (
    cleanup_pos
    < outcome_pos
    < regen_pos
    < counter_pos
):
    fail(
        "regeneration hook ordering is wrong: "
        "expected cleanup < outcome < regen < counter"
    )

# ------------------------------------------------------------
# Economy constants remain locked.
# ------------------------------------------------------------

require(
    "include/constants/battle.h",
    "#define BATTLE_STAMINA_MAX    6",
)

require(
    "include/constants/battle.h",
    "#define BATTLE_STAMINA_REGEN  2",
)

# ------------------------------------------------------------
# There must be no switch-based refill.
# ------------------------------------------------------------

for path in (
    "src/battle_main.c",
    "src/battle_util.c",
    "src/battle_util2.c",
    "src/battle_stamina.c",
):
    contents = read(path)

    # Initialization is allowed exactly once in battle_util2.c.
    if path == "src/battle_util2.c":
        continue

    if (
        "playerStamina = BATTLE_STAMINA_MAX"
        in contents
    ):
        fail(
            "unexpected full Stamina assignment "
            "outside battle initialization: "
            + path
        )


print("Regeneration API          : PASS")
print("Shared pool +2            : PASS")
print("Cap at 6                  : PASS")
print("One hook per turn         : PASS")
print("After end-turn effects    : PASS")
print("After outcome check       : PASS")
print("Before next-turn reset    : PASS")
print("No post-battle regen      : PASS")
print("No switch refill          : PASS")
print()
print(
    "OBJECTIVE 06 VALIDATION: PASS"
)
