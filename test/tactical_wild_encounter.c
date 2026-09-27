#include "global.h"
#include "random.h"
#include "wild_encounter.h"
#include "pokemon.h"
#include "test/test.h"

TEST("Tactical wild encounter normal branch has two Pokemon")
{
    SET_RNG(RNG_TACTICAL_WILD_PACK, 0);

    EXPECT_EQ(ChooseTacticalWildPartySize(), 2);
}

TEST("Tactical wild encounter pack branch has five Pokemon")
{
    SET_RNG(RNG_TACTICAL_WILD_PACK, 1);

    EXPECT_EQ(ChooseTacticalWildPartySize(), 5);
}

TEST("Tactical wild slot generation preserves existing enemy party members")
{
    ZeroEnemyPartyMons();

    CreateWildMonInPartySlot(SPECIES_BULBASAUR, 10, 0);
    CreateWildMonInPartySlot(SPECIES_CHARMANDER, 11, 1);

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_SPECIES),
        SPECIES_BULBASAUR
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][1], MON_DATA_SPECIES),
        SPECIES_CHARMANDER
    );
}

TEST("Tactical wild slot generation can populate later enemy party slots")
{
    ZeroEnemyPartyMons();

    CreateWildMonInPartySlot(SPECIES_SQUIRTLE, 12, 4);

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][4], MON_DATA_SPECIES),
        SPECIES_SQUIRTLE
    );
}

TEST("Legacy CreateWildMon still resets the enemy party")
{
    ZeroEnemyPartyMons();

    CreateWildMonInPartySlot(SPECIES_BULBASAUR, 10, 1);

    CreateWildMon(SPECIES_SQUIRTLE, 12);

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_SPECIES),
        SPECIES_SQUIRTLE
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][1], MON_DATA_SPECIES),
        SPECIES_NONE
    );
}

static const struct WildPokemon sTacticalTestLandMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
    { 10, 10, SPECIES_BULBASAUR },
};

static const struct WildPokemonInfo sTacticalTestLandInfo =
{
    .encounterRate = 1,
    .wildPokemon = sTacticalTestLandMons,
};

TEST("Tactical wild party generator creates exactly two Pokemon")
{
    EXPECT(GenerateTacticalWildParty(
        &sTacticalTestLandInfo,
        WILD_AREA_LAND,
        0,
        2
    ));

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_SPECIES),
        SPECIES_BULBASAUR
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][1], MON_DATA_SPECIES),
        SPECIES_BULBASAUR
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][2], MON_DATA_SPECIES),
        SPECIES_NONE
    );
}

TEST("Tactical wild party generator creates exactly five Pokemon")
{
    EXPECT(GenerateTacticalWildParty(
        &sTacticalTestLandInfo,
        WILD_AREA_LAND,
        0,
        5
    ));

    for (u32 i = 0; i < 5; i++)
    {
        EXPECT_EQ(
            GetMonData(&gParties[B_TRAINER_OPPONENT_A][i], MON_DATA_SPECIES),
            SPECIES_BULBASAUR
        );
    }

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][5], MON_DATA_SPECIES),
        SPECIES_NONE
    );
}


static const struct WildPokemon sTacticalDiverseLandMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    { 10, 10, SPECIES_BULBASAUR  },
    { 10, 10, SPECIES_BULBASAUR  },
    { 10, 10, SPECIES_CHARMANDER },
    { 10, 10, SPECIES_SQUIRTLE   },
    { 10, 10, SPECIES_PIKACHU    },
    { 10, 10, SPECIES_EEVEE      },
    { 10, 10, SPECIES_BULBASAUR  },
    { 10, 10, SPECIES_CHARMANDER },
    { 10, 10, SPECIES_SQUIRTLE   },
    { 10, 10, SPECIES_PIKACHU    },
    { 10, 10, SPECIES_EEVEE      },
    { 10, 10, SPECIES_BULBASAUR  },
};

static const struct WildPokemonInfo sTacticalDiverseLandInfo =
{
    .encounterRate = 1,
    .wildPokemon = sTacticalDiverseLandMons,
};

