# Coverage and Research Roadmap

The long-term goal is to expand coverage of public matches from high competitive tiers, where permissions and privacy safeguards allow it. We cannot promise to obtain every match, and a sample from one source profile must not be presented as comprehensive high-tier coverage.

| Stage | Work | Requirements for moving forward |
|---|---|---|
| Current: methods and synthetic contracts | Field dictionary, allowlists, cleaner, rejection tests, quality notes, and privacy documentation | Reproducible code and synthetic examples; no real-record release |
| Source and access review | Identify permitted public sources, retain terms or authorization evidence, and verify definitions of competitive tiers and modes | Clear use and redistribution conditions; traceable provenance without disclosing private information |
| Coverage audit | Track candidates, successes, failures, and deduplication by competitive tier, time bucket, mode, and version | Explicit denominators, unknowns, and access gaps |
| Expand authorized samples | Gradually include more source players within permitted access and verify match identity across views | No bypassing authentication, access limits, anti-cheat systems, or platform protections; do not use nicknames as identity |
| Aggregate research | Analyze modes separately, stage lineups, level trajectories, and sensitivity to missingness | Explain aggregation thresholds and re-identification risks; exclude decision leakage |
| Independent release review | Confirm rights, necessity, minimization, and deletion/correction procedures | A separate release decision; otherwise continue publishing only methods and synthetic examples |

Access governance must respect source permissions and rate limits. When access is restricted, use backoff, conservative cooldowns, and stop conditions; do not bypass blocks or retry indefinitely. Future collection requires explicit authorization, a single collection coordinator, and auditable request budgets. This repository implements no online collector, background polling, or scheduled task.

Strategy research needs additional context from the time of each decision. More matches do not automatically supply shop alternatives, action costs, hand contents, or click acknowledgements. Any later performance evaluation should define its comparison and use independent samples; descriptive frequencies are not evidence of an improved win rate.
