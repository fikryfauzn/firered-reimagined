#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

CONTROLLER_C = ROOT / "src/battle_controller_player.c"
MESSAGE_C = ROOT / "src/battle_message.c"
MESSAGE_H = ROOT / "include/battle_message.h"
ZMOVE_C = ROOT / "src/battle_z_move.c"


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
            + ": expected exactly one anchor, found "
            + str(count)
        )

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )


print("=== OBJECTIVE 07A — STAMINA BATTLE UI ===")

for path in (
    CONTROLLER_C,
    MESSAGE_C,
    MESSAGE_H,
    ZMOVE_C,
):
    if not path.is_file():
        die("missing required file: " + str(path))


# ============================================================
# 1. Shared UI strings.
# ============================================================

replace_once(
    MESSAGE_C,
    'const u8 gText_MoveInterfacePP[] = _("PP ");\n',
    'const u8 gText_MoveInterfacePP[] = _("PP ");\n'
    'const u8 gText_MoveInterfaceStamina[] = _("STAMINA");\n'
    'const u8 gText_MoveInterfaceStaminaCost[] = _(" C");\n',
)

replace_once(
    MESSAGE_H,
    'extern const u8 gText_MoveInterfacePP[];\n',
    'extern const u8 gText_MoveInterfacePP[];\n'
    'extern const u8 gText_MoveInterfaceStamina[];\n'
    'extern const u8 gText_MoveInterfaceStaminaCost[];\n',
)


# ============================================================
# 2. battle_message.c needs Stamina runtime API.
# ============================================================

replace_once(
    MESSAGE_C,
    '#include "battle.h"\n',
    '#include "battle.h"\n'
    '#include "battle_stamina.h"\n',
)


# ============================================================
# 3. Resource palette:
#
# Vanilla/excluded modes:
#   current move PP / max PP
#
# Stamina mode:
#   shared player Stamina / 6
# ============================================================

old_palette = '''    if (!gBattleStruct->zmove.viewing)
        var = GetCurrentPPToMaxPPState(chooseMoveStruct->currentPP[gMoveSelectionCursor[battler]],
                         chooseMoveStruct->maxPP[gMoveSelectionCursor[battler]]);
    else
        var = 3;
'''

new_palette = '''    if (IsBattlerStaminaEnabled(battler))
    {
        var = GetCurrentPPToMaxPPState(
            gBattleStruct->playerStamina,
            BATTLE_STAMINA_MAX);
    }
    else if (!gBattleStruct->zmove.viewing)
    {
        var = GetCurrentPPToMaxPPState(
            chooseMoveStruct->currentPP[gMoveSelectionCursor[battler]],
            chooseMoveStruct->maxPP[gMoveSelectionCursor[battler]]);
    }
    else
    {
        var = 3;
    }
'''

replace_once(
    MESSAGE_C,
    old_palette,
    new_palette,
)


# ============================================================
# 4. Normal move-menu label.
# ============================================================

old_pp_string = '''static void MoveSelectionDisplayPPString(enum BattlerId battler)
{
    StringCopy(gDisplayedStringBattle, gText_MoveInterfacePP);
    BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_PP);
}
'''

new_pp_string = '''static void MoveSelectionDisplayPPString(enum BattlerId battler)
{
    u8 *end;

    if (IsBattlerStaminaEnabled(battler))
    {
        end = StringCopy(
            gDisplayedStringBattle,
            gText_MoveInterfaceStamina);

        PrependFontIdToFit(
            gDisplayedStringBattle,
            end,
            FONT_NARROW,
            WindowWidthPx(B_WIN_PP));
    }
    else
    {
        StringCopy(
            gDisplayedStringBattle,
            gText_MoveInterfacePP);
    }

    BattlePutTextOnWindow(
        gDisplayedStringBattle,
        B_WIN_PP);
}
'''

replace_once(
    CONTROLLER_C,
    old_pp_string,
    new_pp_string,
)


# ============================================================
# 5. Normal move-menu resource number.
# ============================================================