TEST("Tactical wild diversity excludes every slot of an already used species")
{
    const enum Species usedSpecies[] =
    {
        SPECIES_BULBASAUR,
    };

    u8 wildMonIndex = PARTY_SIZE;

    SET_RNG(RNG_TACTICAL_WILD_DIVERSITY, 0);

    EXPECT(TryChooseDistinctTacticalWildMonIndex(
        &sTacticalDiverseLandInfo,
        WILD_AREA_LAND,
        usedSpecies,
        ARRAY_COUNT(usedSpecies),
        &wildMonIndex
    ));

    EXPECT_EQ(wildMonIndex, 2);
    EXPECT_EQ(
        sTacticalDiverseLandMons[wildMonIndex].species,
        SPECIES_CHARMANDER
    );
}

TEST("Tactical wild diversity continues excluding multiple represented species")
{
    const enum Species usedSpecies[] =
    {
        SPECIES_BULBASAUR,
        SPECIES_CHARMANDER,
    };

    u8 wildMonIndex = PARTY_SIZE;

    SET_RNG(RNG_TACTICAL_WILD_DIVERSITY, 0);

    EXPECT(TryChooseDistinctTacticalWildMonIndex(
        &sTacticalDiverseLandInfo,
        WILD_AREA_LAND,
        usedSpecies,
        ARRAY_COUNT(usedSpecies),
        &wildMonIndex
    ));

    EXPECT_EQ(wildMonIndex, 3);
    EXPECT_EQ(
        sTacticalDiverseLandMons[wildMonIndex].species,
        SPECIES_SQUIRTLE
    );
}

TEST("Tactical wild diversity reports exhaustion when every local species is represented")
{
    const enum Species usedSpecies[] =
    {
        SPECIES_BULBASAUR,
        SPECIES_CHARMANDER,
        SPECIES_SQUIRTLE,
        SPECIES_PIKACHU,
        SPECIES_EEVEE,
    };

    u8 wildMonIndex = PARTY_SIZE;

    EXPECT_EQ(
        TryChooseDistinctTacticalWildMonIndex(
            &sTacticalDiverseLandInfo,
            WILD_AREA_LAND,
            usedSpecies,
            ARRAY_COUNT(usedSpecies),
            &wildMonIndex
        ),
        FALSE
    );
}


TEST("Five Pokemon tactical wild pack uses distinct local species before repeats")
{
    EXPECT(GenerateTacticalWildParty(
        &sTacticalDiverseLandInfo,
        WILD_AREA_LAND,
        0,
        5
    ));

    for (u32 i = 0; i < 5; i++)
    {
        enum Species speciesI = GetMonData(
            &gParties[B_TRAINER_OPPONENT_A][i],
            MON_DATA_SPECIES
        );

        for (u32 j = i + 1; j < 5; j++)
        {
            enum Species speciesJ = GetMonData(
                &gParties[B_TRAINER_OPPONENT_A][j],
                MON_DATA_SPECIES
            );

            EXPECT_NE(speciesI, speciesJ);
        }
    }
}


TEST("Tactical wild encounter helper generates the normal two Pokemon party")
{
    SET_RNG(RNG_TACTICAL_WILD_PACK, 0);

    EXPECT(TryGenerateTacticalWildEncounter(
        &sTacticalTestLandInfo,
        WILD_AREA_LAND,
        0
    ));

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_SPECIES),
        SPECIES_BULBASAUR
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][1], MON_DATA_SPECIES),
        SPECIES_BULBASAUR
    );

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][2], MON_DATA_SPECIES),
        SPECIES_NONE
    );
}

TEST("Tactical wild encounter helper generates the five Pokemon pack")
{
    SET_RNG(RNG_TACTICAL_WILD_PACK, 1);

    EXPECT(TryGenerateTacticalWildEncounter(
        &sTacticalTestLandInfo,
        WILD_AREA_LAND,
        0
    ));

    for (u32 i = 0; i < 5; i++)
    {
        EXPECT_EQ(
            GetMonData(&gParties[B_TRAINER_OPPONENT_A][i], MON_DATA_SPECIES),
            SPECIES_BULBASAUR
        );
    }

    EXPECT_EQ(
        GetMonData(&gParties[B_TRAINER_OPPONENT_A][5], MON_DATA_SPECIES),
        SPECIES_NONE
    );
}
