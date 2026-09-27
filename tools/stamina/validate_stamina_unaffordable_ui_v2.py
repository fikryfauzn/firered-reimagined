#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def read(path: str) -> str:
    p = ROOT / path

    if not p.is_file():
        fail("missing file: " + path)

    return p.read_text(encoding="utf-8")


def extract(
    text: str,
    start: str,
    end: str,
    label: str,
) -> str:
    start_pos = text.find(start)

    if start_pos == -1:
        fail(label + ": start marker not found")

    end_pos = text.find(end, start_pos)

    if end_pos == -1:
        fail(label + ": end marker not found")

    return text[start_pos:end_pos]


print(
    "=== OBJECTIVE 07B VALIDATION ==="
)

controller = read(
    "src/battle_controller_player.c"
)

names_body = extract(
    controller,
    (
        "static void MoveSelectionDisplayMoveNames"
        "(enum BattlerId battler)\n"
        "{"
    ),
    (
        "\nstatic void MoveSelectionDisplayPPString"
    ),
    "MoveSelectionDisplayMoveNames",
)


def require_names(
    needle: str,
    count: int = 1,
) -> None:
    actual = names_body.count(needle)

    if actual != count:
        fail(
            "MoveSelectionDisplayMoveNames: expected "
            + repr(needle)
            + " "
            + str(count)
            + " time(s), found "
            + str(actual)
        )


require_names(
    "enum Move move = moveInfo->moves[i];"
)

require_names(
    "IsBattlerStaminaEnabled(battler)"
)

require_names(
    "!CanBattlerAffordMoveStamina(battler, move)"
)

require_names(
    "EXT_CTRL_CODE_TEXT_COLORS"
)

require_names(
    "TEXT_COLOR_LIGHT_GRAY"
)

require_names(
    "TEXT_COLOR_DARK_GRAY"
)

require_names(
    "TEXT_DYNAMIC_COLOR_5"
)

require_names(
    "GetMoveName(GetMaxMove(battler, move))"
)

require_names(
    "GetMoveName(move)"
)

require_names(
    "move != MOVE_NONE",
    2,
)


# ============================================================
# Z detail view
# ============================================================

zmove = read(
    "src/battle_z_move.c"
)

marker = (
    "// Stamina: the visible Z-move name is transformed"
)

if zmove.count(marker) != 1:
    fail(
        "Z-move unaffordable styling block "
        "not present exactly once"
    )

marker_pos = zmove.find(marker)

z_block_start = zmove.rfind(
    "\n",
    0,
    marker_pos,
)

z_block_end = zmove.find(
    (
        "BattlePutTextOnWindow"
        "(gDisplayedStringBattle, B_WIN_MOVE_NAME_1);"
    ),
    marker_pos,
)

if z_block_end == -1:
    fail(
        "Z-move final name display not found "
        "after Stamina styling block"
    )

z_block = zmove[
    z_block_start:z_block_end
]


def require_z(
    needle: str,
    count: int = 1,
) -> None:
    actual = z_block.count(needle)

    if actual != count:
        fail(
            "Z-move styling block: expected "
            + repr(needle)
            + " "
            + str(count)
            + " time(s), found "
            + str(actual)
        )


require_z(
    "IsBattlerStaminaEnabled(battler)"
)

require_z(
    "moveInfo->moves[gMoveSelectionCursor[battler]]"
)

require_z(
    "!CanBattlerAffordMoveStamina(battler, baseMove)"
)

require_z(
    "StringCopy(\n                    gStringVar4,\n                    gDisplayedStringBattle);"
)

require_z(
    "EXT_CTRL_CODE_TEXT_COLORS"
)

require_z(
    "TEXT_COLOR_LIGHT_GRAY"
)

require_z(
    "TEXT_COLOR_DARK_GRAY"
)

require_z(
    "TEXT_DYNAMIC_COLOR_5"
)

require_z(
    "StringCopy(\n                    text,\n                    gStringVar4);"
)


# ============================================================
# Make sure 07B didn't introduce mechanics.
# ============================================================

for path in (
    "src/battle_controller_player.c",
    "src/battle_z_move.c",
):
    contents = read(path)

    if "TrySpendBattlerStamina(" in contents:
        fail(
            "UI file unexpectedly spends Stamina: "
            + path
        )

    if "RegeneratePlayerStamina(" in contents:
        fail(
            "UI file unexpectedly regenerates Stamina: "
            + path
        )


print("Normal affordability check : PASS")
print("Normal disabled colors     : PASS")
print("MOVE_NONE preservation     : PASS")
print("Dynamax visible name       : PRESERVED")
print("Dynamax base affordability : PASS")
print("Z visible name             : PRESERVED")
print("Z base affordability       : PASS")
print("Mechanics isolation        : PASS")
print()
print(
    "OBJECTIVE 07B VALIDATION: PASS"
)
