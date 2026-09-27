#include "global.h"
#include "test/battle.h"
#include "battle_stamina.h"
#include "constants/battle.h"

ASSUMPTIONS
{
    ASSUME(GetMoveStaminaCost(MOVE_SURF) == 4);
    ASSUME(GetMoveStaminaCost(MOVE_SCRATCH) == 1);
}

SINGLE_BATTLE_TEST("Stamina starts at maximum before the first move")
{
    GIVEN {
        ASSUME(GetMoveStaminaCost(MOVE_ERUPTION) == BATTLE_STAMINA_MAX);

        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            Moves(MOVE_ERUPTION);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        TURN {
            MOVE(player, MOVE_ERUPTION);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ERUPTION, player);
    } THEN {
        // A cost-6 move can execute on turn 1 only if the pool starts at 6.
        // 6 - 6 + 2 = 2.
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 2);
    }
}

SINGLE_BATTLE_TEST("Stamina regeneration is capped at maximum")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Attack(1);
            Moves(MOVE_SCRATCH);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            Defense(1000);
        }
    } WHEN {
        TURN {
            MOVE(player, MOVE_SCRATCH);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, player);
    } THEN {
        // 6 - 1 + 2 would be 7 without the cap.
        EXPECT_EQ((u8)gBattleStruct->playerStamina, BATTLE_STAMINA_MAX);
    }
}

SINGLE_BATTLE_TEST("Stamina spends move cost and regenerates once after the turn")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            MovesWithPP({MOVE_SURF, 1});
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
    } THEN {
        // 6 - 4 + 2 = 4.
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);

        // Stored player PP remains compatibility data.
        EXPECT_EQ(player->pp[0], 1);
    }
}

SINGLE_BATTLE_TEST("Stamina allows player move use at zero stored PP")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            MovesWithPP({MOVE_SURF, 0});
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
        NOT MESSAGE("But there was no PP left for the move!");
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);
        EXPECT_EQ(player->pp[0], 0);
    }
}

SINGLE_BATTLE_TEST("Stamina preserves enemy PP consumption")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET) {
            MovesWithPP({MOVE_SCRATCH, 1});
        }
    } WHEN {
        TURN {
            MOVE(opponent, MOVE_SCRATCH);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
    } THEN {
        EXPECT_EQ(opponent->pp[0], 0);
    }
}

SINGLE_BATTLE_TEST("Stamina switching does not refill the shared pool")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        PLAYER(SPECIES_WYNAUT);

        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Start 6.
        // Turn 1: 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Turn 2: 4 - 4 + 2 = 2.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Switching must not refill to 6.
        // Turn 3: 2 + 2 regeneration = 4.
        TURN {
            SWITCH(player, 1);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);
    }
}

SINGLE_BATTLE_TEST("Stamina is not spent when flinch prevents the move attempt")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Speed(200);
            SpAttack(1);
            Moves(MOVE_SURF, MOVE_SCRATCH);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            Speed(300);
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
            Moves(MOVE_CELEBRATE, MOVE_AIR_SLASH);
        }
    } WHEN {
        // First reduce the pool:
        // 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Air Slash flinches before Scratch reaches the payment boundary.
        // Correct result: 4 + 2 = 6.
        // Incorrect early payment would produce: 4 - 1 + 2 = 5.
        TURN {
            MOVE(opponent, MOVE_AIR_SLASH);
            MOVE(player, MOVE_SCRATCH);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_AIR_SLASH, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, player);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 6);
    }
}

SINGLE_BATTLE_TEST("Stamina is not spent when sleep prevents the move attempt")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Speed(300);
            SpAttack(1);
            Moves(MOVE_SURF, MOVE_SCRATCH);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            Speed(100);
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
            Moves(MOVE_SPORE, MOVE_CELEBRATE);
        }
    } WHEN {
        // Surf executes before the slower opponent puts the player to sleep.
        // End of turn pool: 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_SPORE);
        }

        // Scratch is selected while asleep but never reaches the attempt
        // payment boundary. End result should return to 6.
        TURN {
            MOVE(player, MOVE_SCRATCH);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SPORE, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, player);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 6);
    }
}

