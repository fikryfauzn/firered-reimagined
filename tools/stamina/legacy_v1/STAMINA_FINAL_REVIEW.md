# FireRed Stamina — 00E Final Integrity Review

Status: **PASS**

## Structural checks

- Source moves: **355**
- Draft moves: **355**
- Role-baseline assignments: **0**
- 00D special-case moves validated: **64**
- Errors: **0**
- Warnings: **0**

## Cost distribution

- Cost 0: **2**
- Cost 1: **29**
- Cost 2: **99**
- Cost 3: **133**
- Cost 4: **63**
- Cost 5: **27**
- Cost 6: **2**

## Cost 0

- `MOVE_NONE`
- `MOVE_STRUGGLE`

## Cost 1 — final review

These moves can net +1 shared Stamina over a normal completed turn.

- **MOVE_FORESIGHT** — `setup` / `EFFECT_FORESIGHT` — power 0, acc 100, trainer uses 42, species 31
  - attention: non-damage/utility role: setup
  - rationale: accuracy/evasion/type interaction utility
- **MOVE_EMBER** — `damage` / `EFFECT_BURN_HIT` — power 40, acc 100, trainer uses 34, species 31
  - attention: contains tactical-control/setup/recovery tag
  - rationale: damage baseline from effective power 40
- **MOVE_MUD_SPORT** — `field` / `EFFECT_MUD_SPORT` — power 0, acc 100, trainer uses 24, species 24
  - attention: non-damage/utility role: field
  - rationale: situational field modifier
- **MOVE_ODOR_SLEUTH** — `setup` / `EFFECT_FORESIGHT` — power 0, acc 100, trainer uses 24, species 18
  - attention: non-damage/utility role: setup
  - rationale: accuracy/evasion/type interaction utility
- **MOVE_THUNDER_SHOCK** — `damage` / `EFFECT_PARALYZE_HIT` — power 40, acc 100, trainer uses 23, species 11
  - attention: contains tactical-control/setup/recovery tag
  - rationale: damage baseline from effective power 40
- **MOVE_WATER_SPORT** — `field` / `EFFECT_WATER_SPORT` — power 0, acc 100, trainer uses 18, species 18
  - attention: non-damage/utility role: field
  - rationale: situational field modifier
- **MOVE_TACKLE** — `damage` / `EFFECT_HIT` — power 35, acc 95, trainer uses 181, species 129
  - attention: no structural red flag
  - rationale: damage baseline from effective power 35
- **MOVE_PURSUIT** — `damage` / `EFFECT_PURSUIT` — power 40, acc 100, trainer uses 88, species 41
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_WATER_GUN** — `damage` / `EFFECT_HIT` — power 40, acc 100, trainer uses 78, species 52
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_GUST** — `damage` / `EFFECT_GUST` — power 40, acc 100, trainer uses 68, species 18
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_SCRATCH** — `damage` / `EFFECT_HIT` — power 40, acc 100, trainer uses 34, species 44
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_PAY_DAY** — `damage` / `EFFECT_PAY_DAY` — power 40, acc 100, trainer uses 30, species 2
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_RAPID_SPIN** — `damage` / `EFFECT_RAPID_SPIN` — power 20, acc 100, trainer uses 26, species 18
  - attention: no structural red flag
  - rationale: damage baseline from effective power 20
- **MOVE_CONSTRICT** — `damage` / `EFFECT_SPEED_DOWN_HIT` — power 10, acc 100, trainer uses 19, species 11
  - attention: no structural red flag
  - rationale: damage baseline from effective power 10
- **MOVE_SPLASH** — `utility` / `EFFECT_SPLASH` — power 0, acc 0, trainer uses 14, species 16
  - attention: no structural red flag
  - rationale: intentional no-effect action
- **MOVE_ICICLE_SPEAR** — `damage` / `EFFECT_MULTI_HIT` — power 10, acc 100, trainer uses 13, species 4
  - attention: no structural red flag
  - rationale: damage baseline from effective power 30
- **MOVE_TELEPORT** — `utility` / `EFFECT_TELEPORT` — power 0, acc 0, trainer uses 12, species 10
  - attention: no structural red flag
  - rationale: battle escape utility
