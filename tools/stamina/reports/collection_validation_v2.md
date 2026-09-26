# Stamina V2 — Expansion Data Collection Validation

- Git commit: `2cfbd9a89167687b9562f7a534a0753c870c27e3`
- Branch at collection: `tactical-firered`
- Working tree dirty before collection: `True`

## Canonical move universe

- Normal move slots: **848** (`0..847`)
- Parsed normal `gMovesInfo` records: **848**
- Missing normal records: **0**
- Z-Move IDs: **848..882**
- Max/G-Max IDs: **883..934**
- All engine move slots: **935**

## Learnability/context

- Active level-up generation: **Gen 9**
- Active level-up learnsets: **1104**
- Unique moves in active level-up learnsets: **719**
- Active level-up entries: **16616**
- `all_learnables.json` species keys: **1110**
- Unique moves in `all_learnables.json`: **824**
- Egg-move learnsets: **418**
- Unique egg moves: **435**
- Current TMs: **50**
- Current HMs: **8**

## Trainer context

- Explicit move lines resolved in `trainers_frlg.party`: **1592**
- Explicit move lines unresolved by move-name mapping: **33**

> This trainer count is intentionally incomplete. Most vanilla FRLG trainer Pokémon
> omit explicit moves and receive moves from level-up/default logic. A later
> campaign-menu collector must reconstruct those actual four-move menus.

## Gate result

**PASS — canonical Expansion move/source extraction and first availability/context layer are complete.**

This is not yet the Stamina-cost freeze. No costs are assigned by this collector.
