#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

STAMINA_H = ROOT / "include/battle_stamina.h"
STAMINA_C = ROOT / "src/battle_stamina.c"
RESOLUTION_C = ROOT / "src/battle_move_resolution.c"

BATTLE_SCRIPTS_H = ROOT / "include/battle_scripts.h"
BATTLE_SCRIPTS_S = ROOT / "data/battle_scripts_1.s"
STRING_IDS_H = ROOT / "include/constants/battle_string_ids.h"
BATTLE_MESSAGE_C = ROOT / "src/battle_message.c"


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
    "=== OBJECTIVE 05 — "
    "STAMINA CONSUMPTION ==="
)

for path in (
    STAMINA_H,
    STAMINA_C,
    RESOLUTION_C,
    BATTLE_SCRIPTS_H,
    BATTLE_SCRIPTS_S,
    STRING_IDS_H,
    BATTLE_MESSAGE_C,
):
    if not path.is_file():
        die(
            "missing required file: "
            + str(path)
        )


# ============================================================
# 1. Public spend helper.
# ============================================================

replace_once(
    STAMINA_H,
    "bool32 CanBattlerAffordMoveStamina"
    "(enum BattlerId battler, enum Move move);\n",
    "bool32 CanBattlerAffordMoveStamina"
    "(enum BattlerId battler, enum Move move);\n"
    "bool32 TrySpendBattlerStamina"
    "(enum BattlerId battler, enum Move move);\n",
)

stamina_source = STAMINA_C.read_text(
    encoding="utf-8",
)

if "TrySpendBattlerStamina(" not in stamina_source:
    append = '''
bool32 TrySpendBattlerStamina(enum BattlerId battler, enum Move move)
{
    u8 cost;

    if (!IsBattlerStaminaEnabled(battler))
        return FALSE;

    if (move >= MOVES_COUNT)
        return FALSE;

    cost = GetMoveStaminaCost(move);

    if (cost > gBattleStruct->playerStamina)
        return FALSE;

    gBattleStruct->playerStamina -= cost;
    return TRUE;
}
'''

    STAMINA_C.write_text(
        stamina_source.rstrip()
        + "\n"
        + append,
        encoding="utf-8",
    )


# ============================================================
# 2. Runtime insufficient-Stamina message.
#
# This is separate from the selection message because at the
# PPDEDUCTION boundary the attack string has already occurred.
# This path is principally needed for doubles overcommit:
#
#   both moves were affordable when selected,
#   battler A spends first,
#   battler B is no longer affordable when it acts.
# ============================================================

string_text = STRING_IDS_H.read_text(
    encoding="utf-8",
)

if "STRINGID_BUTNOTENOUGHSTAMINA" not in string_text:
    lines = string_text.splitlines(
        keepends=True,
    )

    matches = [
        i
        for i, line in enumerate(lines)
        if line.strip() == "STRINGID_COUNT"
    ]

    if len(matches) != 1:
        die(
            "battle string enum does not have "
            "exactly one STRINGID_COUNT"
        )

    lines.insert(
        matches[0],
        "    STRINGID_BUTNOTENOUGHSTAMINA,\n",
    )

    STRING_IDS_H.write_text(
        "".join(lines),
        encoding="utf-8",
    )


message_text = BATTLE_MESSAGE_C.read_text(
    encoding="utf-8",
)

if "STRINGID_BUTNOTENOUGHSTAMINA" not in message_text:
    lines = message_text.splitlines(
        keepends=True,
    )

    matches = [
        i
        for i, line in enumerate(lines)
        if "[STRINGID_NOTENOUGHSTAMINA]" in line
    ]

    if len(matches) != 1:
        die(
            "expected exactly one existing "
            "STRINGID_NOTENOUGHSTAMINA table entry"
        )

    lines.insert(
        matches[0] + 1,
        (
            "    [STRINGID_BUTNOTENOUGHSTAMINA]"
            "                  = "
            "COMPOUND_STRING("
            "\"But there wasn't enough Stamina "
            "for the move!\"),\n"
        ),
    )

    BATTLE_MESSAGE_C.write_text(
        "".join(lines),
        encoding="utf-8",
    )


replace_once(
    BATTLE_SCRIPTS_H,
    "extern const u8 "
    "BattleScript_SelectingMoveWithNotEnoughStamina[];\n",
    "extern const u8 "
    "BattleScript_SelectingMoveWithNotEnoughStamina[];\n"
    "extern const u8 "
    "BattleScript_NotEnoughStaminaForMove[];\n",
)


script_text = BATTLE_SCRIPTS_S.read_text(
    encoding="utf-8",
)