SINGLE_BATTLE_TEST("Stamina is spent when Protect blocks an attempted move")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Speed(200);
            SpAttack(1);
            Moves(MOVE_SURF, MOVE_SCRATCH);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            Speed(100);
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
            Moves(MOVE_PROTECT, MOVE_CELEBRATE);
        }
    } WHEN {
        // 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Keep the same speed relationship as turn 1.
        // Protect still executes first because of move priority.
        //
        // Scratch reaches the attempt boundary and pays before Protect
        // resolves the failure:
        // 4 - 1 + 2 = 5.
        TURN {
            MOVE(player, MOVE_SCRATCH);
            MOVE(opponent, MOVE_PROTECT);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PROTECT, opponent);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 5);
    }
}

SINGLE_BATTLE_TEST("Stamina is spent when type immunity blocks an attempted move")
{
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_DRIFBLIM, 0) == TYPE_GHOST
            || GetSpeciesType(SPECIES_DRIFBLIM, 1) == TYPE_GHOST);
        ASSUME(GetMoveType(MOVE_SCRATCH) == TYPE_NORMAL);

        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            Moves(MOVE_SURF, MOVE_SCRATCH);
        }
        OPPONENT(SPECIES_DRIFBLIM) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Surf is not blocked by Ghost typing:
        // 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Scratch attempts to hit a Ghost:
        // 4 - 1 + 2 = 5.
        TURN {
            MOVE(player, MOVE_SCRATCH);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, player);
        MESSAGE("It doesn't affect the opposing Drifblim…");
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 5);
    }
}


SINGLE_BATTLE_TEST("Stamina is spent when a move misses")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Missing happens after the attempt/payment boundary.
        //
        // 6 - 4 + 2 = 4.
        TURN {
            MOVE(player, MOVE_SURF, hit: FALSE);
        }
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);
    }
}

SINGLE_BATTLE_TEST("Stamina is not spent when full paralysis prevents the move attempt")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Status1(STATUS1_PARALYSIS);
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Full paralysis occurs before the payment boundary.
        //
        // No spend:
        // 6 + 2 => capped at 6.
        //
        // An incorrect cost-4 spend would leave 4.
        TURN {
            MOVE(
                player,
                MOVE_SURF,
                WITH_RNG(RNG_PARALYSIS, TRUE)
            );
        }
    } THEN {
        EXPECT_EQ(
            (u8)gBattleStruct->playerStamina,
            BATTLE_STAMINA_MAX
        );
    }
}

SINGLE_BATTLE_TEST("Stamina is not spent when freeze prevents the move attempt")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) {
            Status1(STATUS1_FREEZE);
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // RNG_FROZEN == 0 keeps the battler frozen solid.
        // Freeze prevention occurs before the payment boundary.
        //
        // No spend:
        // 6 + 2 => capped at 6.
        //
        // An incorrect cost-4 spend would leave 4.
        TURN {
            MOVE(
                player,
                MOVE_SURF,
                WITH_RNG(RNG_FROZEN, 0)
            );
        }
    } THEN {
        EXPECT_EQ(
            (u8)gBattleStruct->playerStamina,
            BATTLE_STAMINA_MAX
        );
    }
}


SINGLE_BATTLE_TEST("Stamina charges a two-turn move only on initial commitment")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_RAZOR_WIND) == EFFECT_TWO_TURNS_ATTACK);
        ASSUME(GetMoveStaminaCost(MOVE_RAZOR_WIND) == 3);

        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            Moves(MOVE_RAZOR_WIND);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Initial commitment:
        // 6 - 3 + 2 = 5.
        TURN {
            MOVE(player, MOVE_RAZOR_WIND);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Automatic continuation must be free:
        // 5 + 2 => capped at 6.
        //
        // If charged a second time:
        // 5 - 3 + 2 = 4.
        TURN {
            SKIP_TURN(player);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        MESSAGE("Wobbuffet used Razor Wind!");
        MESSAGE("Wobbuffet whipped up a whirlwind!");

        // Attack resolves automatically on turn 2.
        ANIMATION(ANIM_TYPE_MOVE, MOVE_RAZOR_WIND, player);
        HP_BAR(opponent);
    } THEN {
        EXPECT_EQ(
            (u8)gBattleStruct->playerStamina,
            BATTLE_STAMINA_MAX
        );
    }
}

SINGLE_BATTLE_TEST("Stamina does not charge the forced recharge turn")
{
    GIVEN {
        ASSUME(GetMoveStaminaCost(MOVE_METEOR_ASSAULT) == 5);

        PLAYER(SPECIES_WOBBUFFET) {
            Attack(1);
            Moves(MOVE_METEOR_ASSAULT);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            Defense(1000);
        }
    } WHEN {
        // Attack:
        // 6 - 5 + 2 = 3.
        TURN {
            MOVE(player, MOVE_METEOR_ASSAULT);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Recharge is an automatic non-move turn and must not spend.
        // 3 + 2 = 5.
        TURN {
            SKIP_TURN(player);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_METEOR_ASSAULT, player);
        MESSAGE("Wobbuffet must recharge!");
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 5);
    }
}