- **MOVE_VINE_WHIP** — `damage` / `EFFECT_HIT` — power 35, acc 100, trainer uses 12, species 8
  - attention: no structural red flag
  - rationale: damage baseline from effective power 35
- **MOVE_PECK** — `damage` / `EFFECT_HIT` — power 35, acc 100, trainer uses 11, species 25
  - attention: no structural red flag
  - rationale: damage baseline from effective power 35
- **MOVE_CAMOUFLAGE** — `utility` / `EFFECT_CAMOUFLAGE` — power 0, acc 100, trainer uses 9, species 1
  - attention: no structural red flag
  - rationale: terrain-based self type change
- **MOVE_POUND** — `damage` / `EFFECT_HIT` — power 40, acc 100, trainer uses 8, species 24
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_FALSE_SWIPE** — `damage` / `EFFECT_FALSE_SWIPE` — power 40, acc 100, trainer uses 6, species 16
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_KNOCK_OFF** — `damage` / `EFFECT_KNOCK_OFF` — power 20, acc 100, trainer uses 5, species 13
  - attention: no structural red flag
  - rationale: damage baseline from effective power 20
- **MOVE_SNORE** — `damage` / `EFFECT_SNORE` — power 40, acc 100, trainer uses 4, species 17
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_BULLET_SEED** — `damage` / `EFFECT_MULTI_HIT` — power 10, acc 100, trainer uses 1, species 44
  - attention: no structural red flag
  - rationale: damage baseline from effective power 30
- **MOVE_CONVERSION** — `utility` / `EFFECT_CONVERSION` — power 0, acc 0, trainer uses 1, species 2
  - attention: no structural red flag
  - rationale: self type change
- **MOVE_THIEF** — `damage` / `EFFECT_THIEF` — power 40, acc 100, trainer uses 0, species 173
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_COVET** — `damage` / `EFFECT_THIEF` — power 40, acc 100, trainer uses 0, species 9
  - attention: no structural red flag
  - rationale: damage baseline from effective power 40
- **MOVE_CONVERSION_2** — `utility` / `EFFECT_CONVERSION_2` — power 0, acc 100, trainer uses 0, species 2
  - attention: no structural red flag
  - rationale: reactive self type change

## Cost 6 — final review

- **MOVE_ERUPTION** — `EFFECT_ERUPTION` — power 150, acc 100
  - rationale: HP-scaled power up to 150; spread-target premium +1
- **MOVE_WATER_SPOUT** — `EFFECT_ERUPTION` — power 150, acc 100
  - rationale: HP-scaled power up to 150; spread-target premium +1

## 00D special cases

