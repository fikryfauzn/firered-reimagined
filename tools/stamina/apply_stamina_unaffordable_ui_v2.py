#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

CONTROLLER_C = ROOT / "src/battle_controller_player.c"
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


print(
    "=== OBJECTIVE 07B — "
    "UNAFFORDABLE MOVE STYLING ==="
)

for path in (
    CONTROLLER_C,
    ZMOVE_C,
):
    if not path.is_file():
        die("missing required file: " + str(path))


# ============================================================
# 1. Normal / Dynamax move-list names.
#
# Affordability always uses the underlying ordinary move.
# The visible name may still be transformed to a Max Move.
# ============================================================

old_names = '''static void MoveSelectionDisplayMoveNames(enum BattlerId battler)
{
    s32 i;
    struct ChooseMoveStruct *moveInfo = (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);
    gNumberOfMovesToChoose = 0;

    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        MoveSelectionDestroyCursorAt(i);
        if (IsGimmickSelected(battler, GIMMICK_DYNAMAX) || GetActiveGimmick(battler) == GIMMICK_DYNAMAX)
            StringCopy(gDisplayedStringBattle, GetMoveName(GetMaxMove(battler, moveInfo->moves[i])));
        else
            StringCopy(gDisplayedStringBattle, GetMoveName(moveInfo->moves[i]));
        // Prints on windows B_WIN_MOVE_NAME_1, B_WIN_MOVE_NAME_2, B_WIN_MOVE_NAME_3, B_WIN_MOVE_NAME_4
        BattlePutTextOnWindow(gDisplayedStringBattle, i + B_WIN_MOVE_NAME_1);
        if (moveInfo->moves[i] != MOVE_NONE)
            gNumberOfMovesToChoose++;
    }
}
'''

new_names = '''static void MoveSelectionDisplayMoveNames(enum BattlerId battler)
{
    s32 i;
    struct ChooseMoveStruct *moveInfo = (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);
    gNumberOfMovesToChoose = 0;

    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        u8 *text = gDisplayedStringBattle;
        enum Move move = moveInfo->moves[i];

        MoveSelectionDestroyCursorAt(i);

        // Stamina: grey moves whose underlying ordinary move cannot
        // currently be afforded. This is display-only; hard rejection
        // remains in the battle-selection/execution logic.
        if (move != MOVE_NONE
         && IsBattlerStaminaEnabled(battler)
         && !CanBattlerAffordMoveStamina(battler, move))
        {
            *(text++) = EXT_CTRL_CODE_BEGIN;
            *(text++) = EXT_CTRL_CODE_TEXT_COLORS;
            *(text++) = TEXT_COLOR_LIGHT_GRAY;
            *(text++) = TEXT_COLOR_DARK_GRAY;
            *(text++) = TEXT_DYNAMIC_COLOR_5;
        }

        if (IsGimmickSelected(battler, GIMMICK_DYNAMAX)
         || GetActiveGimmick(battler) == GIMMICK_DYNAMAX)
        {
            StringCopy(
                text,
                GetMoveName(GetMaxMove(battler, move)));
        }
        else
        {
            StringCopy(
                text,
                GetMoveName(move));
        }

        // Prints on windows B_WIN_MOVE_NAME_1,
        // B_WIN_MOVE_NAME_2, B_WIN_MOVE_NAME_3,
        // B_WIN_MOVE_NAME_4.
        BattlePutTextOnWindow(
            gDisplayedStringBattle,
            i + B_WIN_MOVE_NAME_1);

        if (move != MOVE_NONE)
            gNumberOfMovesToChoose++;
    }
}
'''

replace_once(
    CONTROLLER_C,
    old_names,
    new_names,
)


# ============================================================
# 2. Z-move detail view.
#
# At this point gDisplayedStringBattle already contains the
# transformed visible Z-move name. Prefix the same disabled
# text colors when its underlying selected ordinary move is
# unaffordable.
# ============================================================

old_z_display = '''        BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_MOVE_NAME_1);

        ZMoveSelectionDisplayPpNumber(battler);
'''

new_z_display = '''        // Stamina: the visible Z-move name is transformed, but
        // affordability is based on the selected ordinary move.
        if (IsBattlerStaminaEnabled(battler))
        {
            struct ChooseMoveStruct *moveInfo =
                (struct ChooseMoveStruct *)(&gBattleResources->bufferA[battler][4]);
            enum Move baseMove =
                moveInfo->moves[gMoveSelectionCursor[battler]];

            if (baseMove != MOVE_NONE
             && !CanBattlerAffordMoveStamina(battler, baseMove))
            {
                u8 *text;

                // Preserve the already-built transformed Z-move name,
                // then prepend per-string disabled colors.
                StringCopy(
                    gStringVar4,
                    gDisplayedStringBattle);

                text = gDisplayedStringBattle;
                *(text++) = EXT_CTRL_CODE_BEGIN;
                *(text++) = EXT_CTRL_CODE_TEXT_COLORS;
                *(text++) = TEXT_COLOR_LIGHT_GRAY;
                *(text++) = TEXT_COLOR_DARK_GRAY;
                *(text++) = TEXT_DYNAMIC_COLOR_5;

                StringCopy(
                    text,
                    gStringVar4);
            }
        }

        BattlePutTextOnWindow(gDisplayedStringBattle, B_WIN_MOVE_NAME_1);

        ZMoveSelectionDisplayPpNumber(battler);
'''

replace_once(
    ZMOVE_C,
    old_z_display,
    new_z_display,
)


print("Normal affordable names   : unchanged")
print("Normal unaffordable names : grey")
print("Dynamax visible names     : preserved")
print("Dynamax affordability     : underlying move")
print("Z visible names           : preserved")
print("Z affordability           : underlying move")
print("MOVE_NONE                 : unchanged")
print("Mechanics                 : untouched")
print()
print("OBJECTIVE 07B PATCH: APPLIED")
