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

The expanded private structural review covers 671 full details reached through one source profile, plus 147 candidates with list summaries only. This is not a random sample across competitive tiers. Successfully retrieved details favor the accessible portion of the retained history; missingness is not assumed random. The sample lacks verified competitive-tier labels, complete version information, and context from immediately before decisions. Individual real records and precise timestamps are not included in this public repository.

## Availability, time, and refusal evidence

- Full details and list-only summaries are different information layers. A list lineup or placement must not be expanded into invented participants, rounds, or action sequences. The 67,149 stage records belong only to the 671 full details.
- One retained request returned business code `-130`, with a message that the record was older than 30 days **or** the mode did not support details. That response establishes one observed refusal, not 147 observed refusals or a universal rule for every older record.
- Another 146 candidates were not retried after that stop. They retain earlier rate-limit outcomes; "not retried after the stop" does not mean "never requested."
- Interpreting the retained `endTime` values as Unix seconds, all 147 summary-only cases are older than 30 days at the retained stop reference. This offline age check does not establish the cause of every missing detail or predict that every request would be refused. Original display-time timezones remain unverified.
- No server unlock time is known. A local traffic-spacing timestamp is not an eligibility signal or permission to retry. The offline import and public documentation update do not send collection requests or bypass the service restriction.

The prior 476-match snapshot remains preserved separately. The expanded version was checked for composite-key uniqueness, overlap, source hashes, and agreement between list summaries and full details. These checks do not establish global match identity across different source profiles.

## Learning and performance evaluation

For any future authorized research, assign all views, participants, stages, units, and card summaries of the same match to one dataset split. Then use time groups supported by evidence. Quarantine unknown or conflicting times. Fit statistical transformations only on training data. A holdout used for exploration must no longer be described as a blind evaluation set.

Final placement, final lineups, future stages, resources observed after an action, and post-match opponent boards that were not scouted must not enter features for the corresponding decision. Surviving longer can affect both final level and outcome, so final-state associations are not causal evidence for an upgrade policy.

This release checks structure, cleaning boundaries, and synthetic examples. It does not train a model or score strategy effectiveness. Do not fill unknowns with zero, invent actions, or infer missing prices.
