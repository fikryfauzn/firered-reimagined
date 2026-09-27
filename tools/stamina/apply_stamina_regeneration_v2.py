#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

STAMINA_H = ROOT / "include/battle_stamina.h"
STAMINA_C = ROOT / "src/battle_stamina.c"
BATTLE_MAIN_C = ROOT / "src/battle_main.c"


def die(message: str) -> None:
    raise SystemExit("ERROR: " + message)


def replace_once(
    path: Path,
    old: str,
    new: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    if new in text:
        return

    count = text.count(old)

    if count != 1:
        die(
            str(path.relative_to(ROOT))
            + ": expected exactly one anchor, found "
            + str(count)
        )

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )


print(
    "=== OBJECTIVE 06 — "
    "STAMINA REGENERATION ==="
)

for path in (
    STAMINA_H,
    STAMINA_C,
    BATTLE_MAIN_C,
):
    if not path.is_file():
        die(
            "missing required file: "
            + str(path)
        )


# ============================================================
# 1. Public regeneration helper.
# ============================================================

replace_once(
    STAMINA_H,
    "bool32 TrySpendBattlerStamina"
    "(enum BattlerId battler, enum Move move);\n",
    "bool32 TrySpendBattlerStamina"
    "(enum BattlerId battler, enum Move move);\n"
    "void RegeneratePlayerStamina(void);\n",
)


# ============================================================
# 2. Runtime regeneration implementation.
#
# Shared player-side pool:
#   current + 2
#   capped at 6
#
# Disabled battle modes receive no Stamina mutation.
# ============================================================

text = STAMINA_C.read_text(
    encoding="utf-8",
)

if "void RegeneratePlayerStamina(void)" not in text:
    addition = '''
void RegeneratePlayerStamina(void)
{
    u8 stamina;

    if (!IsPlayerStaminaEnabled())
        return;

    stamina = gBattleStruct->playerStamina + BATTLE_STAMINA_REGEN;

    if (stamina > BATTLE_STAMINA_MAX)
        stamina = BATTLE_STAMINA_MAX;

    gBattleStruct->playerStamina = stamina;
}
'''

    STAMINA_C.write_text(
        text.rstrip()
        + "\n"
        + addition,
        encoding="utf-8",
    )


# ============================================================
# 3. battle_main.c include.
# ============================================================

replace_once(
    BATTLE_MAIN_C,
    '#include "battle.h"\n',
    '#include "battle.h"\n'
    '#include "battle_stamina.h"\n',
)


# ============================================================
# 4. End-of-turn hook.
#
# Insert AFTER battle-outcome early return so no regeneration
# occurs after a battle has finished.
#
# Insert BEFORE battleTurnCounter/reset work so this remains
# part of completing the current turn.
# ============================================================

old = '''    if (gBattleOutcome != 0)
    {
        gCurrentActionFuncId = B_ACTION_FINISHED;
        SetBattleCallback(RunTurnActionsFunctions);
        return FALSE;
    }

    if (gBattleResults.battleTurnCounter < 0xFF)
'''

new = '''    if (gBattleOutcome != 0)
    {
        gCurrentActionFuncId = B_ACTION_FINISHED;
        SetBattleCallback(RunTurnActionsFunctions);
        return FALSE;
    }

    RegeneratePlayerStamina();

    if (gBattleResults.battleTurnCounter < 0xFF)
'''

replace_once(
    BATTLE_MAIN_C,
    old,
    new,
)


print("Regeneration helper       : added")
print("Per completed turn        : +2")
print("Maximum                   : 6")
print("Shared player-side pool   : yes")
print("Singles / doubles rate    : identical")
print("After battle outcome      : no regeneration")
print("Switch refill             : none")
print()
print("OBJECTIVE 06 PATCH: APPLIED")
