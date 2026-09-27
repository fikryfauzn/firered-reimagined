#ifndef GUARD_BATTLE_STAMINA_H
#define GUARD_BATTLE_STAMINA_H

#include "global.h"

bool32 IsPlayerStaminaEnabled(void);
bool32 IsBattlerStaminaEnabled(enum BattlerId battler);
u8 GetMoveStaminaCost(enum Move move);
bool32 CanBattlerAffordMoveStamina(enum BattlerId battler, enum Move move);
bool32 TrySpendBattlerStamina(enum BattlerId battler, enum Move move);
void RegeneratePlayerStamina(void);

#endif // GUARD_BATTLE_STAMINA_H
