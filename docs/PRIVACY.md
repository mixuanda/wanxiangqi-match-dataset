# Privacy and Release Requirements

This release publishes zero real records. Real-record publication remains disabled. Only hand-authored synthetic examples are accepted by the public validator.

## Two allowlists

1. `validation.FIELDS` and the JSON Schema define the fields at every level. Cleaning rebuilds records and local relationship keys without copying unknown fields, identity keys, timestamps, URLs, raw payloads, or arbitrary notes. Private output cannot pass public validation directly.
2. `PUBLISH_FILES.json` defines the release inventory. The scanner checks the working tree, every reachable Git history blob, filenames, and commit text. It rejects unapproved files, binary files, archives, databases, symlinks, and oversized files. Sensitive content deleted from the current tree still fails the history check.

Text checks look for patterns such as long numeric identifiers, precise timestamps, user-directory paths, some credentials, and source pseudonyms. They are not a complete personal-information detector and do not prove anonymity. Origin labels and `toy-` names do not independently prove synthetic provenance either.

## Hashed identity can still be identifiable

Rare lineups, continuous stage trajectories, precise match times, outcomes, and linkable match details can be combined to identify a player. Repeatable hashes can increase linkability across tables and releases. Hashing an account ID is not sufficient, and removing fields does not grant redistribution rights.

## Release review

- Use a separate directory and new Git history without inheriting private repository history or author contact information.
- Review every file, test, example, document, and license. Do not include source archives, real-record excerpts, profile links, avatars, or screenshots.
- Run structural and privacy rejection tests and scan the full reachable history. After publication, compare the remote file inventory with the reviewed local version.
- Keep private paths, credentials, request logs, and private engineering handoff material out of audit reports.

Before any future real-data release, separately review permitted source use and redistribution, necessity, re-identification risk, aggregation and suppression, deletion and correction procedures, and responsibility for the release. Until those conditions are met, do not publish real records or accept unreviewed data pull requests.
