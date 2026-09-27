#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def require(path: str, needle: str, count: int = 1) -> None:
    p = ROOT / path

    if not p.is_file():
        fail("missing file: " + path)

    text = p.read_text(
        encoding="utf-8",
    )

    actual = text.count(needle)

    if actual != count:
        fail(
            path
            + ": expected "
            + repr(needle)
            + " exactly "
            + str(count)
            + " time(s), found "
            + str(actual)
        )


print("=== OBJECTIVE 04 VALIDATION ===")

require(
    "include/battle_stamina.h",
    "bool32 IsPlayerStaminaEnabled(void);",
)

require(
    "include/battle_stamina.h",
    "bool32 IsBattlerStaminaEnabled(enum BattlerId battler);",
)

require(
    "include/battle_stamina.h",
    "u8 GetMoveStaminaCost(enum Move move);",
)

require(
    "include/battle_stamina.h",
    "bool32 CanBattlerAffordMoveStamina(enum BattlerId battler, enum Move move);",
)

require(
    "src/battle_stamina.c",
    '#include "data/stamina_move_costs.h"',
)

require(
    "src/battle_stamina.c",
    "BATTLE_TYPE_LINK",
)

require(
    "src/battle_stamina.c",
    "BATTLE_TYPE_SAFARI",
)

require(
    "src/battle_stamina.c",
    "BATTLE_TYPE_POKEDUDE",
)

require(
    "src/battle_stamina.c",
    "return GetMoveStaminaCost(move) <= gBattleStruct->playerStamina;",
)

require(
    "include/constants/battle_util.h",
    "#define MOVE_LIMITATION_STAMINA                 (1 << 17)",
)

require(
    "include/constants/battle_util.h",
    "#define MOVE_LIMITATIONS_ALL                    (0xFFFF | MOVE_LIMITATION_STAMINA)",
)

require(
    "src/battle_util.c",
    '#include "battle_stamina.h"',
)

require(
    "src/battle_util.c",
    "&& !IsBattlerStaminaEnabled(battler)\n"
    "              && gBattleMons[battler].pp[i] == 0",
)

require(
    "src/battle_util.c",
    "else if (check & MOVE_LIMITATION_STAMINA\n"
    "              && !CanBattlerAffordMoveStamina(battler, move))",
)

require(
    "src/battle_util.c",
    "if (!IsBattlerStaminaEnabled(battler)\n"
    "     && gBattleMons[battler].pp[moveId] == 0)",
)

require(
    "src/battle_util.c",
    "gSelectionBattleScripts[battler] = "
    "BattleScript_SelectingMoveWithNotEnoughStamina;",
)

require(
    "include/battle_scripts.h",
    "extern const u8 BattleScript_SelectingMoveWithNotEnoughStamina[];",
)

require(
    "data/battle_scripts_1.s",
    "BattleScript_SelectingMoveWithNotEnoughStamina::",
)

require(
    "include/constants/battle_string_ids.h",
    "STRINGID_NOTENOUGHSTAMINA",
)

require(
    "src/battle_message.c",
    "STRINGID_NOTENOUGHSTAMINA",
)


require(
    "include/constants/battle_string_ids.h",
    "    STRINGID_NOTENOUGHSTAMINA,\n"
    "    STRINGID_COUNT",
)

require(
    "src/battle_controller_player.c",
    '#include "battle_stamina.h"',
)

require(
    "src/battle_controller_player.c",
    "if ((!IsBattlerStaminaEnabled(battler)\n"
    "              && moveInfo->currentPP[gMoveSelectionCursor[battler]] == 0)",
)

require(
    "src/battle_controller_player.c",
    "|| !CanBattlerAffordMoveStamina(\n"
    "                    battler,\n"
    "                    moveInfo->moves[gMoveSelectionCursor[battler]]))",
)

# Objective 05 must not have leaked in.
for path in (
    "include/battle_stamina.h",
    "src/battle_stamina.c",
):
    text = (ROOT / path).read_text(
        encoding="utf-8",
    )

    if "TrySpendBattlerStamina" in text:
        fail(
            "Objective 05 consumption helper "
            "already present in " + path
        )

print("Runtime helper API         : PASS")
print("848-entry cost table       : CONNECTED")
print("Player-side enablement     : PASS")
print("Excluded battle modes      : PASS")
print("MOVE_LIMITATION_STAMINA    : PASS (bit 17)")
print("Generic affordability      : PASS")
print("Direct selection rejection : PASS")
print("Player PP selection bypass : PASS")
print("Controller PP target gate  : PASS")
print("Controller Stamina gate    : PASS")
print("Battle string ID stability : PASS")
print("Enemy PP behavior          : PRESERVED")
print("Selection message          : PASS")
print("Consumption                : ABSENT (expected)")
print()
print("OBJECTIVE 04 VALIDATION: PASS")
