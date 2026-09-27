#include "global.h"
#include "battle_setup.h"
#include "difficulty.h"
#include "pokemon.h"
#include "test/test.h"
#include "constants/difficulty.h"
#include "constants/species.h"

enum
{
    TACTICAL_TEST_SINGLE_ONE_MON = 6,
    TACTICAL_TEST_SINGLE_THREE_MONS = 7,
    TACTICAL_TEST_DOUBLE_THREE_MONS = 8,
};

static void GivePlayerUsableMons(u32 count)
{
    ZeroPlayerPartyMons();

    if (count >= 1)
        CreateRandomMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_WOBBUFFET, 5);

    if (count >= 2)
        CreateRandomMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_WYNAUT, 5);
}

TEST("Tactical doubles preserves authored double trainer with one usable player mon")
{
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    GivePlayerUsableMons(1);

    EXPECT_EQ(
        ShouldUseTacticalDoubles(TACTICAL_TEST_DOUBLE_THREE_MONS),
        TRUE
    );
}

TEST("Tactical doubles keeps one-Pokemon enemy trainer single")
{
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    GivePlayerUsableMons(2);

    EXPECT_EQ(
        ShouldUseTacticalDoubles(TACTICAL_TEST_SINGLE_ONE_MON),
        FALSE
    );
}

TEST("Tactical doubles converts multi-Pokemon singles trainer with two usable player mons")
{
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    GivePlayerUsableMons(2);

    EXPECT_EQ(
        ShouldUseTacticalDoubles(TACTICAL_TEST_SINGLE_THREE_MONS),
        TRUE
    );
}

TEST("Tactical doubles does not convert singles trainer with only one usable player mon")
{
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    GivePlayerUsableMons(1);

    EXPECT_EQ(
        ShouldUseTacticalDoubles(TACTICAL_TEST_SINGLE_THREE_MONS),
        FALSE
    );
}

TEST("Tactical doubles does not convert singles trainer when second player mon is fainted")
{
    u16 hp = 0;

    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    GivePlayerUsableMons(2);

    SetMonData(
        &gParties[B_TRAINER_PLAYER][1],
        MON_DATA_HP,
        &hp
    );

    EXPECT_EQ(
        ShouldUseTacticalDoubles(TACTICAL_TEST_SINGLE_THREE_MONS),
        FALSE
    );
}
