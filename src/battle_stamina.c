#include "global.h"
#include "battle.h"
#include "battle_stamina.h"
#include "constants/battle.h"
#include "constants/moves.h"

#include "data/stamina_move_costs.h"

bool32 IsPlayerStaminaEnabled(void)
{
    if (gBattleTypeFlags & (BATTLE_TYPE_LINK
                          | BATTLE_TYPE_SAFARI
                          | BATTLE_TYPE_POKEDUDE))
    {
        return FALSE;
    }

    return TRUE;
}

bool32 IsBattlerStaminaEnabled(enum BattlerId battler)
{
    return IsPlayerStaminaEnabled()
        && IsOnPlayerSide(battler);
}

u8 GetMoveStaminaCost(enum Move move)
{
    if (move >= MOVES_COUNT)
        return 0;

    return gStaminaMoveCosts[move];
}

bool32 CanBattlerAffordMoveStamina(enum BattlerId battler, enum Move move)
{
    if (!IsBattlerStaminaEnabled(battler))
        return TRUE;

    if (move >= MOVES_COUNT)
        return FALSE;

    return GetMoveStaminaCost(move) <= gBattleStruct->playerStamina;
}

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

void RegeneratePlayerStamina(void)
{
    u8 stamina;

    if (!IsPlayerStaminaEnabled())
        return;

    stamina = gBattleStruct->playerStamina + BATTLE_STAMINA_REGEN;

    if (stamina > BATTLE_STAMINA_MAX)
        stamina = BATTLE_STAMINA_MAX;

    gBattleStruct->playerStamina = stamina;
}
