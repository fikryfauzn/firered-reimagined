#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".").resolve()

CONSTANTS_H = ROOT / "include/constants/battle.h"
BATTLE_H = ROOT / "include/battle.h"
UTIL2_C = ROOT / "src/battle_util2.c"


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


def main() -> None:
    print("=== OBJECTIVE 03 — STAMINA SCAFFOLD ===")

    for path in (
        CONSTANTS_H,
        BATTLE_H,
        UTIL2_C,
    ):
        if not path.is_file():
            die("missing required file: " + str(path))

    # ---------------------------------------------------------
    # 1. Economy constants
    # ---------------------------------------------------------

    replace_once(
        CONSTANTS_H,
        "#define GUARD_CONSTANTS_BATTLE_H\n",
        "#define GUARD_CONSTANTS_BATTLE_H\n"
        "\n"
        "#define BATTLE_STAMINA_MAX    6\n"
        "#define BATTLE_STAMINA_REGEN  2\n",
    )

    # ---------------------------------------------------------
    # 2. Reuse existing unused BattleStruct nibble.
    #
    # Before:
    #   numSpreadTargets : 3
    #   moldBreakerActive: 1
    #   unused4          : 4
    #
    # After:
    #   numSpreadTargets : 3
    #   moldBreakerActive: 1
    #   playerStamina    : 4
    #
    # Same storage width: 8 bits.
    # ---------------------------------------------------------

    replace_once(
        BATTLE_H,
        "    u8 numSpreadTargets:3;\n"
        "    u8 moldBreakerActive:1;\n"
        "    u8 unused4:4;\n",
        "    u8 numSpreadTargets:3;\n"
        "    u8 moldBreakerActive:1;\n"
        "    u8 playerStamina:4;\n",
    )

    # ---------------------------------------------------------
    # 3. Initialize after AllocZeroed.
    # ---------------------------------------------------------

    replace_once(
        UTIL2_C,
        "    gBattleStruct = AllocZeroed(sizeof(*gBattleStruct));\n"
        "    gAiBattleData = AllocZeroed(sizeof(*gAiBattleData));\n",
        "    gBattleStruct = AllocZeroed(sizeof(*gBattleStruct));\n"
        "    gBattleStruct->playerStamina = BATTLE_STAMINA_MAX;\n"
        "    gAiBattleData = AllocZeroed(sizeof(*gAiBattleData));\n",
    )

    print("Added BATTLE_STAMINA_MAX   : 6")
    print("Added BATTLE_STAMINA_REGEN : 2")
    print("BattleStruct storage       : unused4:4 -> playerStamina:4")
    print("Additional state RAM       : 0 bytes")
    print("Battle initialization      : playerStamina = 6")
    print()
    print("OBJECTIVE 03 PATCH: APPLIED")


if __name__ == "__main__":
    main()
