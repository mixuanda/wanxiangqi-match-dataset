# Release Audit

This release contains 20 allowlisted files: original code, documentation, a machine-readable schema, and synthetic examples. It publishes zero real records. It includes no database, source archive, compressed data bundle, image, request log, or personal-information file, and does not inherit another project's history.

The release checks cover:

- 14 passing tests for field cleaning, unknown values, level/star separation, card-summary semantics, rejection of real-record publication, rejection of unknown nested fields, and detection of removed sensitive content in Git history and unapproved archives.
- Successful public-schema validation of the hand-authored synthetic example.
- A passing release inventory and text-pattern scan, including every reachable Git commit and blob. Release commits use a separate, generic contributor identity.
- Manual review of every file: no copied real records, player nicknames, personal avatars, profile links, traceable match details, internal paths, credentials, or private engineering material.

Reproduce the checks:

```bash
python -B -m unittest discover -s tests -v
python -B -m wxqdata validate examples/synthetic.json
python -B -m wxqdata scan . --history
```

Any added file requires an allowlist update and a fresh review. Adding a path to the allowlist is not itself approval. Pattern scans cannot establish that every privacy risk has been detected or that third-party data may be reused. Real-record publication therefore remains disabled, pending source-rights and re-identification reviews.
