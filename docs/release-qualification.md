# Release Qualification

Every published release record must include:

- exact source commit SHA and clean-tree confirmation;
- product version, channel, runtime profile, and build timestamp;
- artifact filenames, byte sizes, and SHA-256 values;
- signature status and trusted-channel status;
- installed-artifact tests executed outside the source checkout;
- operating-system and Python combinations actually observed;
- source-test and installed-smoke summaries;
- storage integrity, backup/restore, updater/rollback status where applicable;
- known limitations, unsupported boundaries, and unresolved blockers;
- evidence bundle, installation instructions, and migration guidance; and
- the immutable version-specific Google Drive location.

## Qualification pipeline

```text
Freeze commit
  -> source tests
  -> clean build
  -> clean installed-package tests
  -> storage qualification
  -> updater and rollback qualification when in scope
  -> sign when required by channel
  -> publish to version-specific Drive folder
  -> install from published channel
  -> final smoke
```

A stage cannot borrow evidence from another commit or artifact. Changing release
code, qualification tooling, manifest schemas, or artifact bytes requires a new
version identity and a restarted pipeline.

The current evidence is summarized in [releases/current.md](../releases/current.md).
