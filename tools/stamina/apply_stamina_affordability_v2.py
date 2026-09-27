#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

UTIL_CONSTANTS_H = ROOT / "include/constants/battle_util.h"
BATTLE_STAMINA_H = ROOT / "include/battle_stamina.h"
BATTLE_STAMINA_C = ROOT / "src/battle_stamina.c"
BATTLE_UTIL_C = ROOT / "src/battle_util.c"
PLAYER_CONTROLLER_C = ROOT / "src/battle_controller_player.c"
BATTLE_SCRIPTS_H = ROOT / "include/battle_scripts.h"
BATTLE_SCRIPTS_S = ROOT / "data/battle_scripts_1.s"
STRING_IDS_H = ROOT / "include/constants/battle_string_ids.h"
BATTLE_MESSAGE_C = ROOT / "src/battle_message.c"
COST_TABLE = ROOT / "src/data/stamina_move_costs.h"


def die(message: str) -> None:
    raise SystemExit("ERROR: " + message)


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")

    if new in text:
        return

    count = text.count(old)

    if count != 1:
        die(
            str(path.relative_to(ROOT))
            + ": expected exactly one patch anchor, found "
            + str(count)
            + ". Refusing to guess."
        )

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )


def write_new_file(path: Path, content: str) -> None:
    if path.exists():
        current = path.read_text(encoding="utf-8")

        if current == content:
            return

        die(
            str(path.relative_to(ROOT))
            + ": already exists with unexpected contents"
        )

    path.write_text(
        content,
        encoding="utf-8",
    )


