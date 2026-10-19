# Current Coverage and Availability

| Item | Current status |
|---|---|
| Cached candidates in the selected-character cohort | 818, reached through a single source profile |
| Full match details reviewed privately | 671 |
| Preserved earlier full-detail baseline | 476; the expanded version adds 195 details |
| Participant observations in full details | 4,026; not 4,026 independently sampled players |
| Stage records in full details | 67,149; includes auction phases, not only combat rounds |
| Auction snapshots in full details | 11,824 |
| Final unit observations in full details | 25,754 |
| Candidates with list summaries only | 147; no full stage trajectories are invented |
| Full-detail share of this cached candidate list | 671/818, or 82.0% |
| Real records published here | 0 |
| Published examples | Hand-authored synthetic data; unsuitable for evaluating gameplay strategies |
| High-tier representation | Unverified; final match placement is not competitive tier |
| Coverage across all characters, modes, and patches | Not established |
| Decision-time shop offers, prices, hand contents, and input acknowledgements | Incomplete |

These figures describe private structural review and the availability of one retained candidate cohort. They are not the number of publicly released records or coverage across the platform or player population. Successful detail retrieval is not a player win rate.

## Availability layers

| Retained evidence | Cases | Interpretation |
|---|---:|---|
| Full details retained | 671 | Includes participants and stage snapshots |
| Observed terminal refusal | 1 | One request returned code `-130`: older than 30 days or details unsupported for that mode |
| Not retried after that stop | 146 | List summaries remain; retained earlier outcomes were rate-limit failures |

Do not describe all 147 summary-only cases as individually rejected by the terminal response. The other 146 were not retried after the stop, which does not mean they had never been attempted. No server unlock time was specified. A local spacing timer does not resolve the retention-or-mode response or authorize another attempt.

## Separate modes and time availability

| Source mode identifier | Full details | List-only cases | Cached candidates |
|---|---:|---:|---:|
| `2` | 652 | 147 | 799 |
| `4` | 19 | 0 | 19 |

These are source-mode identifiers within this cohort, not evidence of comprehensive coverage of either mode. Their game rules and resource scales must not be pooled without validation.

Interpreting retained `endTime` values as Unix seconds, the 671 full-detail cases are within 30 days at the retained stop reference, while all 147 list-only cases are older than 30 days. This is an offline timestamp calculation. It does not prove that age alone caused each missing detail, that a strict cutoff applies universally, or that every older request would fail. Source display-time timezones are still unverified, and no precise match timestamps are published here.

The availability pattern creates age and access selection bias. Summary-only lineups can support separate, appropriately limited descriptive work; they cannot be counted as full trajectories or used to fabricate action labels. Source-use and redistribution conditions remain unresolved for real-record release. The open-source code license does not change those conditions.