old_pp_number = '''static void MoveSelectionDisplayPPNumber(enum BattlerId battler)
{
    u8 *txtPtr;
    struct ChooseMoveStruct *moveInfo;

    if (gBattleResources->bufferA[battler][2] == TRUE) // check if we didn't want to display PP number
        return;

    SetPPNumbersPaletteInMoveSelection(battler);
    moveInfo = (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);
    txtPtr = ConvertIntToDecimalStringN(gDisplayedStringBattle, moveInfo->currentPP[gMoveSelectionCursor[battler]], STR_CONV_MODE_RIGHT_ALIGN, 2);
    *(txtPtr)++ = CHAR_SLASH;
    ConvertIntToDecimalStringN(txtPtr, moveInfo->maxPP[gMoveSelectionCursor[battler]], STR_CONV_MODE_RIGHT_ALIGN, 2);

    BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_PP_REMAINING);
}
'''

new_pp_number = '''static void MoveSelectionDisplayPPNumber(enum BattlerId battler)
{
    u8 *txtPtr;
    struct ChooseMoveStruct *moveInfo;

    if (gBattleResources->bufferA[battler][2] == TRUE) // check if we didn't want to display PP number
        return;

    SetPPNumbersPaletteInMoveSelection(battler);
    moveInfo = (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);

    if (IsBattlerStaminaEnabled(battler))
    {
        txtPtr = ConvertIntToDecimalStringN(
            gDisplayedStringBattle,
            gBattleStruct->playerStamina,
            STR_CONV_MODE_RIGHT_ALIGN,
            1);
        *(txtPtr)++ = CHAR_SLASH;
        ConvertIntToDecimalStringN(
            txtPtr,
            BATTLE_STAMINA_MAX,
            STR_CONV_MODE_RIGHT_ALIGN,
            1);
    }
    else
    {
        txtPtr = ConvertIntToDecimalStringN(
            gDisplayedStringBattle,
            moveInfo->currentPP[gMoveSelectionCursor[battler]],
            STR_CONV_MODE_RIGHT_ALIGN,
            2);
        *(txtPtr)++ = CHAR_SLASH;
        ConvertIntToDecimalStringN(
            txtPtr,
            moveInfo->maxPP[gMoveSelectionCursor[battler]],
            STR_CONV_MODE_RIGHT_ALIGN,
            2);
    }

    BattlePutTextOnWindow(
        gDisplayedStringBattle,
        B_WIN_PP_REMAINING);
}
'''

replace_once(
    CONTROLLER_C,
    old_pp_number,
    new_pp_number,
)


# ============================================================
# 6. Normal / Dynamax type window gets base-move cost.
#
# moveInfo->moves[] remains the ordinary/base move even when
# the visible move name is transformed into a Max Move.
# ============================================================

old_type_tail = '''    end = StringCopy(txtPtr, gTypesInfo[type].name);

    PrependFontIdToFit(txtPtr, end, FONT_NORMAL, WindowWidthPx(B_WIN_MOVE_TYPE) - 25);
    BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_MOVE_TYPE);
}
'''

new_type_tail = '''    end = StringCopy(txtPtr, gTypesInfo[type].name);

    if (IsBattlerStaminaEnabled(battler))
    {
        end = StringCopy(
            end,
            gText_MoveInterfaceStaminaCost);
        end = ConvertIntToDecimalStringN(
            end,
            GetMoveStaminaCost(move),
            STR_CONV_MODE_LEFT_ALIGN,
            1);
    }

    PrependFontIdToFit(
        txtPtr,
        end,
        FONT_NORMAL,
        WindowWidthPx(B_WIN_MOVE_TYPE) - 25);
    BattlePutTextOnWindow(
        gDisplayedStringBattle,
        B_WIN_MOVE_TYPE);
}
'''

replace_once(
    CONTROLLER_C,
    old_type_tail,
    new_type_tail,
)


# ============================================================
# 7. Z-move module runtime API.
# ============================================================

replace_once(
    ZMOVE_C,
    '#include "battle.h"\n',
    '#include "battle.h"\n'
    '#include "battle_stamina.h"\n',
)


# ============================================================
# 8. Z-view PP number becomes shared Stamina.
# ============================================================

old_z_pp = '''static void ZMoveSelectionDisplayPpNumber(enum BattlerId battler)
{
    u8 *txtPtr;

    if (gBattleResources->bufferA[battler][2] == TRUE) // Check if we didn't want to display pp number
        return;

    SetPPNumbersPaletteInMoveSelection(battler);
    txtPtr = ConvertIntToDecimalStringN(gDisplayedStringBattle, 1, STR_CONV_MODE_RIGHT_ALIGN, 2);
    *(txtPtr)++ = CHAR_SLASH;
    ConvertIntToDecimalStringN(txtPtr, 1, STR_CONV_MODE_RIGHT_ALIGN, 2);
    BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_PP_REMAINING);
}
'''