def main() -> None:
    print("=== OBJECTIVE 04 — STAMINA AFFORDABILITY ===")

    required = (
        UTIL_CONSTANTS_H,
        BATTLE_UTIL_C,
        PLAYER_CONTROLLER_C,
        BATTLE_SCRIPTS_H,
        BATTLE_SCRIPTS_S,
        STRING_IDS_H,
        BATTLE_MESSAGE_C,
        COST_TABLE,
    )

    for path in required:
        if not path.is_file():
            die("missing required file: " + str(path))

    battle_h = (
        ROOT / "include/battle.h"
    ).read_text(encoding="utf-8")

    if "u8 playerStamina:4;" not in battle_h:
        die(
            "Objective 03 missing: "
            "BattleStruct::playerStamina not found"
        )

    util2 = (
        ROOT / "src/battle_util2.c"
    ).read_text(encoding="utf-8")

    if (
        "gBattleStruct->playerStamina = "
        "BATTLE_STAMINA_MAX;"
        not in util2
    ):
        die(
            "Objective 03 missing: "
            "battle Stamina initialization not found"
        )

    # ---------------------------------------------------------
    # Runtime helper module.
    # ---------------------------------------------------------

    header = '''#ifndef GUARD_BATTLE_STAMINA_H
#define GUARD_BATTLE_STAMINA_H

#include "global.h"

bool32 IsPlayerStaminaEnabled(void);
bool32 IsBattlerStaminaEnabled(enum BattlerId battler);
u8 GetMoveStaminaCost(enum Move move);
bool32 CanBattlerAffordMoveStamina(enum BattlerId battler, enum Move move);

#endif // GUARD_BATTLE_STAMINA_H
'''

    source = '''#include "global.h"
#include "battle.h"
#include "battle_stamina.h"
#include "constants/battle.h"
#include "constants/moves.h"

#include "data/stamina_move_costs.h"

bool32 IsPlayerStaminaEnabled(void)
{
    if (gBattleTypeFlags & (BATTLE_TYPE_LINK
                          | BATTLE_TYPE_SAFARI
                          | BATTLE_TYPE_POKEDUDE))
    {
        return FALSE;
    }

    return TRUE;
}

bool32 IsBattlerStaminaEnabled(enum BattlerId battler)
{
    return IsPlayerStaminaEnabled()
        && IsOnPlayerSide(battler);
}

u8 GetMoveStaminaCost(enum Move move)
{
    if (move >= MOVES_COUNT)
        return 0;

    return gStaminaMoveCosts[move];
}

bool32 CanBattlerAffordMoveStamina(enum BattlerId battler, enum Move move)
{
    if (!IsBattlerStaminaEnabled(battler))
        return TRUE;

    if (move >= MOVES_COUNT)
        return FALSE;

    return GetMoveStaminaCost(move) <= gBattleStruct->playerStamina;
}
'''

    write_new_file(
        BATTLE_STAMINA_H,
        header,
    )

    write_new_file(
        BATTLE_STAMINA_C,
        source,
    )

    # ---------------------------------------------------------
    # Limitation bit.
    #
    # Existing normal aggregate = bits 0..15.
    # Placeholder is bit 16 but intentionally outside ALL.
    # Stamina gets bit 17 and IS part of normal ALL checks.
    # ---------------------------------------------------------

    replace_once(
        UTIL_CONSTANTS_H,
        "#define MOVE_LIMITATION_PLACEHOLDER             (1 << 16)\n"
        "#define MOVE_LIMITATIONS_ALL                    0xFFFF\n",
        "#define MOVE_LIMITATION_PLACEHOLDER             (1 << 16)\n"
        "#define MOVE_LIMITATION_STAMINA                 (1 << 17)\n"
        "#define MOVE_LIMITATIONS_ALL                    (0xFFFF | MOVE_LIMITATION_STAMINA)\n",
    )

    # ---------------------------------------------------------
    # battle_util.c include.
    # ---------------------------------------------------------

    replace_once(
        BATTLE_UTIL_C,
        '#include "battle_util.h"\n',
        '#include "battle_util.h"\n'
        '#include "battle_stamina.h"\n',
    )

    # ---------------------------------------------------------
    # Direct player selection:
    #
    # PP is inert as the player's normal battle resource.
    # Opponents / excluded battle modes retain vanilla PP.
    #
    # Stamina gets an equivalent hard rejection.
    # ---------------------------------------------------------

    old_selection = '''    if (gBattleMons[battler].pp[moveId] == 0)
    {
        if (gBattleTypeFlags & BATTLE_TYPE_PALACE)
        {
            gProtectStructs[battler].palaceUnableToUseMove = TRUE;
        }
        else
        {
            gSelectionBattleScripts[battler] = BattleScript_SelectingMoveWithNoPP;
            limitations++;
        }
    }

    if (moveEffect == EFFECT_PLACEHOLDER)
'''

    new_selection = '''    if (!IsBattlerStaminaEnabled(battler)
     && gBattleMons[battler].pp[moveId] == 0)
    {
        if (gBattleTypeFlags & BATTLE_TYPE_PALACE)
        {
            gProtectStructs[battler].palaceUnableToUseMove = TRUE;
        }
        else
        {
            gSelectionBattleScripts[battler] = BattleScript_SelectingMoveWithNoPP;
            limitations++;
        }
    }

    if (!CanBattlerAffordMoveStamina(battler, move))
    {
        if (gBattleTypeFlags & BATTLE_TYPE_PALACE)
        {
            gProtectStructs[battler].palaceUnableToUseMove = TRUE;
        }
        else
        {
            gSelectionBattleScripts[battler] = BattleScript_SelectingMoveWithNotEnoughStamina;
            limitations++;
        }
    }

    if (moveEffect == EFFECT_PLACEHOLDER)
'''

    replace_once(
        BATTLE_UTIL_C,
        old_selection,
        new_selection,
    )

    # ---------------------------------------------------------
    # Generic move limitation system.
    # ---------------------------------------------------------

    old_generic = '''        // No PP
        else if (check & MOVE_LIMITATION_PP && gBattleMons[battler].pp[i] == 0)
            unusableMoves |= 1u << i;
        // Placeholder
'''

    new_generic = '''        // No PP (opponents and non-Stamina battle modes only)
        else if (check & MOVE_LIMITATION_PP
              && !IsBattlerStaminaEnabled(battler)
              && gBattleMons[battler].pp[i] == 0)
            unusableMoves |= 1u << i;
        // Not enough shared player-side Stamina
        else if (check & MOVE_LIMITATION_STAMINA
              && !CanBattlerAffordMoveStamina(battler, move))
            unusableMoves |= 1u << i;
        // Placeholder
'''

    replace_once(
        BATTLE_UTIL_C,
        old_generic,
        new_generic,
    )

    # ---------------------------------------------------------
    # Player target-selection gate.
    #
    # Vanilla blocks target selection at PP=0 in doubles.
    # In Stamina mode, stored PP must not govern usability;
    # instead use the shared Stamina affordability check.
    # ---------------------------------------------------------

    replace_once(
        PLAYER_CONTROLLER_C,
        '#include "battle.h"\n',
        '#include "battle.h"\n'
        '#include "battle_stamina.h"\n',
    )

    replace_once(
        PLAYER_CONTROLLER_C,
        "            if (moveInfo->currentPP[gMoveSelectionCursor[battler]] == 0)\n"
        "            {\n"
        "                canSelectTarget = 0;\n"
        "            }\n"
        "            else if (isUserOrAlly && !IsBattlerAlive(partner))\n",
        "            if ((!IsBattlerStaminaEnabled(battler)\n"
        "              && moveInfo->currentPP[gMoveSelectionCursor[battler]] == 0)\n"
        "             || !CanBattlerAffordMoveStamina(\n"
        "                    battler,\n"
        "                    moveInfo->moves[gMoveSelectionCursor[battler]]))\n"
        "            {\n"
        "                canSelectTarget = 0;\n"
        "            }\n"
        "            else if (isUserOrAlly && !IsBattlerAlive(partner))\n",
    )

    # ---------------------------------------------------------
    # Selection message/script.
    # ---------------------------------------------------------

    replace_once(
        BATTLE_SCRIPTS_H,
        "extern const u8 BattleScript_SelectingMoveWithNoPP[];\n"
        "extern const u8 BattleScript_NoPPForMove[];\n",
        "extern const u8 BattleScript_SelectingMoveWithNoPP[];\n"
        "extern const u8 BattleScript_SelectingMoveWithNotEnoughStamina[];\n"
        "extern const u8 BattleScript_NoPPForMove[];\n",
    )

    replace_once(
        BATTLE_SCRIPTS_S,
        "BattleScript_SelectingMoveWithNoPP::\n"
        "\tprintselectionstring STRINGID_NOPPLEFT\n"
        "\tendselectionscript\n"
        "\n"
        "BattleScript_NoPPForMove::\n",
        "BattleScript_SelectingMoveWithNoPP::\n"
        "\tprintselectionstring STRINGID_NOPPLEFT\n"
        "\tendselectionscript\n"
        "\n"
        "BattleScript_SelectingMoveWithNotEnoughStamina::\n"
        "\tprintselectionstring STRINGID_NOTENOUGHSTAMINA\n"
        "\tendselectionscript\n"
        "\n"
        "BattleScript_NoPPForMove::\n",
    )

    string_id_text = STRING_IDS_H.read_text(
        encoding="utf-8",
    )

    if "STRINGID_NOTENOUGHSTAMINA" not in string_id_text:
        string_id_lines = string_id_text.splitlines(
            keepends=True,
        )

        count_matches = [
            i
            for i, line in enumerate(string_id_lines)
            if line.strip() == "STRINGID_COUNT"
        ]

        if len(count_matches) != 1:
            die(
                "battle_string_ids.h: expected exactly "
                "one STRINGID_COUNT"
            )

        string_id_lines.insert(
            count_matches[0],
            "    STRINGID_NOTENOUGHSTAMINA,\n",
        )

        STRING_IDS_H.write_text(
            "".join(string_id_lines),
            encoding="utf-8",
        )

    message_text = BATTLE_MESSAGE_C.read_text(
        encoding="utf-8",
    )

    if "STRINGID_NOTENOUGHSTAMINA" not in message_text:
        message_lines = message_text.splitlines(
            keepends=True,
        )

        message_matches = [
            i
            for i, line in enumerate(message_lines)
            if "[STRINGID_BUTNOPPLEFT]" in line
        ]

        if len(message_matches) != 1:
            die(
                "src/battle_message.c: expected exactly "
                "one STRINGID_BUTNOPPLEFT table entry, found "
                + str(len(message_matches))
            )

        stamina_message = (
            "    [STRINGID_NOTENOUGHSTAMINA]                     = "
            "COMPOUND_STRING(\"There's not enough Stamina "
            "for this move!\\p\"),\n"
        )

        message_lines.insert(
            message_matches[0] + 1,
            stamina_message,
        )

        BATTLE_MESSAGE_C.write_text(
            "".join(message_lines),
            encoding="utf-8",
        )

    print("Runtime helper module       : added")
    print("Runtime cost table          : connected")
    print("Stamina limitation bit      : bit 17")
    print("Player-side PP selection    : bypassed")
    print("Hard affordability          : enabled")
    print("Enemy PP behavior           : unchanged")
    print("Selection message           : added")
    print("Stamina consumption         : NOT implemented")
    print()
    print("OBJECTIVE 04 PATCH: APPLIED")


if __name__ == "__main__":
    main()