SINGLE_BATTLE_TEST("Stamina fallback Struggle is free when no normal move is affordable")
{
    GIVEN {
        ASSUME(GetMoveStaminaCost(MOVE_ERUPTION) == 6);
        ASSUME(GetMoveStaminaCost(MOVE_STRUGGLE) == 0);

        PLAYER(SPECIES_WOBBUFFET) {
            MaxHP(10000);
            HP(10000);
            SpAttack(1);
            Attack(1);
            Moves(MOVE_ERUPTION);
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            Defense(1000);
            SpDefense(1000);
        }
    } WHEN {
        // Turn 1:
        // 6 - 6 + 2 = 2.
        TURN {
            MOVE(player, MOVE_ERUPTION);
            MOVE(opponent, MOVE_CELEBRATE);
        }

        // Eruption costs 6 but only 2 Stamina remains.
        //
        // Mark the explicitly known move as unavailable. With no other
        // selectable normal move, the real battle engine must fall back
        // to Struggle.
        //
        // Struggle is free:
        // 2 + 2 = 4.
        TURN {
            MOVE(player, MOVE_ERUPTION, allowed: FALSE);
            MOVE(opponent, MOVE_CELEBRATE);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ERUPTION, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STRUGGLE, player);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);
    }
}

SINGLE_BATTLE_TEST("Stamina charges Sleep Talk caller once and called move is free")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_SLEEP_TALK) == EFFECT_SLEEP_TALK);
        ASSUME(GetMoveStaminaCost(MOVE_SLEEP_TALK) == 2);

        // The called move must have a positive cost so this test detects
        // accidental charging of either the called result or caller twice.
        ASSUME(GetMoveStaminaCost(MOVE_POUND) > 0);

        PLAYER(SPECIES_WOBBUFFET) {
            Status1(STATUS1_SLEEP);
            MovesWithPP(
                {MOVE_SLEEP_TALK, 10},
                {MOVE_POUND, 35}
            );
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            Defense(1000);
        }
    } WHEN {
        // Correct:
        // 6 - 2 + 2 = 6.
        //
        // Any second Stamina payment produces a value below 6.
        TURN {
            MOVE(player, MOVE_SLEEP_TALK);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SLEEP_TALK, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_POUND, player);
    } THEN {
        EXPECT_EQ(
            (u8)gBattleStruct->playerStamina,
            BATTLE_STAMINA_MAX
        );

        // Stamina mode does not consume stored player PP.
        EXPECT_EQ(player->pp[0], 10);
        EXPECT_EQ(player->pp[1], 35);
    }
}

SINGLE_BATTLE_TEST("Stamina charges Metronome caller once and generated move is free")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_METRONOME) == EFFECT_METRONOME);
        ASSUME(GetMoveStaminaCost(MOVE_METRONOME) == 3);
        ASSUME(GetMoveStaminaCost(MOVE_SCRATCH) == 1);

        PLAYER(SPECIES_WOBBUFFET) {
            Attack(1);
            MovesWithPP({MOVE_METRONOME, 10});
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            Defense(1000);
        }
    } WHEN {
        // Correct:
        // Metronome costs 3.
        //
        // 6 - 3 + 2 = 5.
        //
        // If Scratch were incorrectly charged too:
        // 6 - 3 - 1 + 2 = 4.
        //
        // If Metronome were charged twice:
        // 6 - 3 - 3 + 2 = 2.
        TURN {
            MOVE(
                player,
                MOVE_METRONOME,
                WITH_RNG(RNG_METRONOME, MOVE_SCRATCH)
            );
        }
    } SCENE {
        MESSAGE("Wobbuffet used Metronome!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_METRONOME, player);
        MESSAGE("Waggling a finger let it use Scratch!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, player);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 5);

        // Stored compatibility PP remains untouched.
        EXPECT_EQ(player->pp[0], 10);
    }
}


DOUBLE_BATTLE_TEST("Stamina uses one shared pool across both player battlers")
{
    GIVEN {
        ASSUME(GetMoveStaminaCost(MOVE_SURF) == 4);
        ASSUME(GetMoveStaminaCost(MOVE_SCRATCH) == 1);

        PLAYER(SPECIES_WOBBUFFET) {
            Speed(300);
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        PLAYER(SPECIES_WYNAUT) {
            Speed(200);
            Attack(1);
            Moves(MOVE_SCRATCH);
        }

        OPPONENT(SPECIES_WOBBUFFET) {
            Speed(100);
            HP(10000);
            MaxHP(10000);
            Defense(1000);
            SpDefense(1000);
        }
        OPPONENT(SPECIES_WYNAUT) {
            Speed(50);
            HP(10000);
            MaxHP(10000);
            Defense(1000);
            SpDefense(1000);
        }
    } WHEN {
        // Shared pool:
        // 6 - 4 - 1 + 2 = 3.
        TURN {
            MOVE(playerLeft, MOVE_SURF, target: opponentLeft);
            MOVE(playerRight, MOVE_SCRATCH, target: opponentRight);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, playerLeft);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, playerRight);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 3);
    }
}

