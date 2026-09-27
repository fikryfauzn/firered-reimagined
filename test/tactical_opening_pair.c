#include "global.h"
#include "battle.h"
#include "battle_controllers.h"
#include "battle_setup.h"
#include "pokemon.h"
#include "random.h"
#include "test/test.h"
#include "constants/battle.h"

TEST("Random opening applies to ordinary trainer doubles")
{
    gBattleTypeFlags = BATTLE_TYPE_TRAINER | BATTLE_TYPE_DOUBLE;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), TRUE);
}

TEST("Random opening applies against two ordinary opponent trainers")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TWO_OPPONENTS;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), TRUE);
}

TEST("Random opening does not apply to trainer singles")
{
    gBattleTypeFlags = BATTLE_TYPE_TRAINER;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to wild doubles")
{
    gBattleTypeFlags = BATTLE_TYPE_DOUBLE;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to link trainer doubles")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_LINK;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply with a player-side battle partner")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_MULTI
      | BATTLE_TYPE_INGAME_PARTNER;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply in Battle Frontier")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_BATTLE_TOWER;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply in Trainer Hill")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TRAINER_HILL;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to recorded battles")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_RECORDED;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to first battle special cases")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_FIRST_BATTLE;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to secret base battles")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_SECRET_BASE;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

TEST("Random opening does not apply to e-Reader trainer battles")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_EREADER_TRAINER;

    EXPECT_EQ(ShouldUseTacticalOpeningPair(gBattleTypeFlags), FALSE);
}

static void GiveOpeningTestMon(u32 slot, enum Species species)
{
    CreateRandomMon(&gParties[B_TRAINER_PLAYER][slot], species, 10);
}

TEST("Random opening selector returns false with fewer than two usable Pokemon")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;

    ZeroPlayerPartyMons();
    GiveOpeningTestMon(0, SPECIES_BULBASAUR);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        FALSE
    );
}

TEST("Random opening selector chooses the only two usable Pokemon")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;

    ZeroPlayerPartyMons();

    GiveOpeningTestMon(1, SPECIES_BULBASAUR);
    GiveOpeningTestMon(4, SPECIES_CHARMANDER);

    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 0);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        TRUE
    );

    EXPECT_EQ(left, 1);
    EXPECT_EQ(right, 4);
}

TEST("Random opening selector ignores fainted Pokemon and Eggs")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;
    u16 zeroHp = 0;
    bool32 isEgg = TRUE;

    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);

    GiveOpeningTestMon(1, SPECIES_SQUIRTLE);
    SetMonData(
        &gParties[B_TRAINER_PLAYER][1],
        MON_DATA_HP,
        &zeroHp
    );

    GiveOpeningTestMon(2, SPECIES_PIKACHU);
    SetMonData(
        &gParties[B_TRAINER_PLAYER][2],
        MON_DATA_IS_EGG,
        &isEgg
    );

    GiveOpeningTestMon(5, SPECIES_CHARMANDER);

    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 0);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        TRUE
    );

    EXPECT_EQ(left, 0);
    EXPECT_EQ(right, 5);
}

TEST("Random opening selector always returns distinct party slots")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;

    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);
    GiveOpeningTestMon(1, SPECIES_CHARMANDER);
    GiveOpeningTestMon(2, SPECIES_SQUIRTLE);
    GiveOpeningTestMon(3, SPECIES_PIKACHU);

    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 0);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        TRUE
    );

    EXPECT_NE(left, right);
}

TEST("Random opening selector uses its structured RNG choice")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;

    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);
    GiveOpeningTestMon(1, SPECIES_CHARMANDER);
    GiveOpeningTestMon(2, SPECIES_SQUIRTLE);

    // For three usable mons there are six ordered pairs.
    // Choice 1 should differ from choice 0.
    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 1);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        TRUE
    );

    EXPECT_EQ(left, 0);
    EXPECT_EQ(right, 2);
}

TEST("Random opening selector does not reorder the player party")
{
    u8 left = PARTY_SIZE;
    u8 right = PARTY_SIZE;

    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);
    GiveOpeningTestMon(1, SPECIES_CHARMANDER);
    GiveOpeningTestMon(2, SPECIES_SQUIRTLE);
    GiveOpeningTestMon(3, SPECIES_PIKACHU);

    enum Species before[4];

    for (u32 i = 0; i < 4; i++)
        before[i] = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES);

    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 5);

    EXPECT_EQ(
        TrySelectRandomPlayerOpeningPair(&left, &right),
        TRUE
    );

    for (u32 i = 0; i < 4; i++)
    {
        EXPECT_EQ(
            GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES),
            before[i]
        );
    }
}


TEST("Random opening runtime gate requires explicit tactical marker")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE;

    EXPECT_EQ(
        ShouldRandomizePlayerOpeningPair(),
        FALSE
    );
}

TEST("Random opening runtime gate accepts marked campaign double")
{
    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TACTICAL_OPENING_PAIR;

    EXPECT_EQ(
        ShouldRandomizePlayerOpeningPair(),
        TRUE
    );
}

TEST("Opening pair apply helper ignores unmarked trainer doubles")
{
    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);
    GiveOpeningTestMon(1, SPECIES_CHARMANDER);
    GiveOpeningTestMon(2, SPECIES_SQUIRTLE);

    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE;

    gBattlerPartyIndexes[B_BATTLER_0] = 4;
    gBattlerPartyIndexes[B_BATTLER_2] = 5;

    EXPECT_EQ(TryApplyRandomPlayerOpeningPair(), FALSE);

    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_0], 4);
    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_2], 5);
}

TEST("Opening pair apply helper writes selected player battle slots")
{
    ZeroPlayerPartyMons();

    GiveOpeningTestMon(0, SPECIES_BULBASAUR);
    GiveOpeningTestMon(1, SPECIES_CHARMANDER);
    GiveOpeningTestMon(2, SPECIES_SQUIRTLE);

    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TACTICAL_OPENING_PAIR;

    gBattlerPartyIndexes[B_BATTLER_0] = 5;
    gBattlerPartyIndexes[B_BATTLER_2] = 5;

    // For [0, 1, 2], choice 1 = ordered pair [0, 2].
    SET_RNG(RNG_TACTICAL_OPENING_PAIR, 1);

    EXPECT_EQ(TryApplyRandomPlayerOpeningPair(), TRUE);

    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_0], 0);
    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_2], 2);
}

TEST("Opening pair apply helper preserves vanilla slots if fewer than two are usable")
{
    ZeroPlayerPartyMons();

    GiveOpeningTestMon(3, SPECIES_BULBASAUR);

    gBattleTypeFlags =
        BATTLE_TYPE_TRAINER
      | BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TACTICAL_OPENING_PAIR;

    // Simulate values vanilla SetBattlePartyIds already chose.
    gBattlerPartyIndexes[B_BATTLER_0] = 3;
    gBattlerPartyIndexes[B_BATTLER_2] = 0;

    EXPECT_EQ(TryApplyRandomPlayerOpeningPair(), FALSE);

    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_0], 3);
    EXPECT_EQ(gBattlerPartyIndexes[B_BATTLER_2], 0);
}


TEST("Marked wild double uses tactical opening pair")
{
    gBattleTypeFlags =
        BATTLE_TYPE_DOUBLE
      | BATTLE_TYPE_TACTICAL_OPENING_PAIR;

    EXPECT_EQ(
        ShouldRandomizePlayerOpeningPair(),
        TRUE
    );
}