if (
    "BattleScript_NotEnoughStaminaForMove::"
    not in script_text
):
    anchor = (
        "BattleScript_SelectingMoveWithNotEnoughStamina::\n"
        "\tprintselectionstring STRINGID_NOTENOUGHSTAMINA\n"
        "\tendselectionscript\n"
    )

    insertion = (
        anchor
        + "\n"
        + "BattleScript_NotEnoughStaminaForMove::\n"
        + "\tprintstring STRINGID_BUTNOTENOUGHSTAMINA\n"
        + "\twaitmessage B_WAIT_TIME_LONG\n"
        + "\tgoto BattleScript_MoveEnd\n"
    )

    if script_text.count(anchor) != 1:
        die(
            "Stamina selection-script anchor "
            "not found exactly once"
        )

    BATTLE_SCRIPTS_S.write_text(
        script_text.replace(
            anchor,
            insertion,
            1,
        ),
        encoding="utf-8",
    )


# ============================================================
# 3. battle_move_resolution.c include.
# ============================================================

replace_once(
    RESOLUTION_C,
    '#include "battle.h"\n',
    '#include "battle.h"\n'
    '#include "battle_stamina.h"\n',
)


# ============================================================
# 4. Execution-time zero-PP bypass.
#
# Enemy and excluded modes retain vanilla behavior.
# ============================================================

old_power_points = '''static enum CancelerResult CancelerPowerPoints(struct BattleCalcValues *cv)
{
    if (gBattleMons[cv->battlerAtk].pp[gCurrMovePos] == 0
     && cv->move != MOVE_STRUGGLE
     && !gSpecialStatuses[cv->battlerAtk].dancerUsedMove
     && !gBattleMons[cv->battlerAtk].volatiles.multipleTurns)
'''

new_power_points = '''static enum CancelerResult CancelerPowerPoints(struct BattleCalcValues *cv)
{
    if (!IsBattlerStaminaEnabled(cv->battlerAtk)
     && gBattleMons[cv->battlerAtk].pp[gCurrMovePos] == 0
     && cv->move != MOVE_STRUGGLE
     && !gSpecialStatuses[cv->battlerAtk].dancerUsedMove
     && !gBattleMons[cv->battlerAtk].volatiles.multipleTurns)
'''

replace_once(
    RESOLUTION_C,
    old_power_points,
    new_power_points,
)


# ============================================================
# 5. Replace CancelerPPDeduction.
#
# Important semantics:
#
# - automatic continuations skip this resource payment
# - Dancer / bounced / snatched results are free
# - Bide continuation is free
# - Struggle is free
# - called moves pay caller cost:
#       submoveAnnouncement == SUBMOVE_SUCCESS
#       -> chosen moveslot's ordinary move
# - Z / Max pay gBattleStruct->baseMove
# - player Stamina mode does NOT decrement stored PP
# - opponents / excluded modes use original vanilla PP logic
# - failed atomic spend means doubles overcommit; abort action
# ============================================================

text = RESOLUTION_C.read_text(
    encoding="utf-8",
)

start_marker = (
    "static enum CancelerResult "
    "CancelerPPDeduction(struct BattleCalcValues *cv)\n"
)

end_marker = (
    "\n// We don't have clear data on where this belongs"
)

start = text.find(start_marker)

if start == -1:
    die(
        "CancelerPPDeduction start not found"
    )

end = text.find(
    end_marker,
    start,
)

if end == -1:
    die(
        "CancelerPPDeduction end anchor not found"
    )

old_body = text[start:end]

