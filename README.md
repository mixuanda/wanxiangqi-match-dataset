# Wanxiangqi Match Data Research (王者万象棋)

Research on match data schemas, quality, privacy, and reproducible analysis. Our long-term goal is to expand coverage of public matches from high competitive tiers, subject to source permissions and privacy review.

**This release contains only original documentation, offline cleaning and validation code, and entirely synthetic examples. It publishes zero real match records.** This is an independent research project, not an official product or a dataset with comprehensive high-tier coverage.

## What has been reviewed

A retained local sample has undergone private structural checks: 476 matches, 2,856 participant observations, and 47,586 stage records. The sample comes through a single source profile. The six participants in a match and repeated stages of the same participant are dependent observations. Final placement within a match is not a player's competitive tier; this sample does not establish high-tier representation.

Real records, source archives, player identifiers, nicknames, avatars, profile links, traceable match identifiers, precise timestamps, request logs, and credentials are not included. Real records remain private while source-use and redistribution conditions are unresolved. Removing or hashing account identifiers does not make a match trajectory anonymous.

## Run locally

The tools use only the Python standard library. They do not make network requests or collect data.

```bash
python -B -m unittest discover -s tests -v
python -B -m wxqdata validate examples/synthetic.json
python -B -m wxqdata scan . --history
```

The cleaner accepts the generic research draft defined by this project. **It is not a parser for a particular platform's API.** Prepare an input using the field dictionary, then write the cleaned draft to a private directory:

```bash
python -B -m wxqdata clean draft.json .private/cleaned.json
python -B -m wxqdata validate .private/cleaned.json --private
```

The cleaner rebuilds records from a field allowlist and creates local relationship keys. It does not copy source identity keys or timestamps. Its output is always marked `private_research` and is rejected by the public validator. Cleaning does not grant permission to publish or eliminate the possibility of identifying a match trajectory. The release scanner intentionally rejects unapproved files in the repository working tree, including private drafts. Process real data in a separate working directory.

## Synthetic example

`examples/synthetic.json` is hand-authored fiction. Its `toy-` labels do not identify real players, matches, game characters, or items, and its numbers do not describe actual gameplay. It illustrates a combat snapshot, an auction snapshot, card-count summaries, and explicit unknown values. For example, `board: null` means unknown, while an empty array means observed to be empty. The example is not suitable for measuring strategy performance.

## Documentation

- [Field dictionary](docs/FIELD_DICTIONARY.md): final lineups, stage snapshots, card summaries, and unknown fields.
- [Data quality](docs/QUALITY.md): modes, versions, time, missingness, deduplication, and training leakage.
- [Privacy and release requirements](docs/PRIVACY.md): field and file allowlists, complete reachable Git history checks, and the block on real-record publication.
- [Coverage](docs/COVERAGE.md): the scope and limitations of the current sample.
- [Roadmap](docs/ROADMAP.md): prerequisites for expanding coverage of public matches from high competitive tiers.
- [Data rights and license scope](docs/RIGHTS.md) and the [release audit](AUDIT.md).

Research can start with stage lineup frequencies by mode, paired snapshot comparisons, and level distributions. Snapshot differences do not reveal purchase or sale actions. An association between final placement and higher levels does not show that a strategy improves win rates. This release provides no model, automated gameplay tool, or claim of improved performance.

## Contributing

Contributions to field contracts, quality checks, synthetic cases, and research methods are welcome. Do not submit real account information, match links, logs, credentials, or unreviewed records in issues, pull requests, attachments, or screenshots. Any future release of real data requires a separate review of source rights and re-identification risk.

Original code, documentation, and hand-authored synthetic examples are licensed under [MIT](LICENSE). This license does not grant rights to game assets, platform content, or unpublished third-party match records.