DOUBLE_BATTLE_TEST("Stamina execution guard rejects doubles overcommit")
{
    GIVEN {
        ASSUME(GetMoveStaminaCost(MOVE_SURF) == 4);

        PLAYER(SPECIES_WOBBUFFET) {
            Speed(300);
            SpAttack(1);
            Moves(MOVE_SURF);
        }
        PLAYER(SPECIES_WYNAUT) {
            Speed(200);
            SpAttack(1);
            Moves(MOVE_SURF);
        }

        OPPONENT(SPECIES_WOBBUFFET) {
            Speed(100);
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
        OPPONENT(SPECIES_WYNAUT) {
            Speed(50);
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Both moves are selected while the pool is 6.
        //
        // First Surf:
        // 6 - 4 = 2.
        //
        // Second Surf reaches execution with only 2 remaining and must
        // be rejected by the runtime affordability guard.
        //
        // End-turn regeneration:
        // 2 + 2 = 4.
        TURN {
            MOVE(playerLeft, MOVE_SURF, target: opponentLeft);
            MOVE(playerRight, MOVE_SURF, target: opponentRight);
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, playerLeft);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_SURF, playerRight);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 4);
    }
}

SINGLE_BATTLE_TEST("Stamina prices Z-Move from its ordinary base move")
{
    GIVEN {
        ASSUME(GetMoveType(MOVE_HYPER_BEAM) == TYPE_NORMAL);
        ASSUME(GetMoveStaminaCost(MOVE_HYPER_BEAM) == 5);

        PLAYER(SPECIES_WOBBUFFET) {
            Item(ITEM_NORMALIUM_Z);
            SpAttack(1);
            MovesWithPP({MOVE_HYPER_BEAM, 1});
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Hyper Beam becomes Breakneck Blitz, but Stamina must price
        // the ordinary base move:
        //
        // 6 - 5 + 2 = 3.
        TURN {
            MOVE(
                player,
                MOVE_HYPER_BEAM,
                gimmick: GIMMICK_Z_MOVE
            );
        }
    } SCENE {
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_ZMOVE_ACTIVATE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BREAKNECK_BLITZ, player);
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 3);
        EXPECT_EQ(player->pp[0], 1);
    }
}

SINGLE_BATTLE_TEST("Stamina prices Max Move from its ordinary base move")
{
    GIVEN {
        ASSUME(GetMoveType(MOVE_HYPER_BEAM) == TYPE_NORMAL);
        ASSUME(GetMoveStaminaCost(MOVE_HYPER_BEAM) == 5);

        PLAYER(SPECIES_WOBBUFFET) {
            SpAttack(1);
            MovesWithPP({MOVE_HYPER_BEAM, 1});
        }
        OPPONENT(SPECIES_WOBBUFFET) {
            HP(10000);
            MaxHP(10000);
            SpDefense(1000);
        }
    } WHEN {
        // Hyper Beam becomes Max Strike, but Stamina must price
        // the ordinary base move:
        //
        // 6 - 5 + 2 = 3.
        TURN {
            MOVE(
                player,
                MOVE_HYPER_BEAM,
                gimmick: GIMMICK_DYNAMAX
            );
        }
    } SCENE {
        MESSAGE("Wobbuffet used Max Strike!");
    } THEN {
        EXPECT_EQ((u8)gBattleStruct->playerStamina, 3);
        EXPECT_EQ(player->pp[0], 1);
    }
}