new_z_pp = '''static void ZMoveSelectionDisplayPpNumber(enum BattlerId battler)
{
    u8 *txtPtr;

    if (gBattleResources->bufferA[battler][2] == TRUE) // Check if we didn't want to display pp number
        return;

    SetPPNumbersPaletteInMoveSelection(battler);

    if (IsBattlerStaminaEnabled(battler))
    {
        txtPtr = ConvertIntToDecimalStringN(
            gDisplayedStringBattle,
            gBattleStruct->playerStamina,
            STR_CONV_MODE_RIGHT_ALIGN,
            1);
        *(txtPtr)++ = CHAR_SLASH;
        ConvertIntToDecimalStringN(
            txtPtr,
            BATTLE_STAMINA_MAX,
            STR_CONV_MODE_RIGHT_ALIGN,
            1);
    }
    else
    {
        txtPtr = ConvertIntToDecimalStringN(
            gDisplayedStringBattle,
            1,
            STR_CONV_MODE_RIGHT_ALIGN,
            2);
        *(txtPtr)++ = CHAR_SLASH;
        ConvertIntToDecimalStringN(
            txtPtr,
            1,
            STR_CONV_MODE_RIGHT_ALIGN,
            2);
    }

    BattlePutTextOnWindow(
        gDisplayedStringBattle,
        B_WIN_PP_REMAINING);
}
'''

replace_once(
    ZMOVE_C,
    old_z_pp,
    new_z_pp,
)


# ============================================================
# 9. Z-view type window:
#
# Visible type = transformed Z Move.
# Stamina cost = underlying ordinary selected move.
# ============================================================

old_z_type = '''static void ZMoveSelectionDisplayMoveType(enum Move zMove, enum BattlerId battler)
{
    u8 *txtPtr, *end;
    enum Type zMoveType = GetBattleMoveType(zMove);

    txtPtr = StringCopy(gDisplayedStringBattle, gText_MoveInterfaceType);
    *(txtPtr)++ = EXT_CTRL_CODE_BEGIN;
    *(txtPtr)++ = EXT_CTRL_CODE_FONT;
    *(txtPtr)++ = FONT_NORMAL;

    end = StringCopy(txtPtr, gTypesInfo[zMoveType].name);
    PrependFontIdToFit(txtPtr, end, FONT_NORMAL, WindowWidthPx(B_WIN_MOVE_TYPE) - 25);
    BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_MOVE_TYPE);
}
'''

new_z_type = '''static void ZMoveSelectionDisplayMoveType(enum Move zMove, enum BattlerId battler)
{
    u8 *txtPtr, *end;
    enum Type zMoveType = GetBattleMoveType(zMove);
    struct ChooseMoveStruct *moveInfo =
        (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);
    enum Move baseMove =
        moveInfo->moves[gMoveSelectionCursor[battler]];

    txtPtr = StringCopy(
        gDisplayedStringBattle,
        gText_MoveInterfaceType);
    *(txtPtr)++ = EXT_CTRL_CODE_BEGIN;
    *(txtPtr)++ = EXT_CTRL_CODE_FONT;
    *(txtPtr)++ = FONT_NORMAL;

    end = StringCopy(
        txtPtr,
        gTypesInfo[zMoveType].name);

    if (IsBattlerStaminaEnabled(battler))
    {
        end = StringCopy(
            end,
            gText_MoveInterfaceStaminaCost);
        end = ConvertIntToDecimalStringN(
            end,
            GetMoveStaminaCost(baseMove),
            STR_CONV_MODE_LEFT_ALIGN,
            1);
    }

    PrependFontIdToFit(
        txtPtr,
        end,
        FONT_NORMAL,
        WindowWidthPx(B_WIN_MOVE_TYPE) - 25);
    BattlePutTextOnWindow(
        gDisplayedStringBattle,
        B_WIN_MOVE_TYPE);
}
'''

replace_once(
    ZMOVE_C,
    old_z_type,
    new_z_type,
)


print("Resource label            : STAMINA")
print("Resource number           : shared current / 6")
print("Resource palette          : based on Stamina")
print("Normal move cost          : displayed")
print("Dynamax cost              : underlying move")
print("Z-move cost               : underlying move")
print("Enemy / excluded PP UI    : preserved")
print("Unaffordable name styling : NOT implemented")
print()
print("OBJECTIVE 07A PATCH: APPLIED")
