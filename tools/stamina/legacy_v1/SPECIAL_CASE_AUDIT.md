# FireRed Stamina — Objective 00D Special-Case Audit

This report is generated from Objectives 00A–00C.

No numeric Stamina costs are assigned here.

## Global execution rule

- Pay Stamina only when the selected move genuinely begins its attempt.
- Do not pay when a pre-action blocker prevents the move from beginning.
- Once the attempt begins, miss/immunity/Protect/effect failure does not refund it.

## Special-case rules

### `standard_attempt` — 63 flagged move(s)

Pay the selected move's Stamina once when the move genuinely begins its attempt. No refund for miss, immunity, Protect, effect failure, or other failure after the attempt begins.

Implementation: Do not charge if a pre-action blocker prevents the move from beginning at all (sleep, freeze, flinch, full paralysis, etc.).

### `struggle_fallback` — 1 flagged move(s)

Struggle is the emergency action when no normal player move is affordable.

Implementation: Struggle costs 0 Stamina. It is not a normal low-cost tactical option and should only be offered/forced by the no-affordable-move fallback condition.

### `forced_multiturn_single_commit` — 15 flagged move(s)

Pay once when the player initially commits to the move. Forced continuation turns do not consume additional Stamina.

Implementation: Affordability is checked only when the player selects the initial move. Automatic continuation/resolution must not re-check or re-charge Stamina.

### `recharge_turn_free` — 4 flagged move(s)

Pay once for the attacking move. The forced recharge turn costs no Stamina.

Implementation: Recharge is not a new player-selected action, so it cannot create a second resource charge.

### `called_move_caller_only` — 5 flagged move(s)

Pay only the move the player selected (Metronome, Sleep Talk, Assist, Mirror Move, Nature Power). The called move costs no additional Stamina.

Implementation: The called move may execute even when its standalone Stamina cost would exceed the remaining pool. There is no hidden second cost.

### `copied_move_future_cost` — 3 flagged move(s)

Pay the copy/transform move when it is used. A copied move later selected directly uses that copied move's normal Stamina cost.

Implementation: Mimic/Sketch/Transform do not pre-pay future uses and do not make copied moves free.

### `delayed_resolution_free` — 6 flagged move(s)

Pay when the player selects and attempts the move. Delayed damage, healing, residual damage, KO reaction, or timer resolution costs no additional Stamina.

Implementation: The later battle event is a consequence of an already-paid action, not a new action selection.

### `repeat_reselection_each_time` — 2 flagged move(s)

If the player must manually select the move again on later turns, each new selection pays that move's normal Stamina cost.

Implementation: This applies to repeated-use scaling such as Rage and Fury Cutter. They are not treated as automatic locked continuations.

### `linked_moves_independent_cost` — 4 flagged move(s)

Each separately selected move in a linked family pays its own Stamina cost.

Implementation: Stockpile does not pre-pay Spit Up or Swallow. Defense Curl does not discount or pre-pay Rollout/Ice Ball.

### `pp_asymmetry` — 2 flagged move(s)

PP-manipulation moves continue to interact with enemy PP, because the enemy still uses vanilla PP. They do not reduce player Stamina.

Implementation: When an enemy PP-reduction effect targets the player, its PP change may become tactically irrelevant once player PP is bypassed. Do not secretly convert PP loss into Stamina loss in V1.

### `focus_punch_attempt` — 1 flagged move(s)

Focus Punch pays if its move attempt has begun, even if the user later loses focus from taking damage.

Implementation: A pre-action blocker that prevents the move from beginning still follows the global no-charge rule. Losing focus after commitment is not a refund.

### `random_result_one_cost` — 4 flagged move(s)

Random or dynamically calculated outcomes do not alter Stamina after selection.

Implementation: Present, Magnitude, Hidden Power, Secret Power, and similar moves pay exactly their selected move cost once, regardless of the result rolled/calculated.

### `charge_setup_separate_next_move` — 1 flagged move(s)

Charge pays its own Stamina cost. A later Electric attack is a new player-selected action and pays its own normal Stamina cost.

Implementation: The temporary charged state does not pre-pay the next Electric move and does not add an extra surcharge to it.

### `hp_or_self_cost_no_refund` — 4 flagged move(s)

HP loss, self-KO, recoil, or other built-in sacrifice remains an independent move drawback and does not refund Stamina.

Implementation: Stamina is the action cost; HP/recoil/self-KO is the move's existing combat cost.

### `cost_tuning_only` — 10 flagged move(s)

No special Stamina execution logic is required. The move only needs careful numeric cost tuning later.

Implementation: Use standard attempt semantics unless another rule is attached.