- **MOVE_ASSIST** — cost **3** — `standard_attempt`, `called_move_caller_only`
- **MOVE_BELLY_DRUM** — cost **4** — `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_BIDE** — cost **3** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_BLAST_BURN** — cost **5** — `standard_attempt`, `recharge_turn_free`
- **MOVE_BOUNCE** — cost **4** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_CHARGE** — cost **2** — `standard_attempt`, `charge_setup_separate_next_move`, `cost_tuning_only`
- **MOVE_CURSE** — cost **3** — `standard_attempt`
- **MOVE_DEFENSE_CURL** — cost **3** — `standard_attempt`, `linked_moves_independent_cost`, `cost_tuning_only`
- **MOVE_DESTINY_BOND** — cost **4** — `standard_attempt`, `delayed_resolution_free`
- **MOVE_DIG** — cost **3** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_DIVE** — cost **3** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_DOOM_DESIRE** — cost **4** — `standard_attempt`, `delayed_resolution_free`
- **MOVE_ENDEAVOR** — cost **4** — `standard_attempt`
- **MOVE_EXPLOSION** — cost **5** — `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_FISSURE** — cost **5** — `standard_attempt`, `cost_tuning_only`
- **MOVE_FLY** — cost **3** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_FOCUS_ENERGY** — cost **2** — `standard_attempt`, `cost_tuning_only`
- **MOVE_FOCUS_PUNCH** — cost **5** — `standard_attempt`, `focus_punch_attempt`
- **MOVE_FRENZY_PLANT** — cost **5** — `standard_attempt`, `recharge_turn_free`
- **MOVE_FURY_CUTTER** — cost **2** — `standard_attempt`, `repeat_reselection_each_time`
- **MOVE_FUTURE_SIGHT** — cost **4** — `standard_attempt`, `delayed_resolution_free`
- **MOVE_GRUDGE** — cost **2** — `standard_attempt`, `pp_asymmetry`
- **MOVE_GUILLOTINE** — cost **5** — `standard_attempt`, `cost_tuning_only`
- **MOVE_HIDDEN_POWER** — cost **3** — `standard_attempt`, `random_result_one_cost`
- **MOVE_HORN_DRILL** — cost **5** — `standard_attempt`, `cost_tuning_only`
- **MOVE_HYDRO_CANNON** — cost **5** — `standard_attempt`, `recharge_turn_free`
- **MOVE_HYPER_BEAM** — cost **5** — `standard_attempt`, `recharge_turn_free`
- **MOVE_ICE_BALL** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_IMPRISON** — cost **2** — `standard_attempt`
- **MOVE_MAGNITUDE** — cost **3** — `standard_attempt`, `random_result_one_cost`
- **MOVE_MEMENTO** — cost **3** — `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_METRONOME** — cost **3** — `standard_attempt`, `called_move_caller_only`
- **MOVE_MIMIC** — cost **2** — `standard_attempt`, `copied_move_future_cost`
- **MOVE_MIRROR_MOVE** — cost **3** — `standard_attempt`, `called_move_caller_only`
- **MOVE_MIST** — cost **2** — `standard_attempt`, `cost_tuning_only`
- **MOVE_NATURE_POWER** — cost **3** — `standard_attempt`, `called_move_caller_only`
- **MOVE_NIGHTMARE** — cost **3** — `standard_attempt`, `delayed_resolution_free`
- **MOVE_OUTRAGE** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_PAIN_SPLIT** — cost **3** — `standard_attempt`
- **MOVE_PERISH_SONG** — cost **4** — `standard_attempt`, `delayed_resolution_free`
- **MOVE_PETAL_DANCE** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_PRESENT** — cost **2** — `standard_attempt`, `random_result_one_cost`
- **MOVE_RAGE** — cost **2** — `standard_attempt`, `repeat_reselection_each_time`
- **MOVE_RAZOR_WIND** — cost **3** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_ROLLOUT** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_SECRET_POWER** — cost **3** — `standard_attempt`, `random_result_one_cost`
- **MOVE_SELF_DESTRUCT** — cost **5** — `standard_attempt`, `hp_or_self_cost_no_refund`
- **MOVE_SHEER_COLD** — cost **5** — `standard_attempt`, `cost_tuning_only`
- **MOVE_SKETCH** — cost **3** — `standard_attempt`, `copied_move_future_cost`
- **MOVE_SKULL_BASH** — cost **4** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_SKY_ATTACK** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_SLEEP_TALK** — cost **2** — `standard_attempt`, `called_move_caller_only`
- **MOVE_SOLAR_BEAM** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_SPITE** — cost **2** — `standard_attempt`, `pp_asymmetry`
- **MOVE_SPIT_UP** — cost **4** — `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_SPLASH** — cost **1** — `standard_attempt`, `cost_tuning_only`
- **MOVE_STOCKPILE** — cost **2** — `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_STRUGGLE** — cost **0** — `struggle_fallback`
- **MOVE_SWALLOW** — cost **3** — `standard_attempt`, `linked_moves_independent_cost`
- **MOVE_TELEPORT** — cost **1** — `standard_attempt`, `cost_tuning_only`
- **MOVE_THRASH** — cost **5** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_TRANSFORM** — cost **3** — `standard_attempt`, `copied_move_future_cost`
- **MOVE_UPROAR** — cost **4** — `standard_attempt`, `forced_multiturn_single_commit`
- **MOVE_WISH** — cost **3** — `standard_attempt`, `delayed_resolution_free`

## Errors

None.

## Freeze condition

If this gate reports PASS and the cost-1/cost-6 lists are accepted, the reviewed draft can be frozen into authored `stamina_moves.json`.
