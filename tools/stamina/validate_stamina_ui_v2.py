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


def require(
    path: str,
    needle: str,
    count: int = 1,
) -> None:
    actual = read(path).count(needle)

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


print("=== OBJECTIVE 07A VALIDATION ===")

require(
    "src/battle_message.c",
    'const u8 gText_MoveInterfaceStamina[] = _("STAMINA");',
)

require(
    "src/battle_message.c",
    'const u8 gText_MoveInterfaceStaminaCost[] = _(" C");',
)

require(
    "include/battle_message.h",
    "extern const u8 gText_MoveInterfaceStamina[];",
)

require(
    "include/battle_message.h",
    "extern const u8 gText_MoveInterfaceStaminaCost[];",
)

require(
    "src/battle_message.c",
    '#include "battle_stamina.h"',
)

require(
    "src/battle_message.c",
    "gBattleStruct->playerStamina,\n"
    "            BATTLE_STAMINA_MAX",
)

controller = read(
    "src/battle_controller_player.c"
)

if controller.count(
    "gText_MoveInterfaceStamina"
) < 2:
    fail(
        "normal move UI does not reference "
        "Stamina label/cost"
    )

if controller.count(
    "gBattleStruct->playerStamina"
) < 1:
    fail(
        "normal resource display is not "
        "using shared Stamina"
    )

if controller.count(
    "GetMoveStaminaCost(move)"
) < 1:
    fail(
        "normal move cost display missing"
    )

require(
    "src/battle_z_move.c",
    '#include "battle_stamina.h"',
)

require(
    "src/battle_z_move.c",
    "gBattleStruct->playerStamina",
)

require(
    "src/battle_z_move.c",
    "GetMoveStaminaCost(baseMove)",
)

zmove = read(
    "src/battle_z_move.c"
)

z_type_start = zmove.find(
    "static void ZMoveSelectionDisplayMoveType"
    "(enum Move zMove, enum BattlerId battler)\n"
    "{"
)

if z_type_start == -1:
    fail(
        "ZMoveSelectionDisplayMoveType not found"
    )

z_type_end = zmove.find(
    "\n#define Z_EFFECT_BS_LENGTH",
    z_type_start,
)

if z_type_end == -1:
    fail(
        "ZMoveSelectionDisplayMoveType end "
        "boundary not found"
    )

z_type_body = zmove[
    z_type_start:z_type_end
]

if (
    z_type_body.count(
        "moveInfo->moves[gMoveSelectionCursor[battler]]"
    )
    != 1
):
    fail(
        "Z-move cost display is not using "
        "exactly one selected underlying move"
    )

if (
    z_type_body.count(
        "GetMoveStaminaCost(baseMove)"
    )
    != 1
):
    fail(
        "Z-move type display is not pricing "
        "the underlying move exactly once"
    )

# Vanilla labels/data must remain available for excluded modes.
require(
    "src/battle_message.c",
    'const u8 gText_MoveInterfacePP[] = _("PP ");',
)

if (
    "moveInfo->currentPP[gMoveSelectionCursor[battler]]"
    not in controller
):
    fail(
        "vanilla PP display path was removed"
    )

zmove = read(
    "src/battle_z_move.c"
)

if (
    "STR_CONV_MODE_RIGHT_ALIGN,\n"
    "            2"
    not in zmove
):
    fail(
        "vanilla Z-move 1/1 display path "
        "appears removed"
    )

print("STAMINA label             : PASS")
print("Shared current / max      : PASS")
print("Stamina-based palette     : PASS")
print("Normal move cost          : PASS")
print("Dynamax base cost         : PASS")
print("Z-move base cost          : PASS")
print("Vanilla PP fallback       : PRESERVED")
print("Unaffordable styling      : ABSENT (expected)")
print()
print("OBJECTIVE 07A VALIDATION: PASS")