## Flagged moves

- **MOVE_GUILLOTINE** — `EFFECT_OHKO` — flags: `ohko` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_RAZOR_WIND** — `EFFECT_RAZOR_WIND` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_FLY** — `EFFECT_SEMI_INVULNERABLE` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_HORN_DRILL** — `EFFECT_OHKO` — flags: `ohko` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_THRASH** — `EFFECT_RAMPAGE` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_MIST** — `EFFECT_MIST` — flags: `utility_value_review` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_HYPER_BEAM** — `EFFECT_RECHARGE` — flags: `recharge_turn` — rules: `standard_attempt`, `recharge_turn_free`
- **MOVE_SOLAR_BEAM** — `EFFECT_SOLAR_BEAM` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_PETAL_DANCE** — `EFFECT_RAMPAGE` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_FISSURE** — `EFFECT_OHKO` — flags: `ohko` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_DIG** — `EFFECT_SEMI_INVULNERABLE` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_RAGE** — `EFFECT_RAGE` — flags: `repeat_scaling` — rules: `standard_attempt`, `repeat_reselection_each_time`
- **MOVE_TELEPORT** — `EFFECT_TELEPORT` — flags: `utility_value_review` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_MIMIC** — `EFFECT_MIMIC` — flags: `copied_move_interaction` — rules: `standard_attempt`, `copied_move_future_cost`
- **MOVE_DEFENSE_CURL** — `EFFECT_DEFENSE_CURL` — flags: `linked_move_family`, `utility_value_review` — rules: `standard_attempt`, `linked_moves_independent_cost`, `cost_tuning_only`
- **MOVE_FOCUS_ENERGY** — `EFFECT_FOCUS_ENERGY` — flags: `utility_value_review` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_BIDE** — `EFFECT_BIDE` — flags: `effect_specific_review` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_METRONOME** — `EFFECT_METRONOME` — flags: `called_move_cost_rule` — rules: `standard_attempt`, `called_move_caller_only`
- **MOVE_MIRROR_MOVE** — `EFFECT_MIRROR_MOVE` — flags: `called_move_cost_rule` — rules: `standard_attempt`, `called_move_caller_only`
- **MOVE_SELF_DESTRUCT** — `EFFECT_EXPLOSION` — flags: `self_sacrifice` — rules: `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_SKULL_BASH** — `EFFECT_SKULL_BASH` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_SKY_ATTACK** — `EFFECT_SKY_ATTACK` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_TRANSFORM** — `EFFECT_TRANSFORM` — flags: `copied_move_interaction` — rules: `standard_attempt`, `copied_move_future_cost`
- **MOVE_SPLASH** — `EFFECT_SPLASH` — flags: `utility_value_review` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_EXPLOSION** — `EFFECT_EXPLOSION` — flags: `self_sacrifice` — rules: `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_STRUGGLE** — `EFFECT_RECOIL` — flags: `stamina_fallback_rule` — rules: `struggle_fallback`
- **MOVE_SKETCH** — `EFFECT_SKETCH` — flags: `copied_move_interaction` — rules: `standard_attempt`, `copied_move_future_cost`
- **MOVE_NIGHTMARE** — `EFFECT_NIGHTMARE` — flags: `effect_specific_review` — rules: `standard_attempt`, `delayed_resolution_free`
- **MOVE_CURSE** — `EFFECT_CURSE` — flags: `effect_specific_review` — rules: `standard_attempt`
- **MOVE_SPITE** — `EFFECT_SPITE` — flags: `player_pp_replacement` — rules: `standard_attempt`, `pp_asymmetry`
- **MOVE_BELLY_DRUM** — `EFFECT_BELLY_DRUM` — flags: `effect_specific_review` — rules: `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_DESTINY_BOND** — `EFFECT_DESTINY_BOND` — flags: `effect_specific_review` — rules: `standard_attempt`, `delayed_resolution_free`
- **MOVE_PERISH_SONG** — `EFFECT_PERISH_SONG` — flags: `perish_timer` — rules: `standard_attempt`, `delayed_resolution_free`
- **MOVE_OUTRAGE** — `EFFECT_RAMPAGE` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_ROLLOUT** — `EFFECT_ROLLOUT` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_FURY_CUTTER** — `EFFECT_FURY_CUTTER` — flags: `repeat_scaling` — rules: `standard_attempt`, `repeat_reselection_each_time`
- **MOVE_SLEEP_TALK** — `EFFECT_SLEEP_TALK` — flags: `called_move_cost_rule` — rules: `standard_attempt`, `called_move_caller_only`
- **MOVE_PRESENT** — `EFFECT_PRESENT` — flags: `effect_specific_review` — rules: `standard_attempt`, `random_result_one_cost`
- **MOVE_PAIN_SPLIT** — `EFFECT_PAIN_SPLIT` — flags: `effect_specific_review` — rules: `standard_attempt`
- **MOVE_MAGNITUDE** — `EFFECT_MAGNITUDE` — flags: `effect_specific_review` — rules: `standard_attempt`, `random_result_one_cost`
- **MOVE_HIDDEN_POWER** — `EFFECT_HIDDEN_POWER` — flags: `effect_specific_review` — rules: `standard_attempt`, `random_result_one_cost`
- **MOVE_FUTURE_SIGHT** — `EFFECT_FUTURE_SIGHT` — flags: `delayed_execution`, `effect_specific_review` — rules: `standard_attempt`, `delayed_resolution_free`
- **MOVE_UPROAR** — `EFFECT_UPROAR` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_STOCKPILE** — `EFFECT_STOCKPILE` — flags: `effect_specific_review`, `linked_move_family` — rules: `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_SPIT_UP** — `EFFECT_SPIT_UP` — flags: `effect_specific_review`, `linked_move_family` — rules: `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_SWALLOW** — `EFFECT_SWALLOW` — flags: `effect_specific_review`, `linked_move_family` — rules: `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_MEMENTO** — `EFFECT_MEMENTO` — flags: `self_sacrifice` — rules: `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_FOCUS_PUNCH** — `EFFECT_FOCUS_PUNCH` — flags: `effect_specific_review` — rules: `standard_attempt`, `focus_punch_attempt`
- **MOVE_NATURE_POWER** — `EFFECT_NATURE_POWER` — flags: `called_move_cost_rule` — rules: `standard_attempt`, `called_move_caller_only`
- **MOVE_CHARGE** — `EFFECT_CHARGE` — flags: `effect_specific_review`, `utility_value_review` — rules: `standard_attempt`, `charge_setup_separate_next_move`, `cost_tuning_only`
- **MOVE_WISH** — `EFFECT_WISH` — flags: `effect_specific_review` — rules: `standard_attempt`, `delayed_resolution_free`
- **MOVE_ASSIST** — `EFFECT_ASSIST` — flags: `called_move_cost_rule` — rules: `standard_attempt`, `called_move_caller_only`
- **MOVE_ENDEAVOR** — `EFFECT_ENDEAVOR` — flags: `effect_specific_review` — rules: `standard_attempt`
- **MOVE_IMPRISON** — `EFFECT_IMPRISON` — flags: `effect_specific_review` — rules: `standard_attempt`
- **MOVE_GRUDGE** — `EFFECT_GRUDGE` — flags: `effect_specific_review`, `player_pp_replacement` — rules: `standard_attempt`, `pp_asymmetry`
- **MOVE_SECRET_POWER** — `EFFECT_SECRET_POWER` — flags: `effect_specific_review` — rules: `standard_attempt`, `random_result_one_cost`
- **MOVE_DIVE** — `EFFECT_SEMI_INVULNERABLE` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_ICE_BALL** — `EFFECT_ROLLOUT` — flags: `forced_or_chained_turns` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_BLAST_BURN** — `EFFECT_RECHARGE` — flags: `recharge_turn` — rules: `standard_attempt`, `recharge_turn_free`
- **MOVE_HYDRO_CANNON** — `EFFECT_RECHARGE` — flags: `recharge_turn` — rules: `standard_attempt`, `recharge_turn_free`
- **MOVE_SHEER_COLD** — `EFFECT_OHKO` — flags: `ohko` — rules: `standard_attempt`, `cost_tuning_only`
- **MOVE_FRENZY_PLANT** — `EFFECT_RECHARGE` — flags: `recharge_turn` — rules: `standard_attempt`, `recharge_turn_free`
- **MOVE_BOUNCE** — `EFFECT_SEMI_INVULNERABLE` — flags: `multi_turn_commitment` — rules: `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_DOOM_DESIRE** — `EFFECT_FUTURE_SIGHT` — flags: `delayed_execution`, `effect_specific_review` — rules: `standard_attempt`, `delayed_resolution_free`

## Unresolved

None. All 00C review flags map to an explicit V1 rule.

## PP asymmetry note

Spite/Grudge remain useful when the player targets the enemy because the enemy retains vanilla PP. Enemy PP-manipulation against the player does not convert into Stamina loss in V1. This is a known asymmetry, not an accidental omission.

## Next

After this audit has zero unresolved flags, Objective 00E assigns prototype numeric Stamina costs.