if "TrySpendBattlerStamina" not in old_body:
    required_fragments = (
        "s32 ppToDeduct = 1;",
        "MOVE_IS_PERMANENT",
        "gBattleStruct->submoveAnnouncement",
        "gLastMoves[cv->battlerAtk] = gChosenMove;",
    )

    for fragment in required_fragments:
        if fragment not in old_body:
            die(
                "unexpected CancelerPPDeduction shape; "
                "missing "
                + repr(fragment)
            )

    new_body = '''static enum CancelerResult CancelerPPDeduction(struct BattleCalcValues *cv)
{
    if (gBattleMons[cv->battlerAtk].volatiles.multipleTurns
     || gSpecialStatuses[cv->battlerAtk].dancerUsedMove
     || gBattleStruct->bouncedMoveIsUsed
     || gBattleStruct->snatchedMoveIsUsed
     || gBattleMons[cv->battlerAtk].volatiles.bideTurns
     || cv->move == MOVE_STRUGGLE)
        return CANCELER_RESULT_SUCCESS;

    u32 movePosition = gCurrMovePos;

    if (gBattleStruct->submoveAnnouncement == SUBMOVE_SUCCESS)
        movePosition = gChosenMovePos;

    // For item Metronome, Echoed Voice.
    if (cv->move != gLastResultingMoves[cv->battlerAtk] || gBattleStruct->unableToUseMove)
        gBattleMons[cv->battlerAtk].volatiles.metronomeItemCounter = 0;

    if (IsBattlerStaminaEnabled(cv->battlerAtk))
    {
        enum Move staminaMove = gBattleStruct->baseMove;

        // Called moves consume the caller's Stamina cost, not the
        // generated/called result. At this point baseMove has already
        // been replaced by the called move, so recover the caller from
        // its originally chosen moveslot.
        if (gBattleStruct->submoveAnnouncement == SUBMOVE_SUCCESS)
            staminaMove = gBattleMons[cv->battlerAtk].moves[gChosenMovePos];

        // Selection-time affordability can become stale in doubles
        // because both battlers share one pool. The spend itself is
        // therefore the authoritative execution-time affordability
        // check and must never underflow.
        if (!TrySpendBattlerStamina(cv->battlerAtk, staminaMove))
        {
            gBattleStruct->moveResultFlags[cv->battlerDef] |= MOVE_RESULT_MISSED;
            gBattlescriptCurrInstr = BattleScript_NotEnoughStaminaForMove;
            return CANCELER_RESULT_FAILURE;
        }
    }
    else
    {
        s32 ppToDeduct = 1;
        enum MoveTarget moveTarget = GetBattlerMoveTargetType(cv->battlerAtk, cv->move);

        if (IsSpreadMove(moveTarget)
         || moveTarget == TARGET_ALL_BATTLERS
         || moveTarget == TARGET_FIELD
         || MoveForcesPressure(cv->move))
        {
            for (u32 i = 0; i < gBattlersCount; i++)
            {
                if (!IsBattlerAlly(i, cv->battlerAtk))
                    ppToDeduct += (GetBattlerAbility(i) == ABILITY_PRESSURE);
            }
        }
        else if (moveTarget != TARGET_OPPONENTS_FIELD)
        {
            if (cv->battlerAtk != cv->battlerDef
             && GetBattlerAbility(cv->battlerDef) == ABILITY_PRESSURE)
                ppToDeduct++;
        }

        if (gBattleMons[cv->battlerAtk].pp[movePosition] > ppToDeduct)
            gBattleMons[cv->battlerAtk].pp[movePosition] -= ppToDeduct;
        else
            gBattleMons[cv->battlerAtk].pp[movePosition] = 0;

        if (MOVE_IS_PERMANENT(cv->battlerAtk, movePosition))
        {
            BtlController_EmitSetMonData(
                cv->battlerAtk,
                B_COMM_TO_CONTROLLER,
                REQUEST_PPMOVE1_BATTLE + movePosition,
                0,
                sizeof(gBattleMons[cv->battlerAtk].pp[movePosition]),
                &gBattleMons[cv->battlerAtk].pp[movePosition]);
            MarkBattlerForControllerExec(cv->battlerAtk);
        }
    }

    gLastMoves[cv->battlerAtk] = gChosenMove;

    if (gBattleStruct->submoveAnnouncement != SUBMOVE_NO_EFFECT)
    {
        if (gBattleStruct->submoveAnnouncement == SUBMOVE_FAILURE)
        {
            gBattleStruct->submoveAnnouncement = SUBMOVE_NO_EFFECT;
            gBattlescriptCurrInstr = BattleScript_ButItFailed;
            return CANCELER_RESULT_FAILURE;
        }
        else if (CancelerVolatileBlocked(cv) == CANCELER_RESULT_FAILURE)
        {
            // Check Gravity / Heal Block / Throat Chop for Submove.
            gBattleStruct->submoveAnnouncement = SUBMOVE_NO_EFFECT;
            return CANCELER_RESULT_FAILURE;
        }
        else
        {
            gBattleStruct->submoveAnnouncement = SUBMOVE_NO_EFFECT;
            gBattleScripting.animTurn = 0;
            gBattleScripting.animTargetsHit = 0;

            // Possibly better to just move type setting and redirection
            // to attackcanceler as a new case at this point.
            SetTypeBeforeUsingMove(
                cv->move,
                cv->battlerAtk,
                cv->abilities[cv->battlerAtk],
                cv->holdEffects[cv->battlerAtk]);
            gBattlescriptCurrInstr = GetMoveBattleScript(cv->move);
            return CANCELER_RESULT_RUN_SCRIPT_AND_INCREMENT;
        }
    }

    return CANCELER_RESULT_RUN_SCRIPT_AND_INCREMENT;
}
'''

    text = (
        text[:start]
        + new_body
        + text[end:]
    )

    RESOLUTION_C.write_text(
        text,
        encoding="utf-8",
    )


print("Spend helper              : added")
print("Execution PP blocker      : bypassed for Stamina player")
print("Player PP deduction       : bypassed")
print("Enemy PP deduction        : preserved")
print("Ordinary move payment     : enabled")
print("Z / Max payment identity  : base ordinary move")
print("Called-result payment     : caller pays")
print("Continuation payment      : free")
print("Doubles overcommit        : hard execution failure")
print("Stamina underflow         : impossible")
print("Regeneration              : NOT implemented")
print()
print("OBJECTIVE 05 PATCH: APPLIED")
