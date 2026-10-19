# Data Quality

## Record grain and denominators

Matches, participant observations, stages, and unit snapshots have different grains. Participants in the same match have related outcomes, and stages repeatedly observe the same participant. When describing a source profile's lineup frequency, count one observation for that profile per match. Do not treat all participants as additional independent players.

## Keep these concepts separate

- Analyze modes separately. Resource scales, stage structures, and starting levels may differ.
- Preserve unknown versions, patches, and source-time timezones as unknown. Calendar groups are not patch groups.
- Separate final lineups from stage boards. Final-only analysis can miss transition units.
- Separate card-count summaries from input actions. Acquisition is not necessarily a purchase; removal is not necessarily a sale.
- Do not claim deduplication across player views until the global identity of source match identifiers has been verified.

## Limits of the current private sample

The private structural review covers 476 matches reached through a single source profile, not a random sample across competitive tiers. Successfully retrieved details may favor newer or more accessible entries. Missing records are not guaranteed to be missing at random. The sample lacks verified competitive-tier labels, complete version information, and context from immediately before decisions. Individual real records and precise timestamps are not included in this public repository.

## Learning and performance evaluation

For any future authorized research, assign all views, participants, stages, units, and card summaries of the same match to one dataset split. Then use time groups supported by evidence. Quarantine unknown or conflicting times. Fit statistical transformations only on training data. A holdout used for exploration must no longer be described as a blind evaluation set.

Final placement, final lineups, future stages, resources observed after an action, and post-match opponent boards that were not scouted must not enter features for the corresponding decision. Surviving longer can affect both final level and outcome, so final-state associations are not causal evidence for an upgrade policy.

This release checks structure, cleaning boundaries, and synthetic examples. It does not train a model or score strategy effectiveness. Do not fill unknowns with zero, invent actions, or infer missing prices.
