# Field Allowlist and Semantics

The machine-readable contract is `schemas/public-synthetic.schema.json`. The Python validator rejects unknown fields. No layer accepts arbitrary metadata, raw responses, free-text notes, or identity fields. Retained fields must be explicitly present. Unknown scalars use `null`; unknown boards, equipment lists, and summary lists also use `null`. Use an empty array only when a list was observed to be empty.

| Level | Allowed fields | Meaning |
|---|---|---|
| Dataset | schema_version, origin, matches | `origin` is `synthetic` or `private_research`; public validation accepts only `synthetic`. |
| Match | sample_key, mode, patch, participants | `sample_key` is local to the file. Source match IDs, timestamps, and links are excluded. Do not infer an unknown patch from a date. |
| Participant observation | actor_key, selected, final_rank, chess_player, final_board, stages | `actor_key` links observations within a match; it is not a player identity across matches. `final_rank` is final match placement, not competitive tier. |
| Stage snapshot | stage_index, phase, player_level, energy_left, hero_limit, board, card_summaries, auction | `stage_index` orders observed records; it does not guarantee consecutive game rounds. `phase` explicitly distinguishes combat, auction, and unknown snapshots. |
| Unit observation | unit, level, quality, star, equipment, position | Hero level, quality, and an explicitly reported star count are separate fields. Missing stars must not be derived from level or quality. |
| Card summary | kind, card, count | Acquisition, use, or removal counts; not purchases, refreshes, sales, or an input-action sequence. |
| Auction source summary | card, reported_cost_energy, reported_shared_energy | Only reported source values. These do not establish complete options, all bids, or a verified winner. |

The selected chess character (`chess_player`, 棋手) and a deployed hero (`unit`, 棋子) are different entity types, even when their names match. `player_level` refers only to the reported level of the chess character; a deployed hero's `level` is not a substitute. The mapping from `hero_limit` to UI capacity must be verified separately. It does not establish available hand or inventory space.

`energy_left` may describe the end of a stage. Do not assume it is the cash available before a decision. Preserve negative source values for review instead of silently clipping them to zero. Resource scales from different modes must not be pooled.

This version has no fields for individual action prices or timestamps, shop offers, hand contents, refresh counters, click acknowledgements, or strategy goals. These cannot be reconstructed from card summaries, final lineups, or final level-contribution aggregates.

Public synthetic keys and labels must use the `toy-` prefix. The patch remains `null`, and the numbers are invented. Changing a real record's origin to `synthetic` does not prove that it is synthetic; maintainers must still review its provenance.
