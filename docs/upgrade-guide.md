# Upgrade Guide

## Internal preview policy

There is no supported automatic upgrade path into or out of `0.2.1.dev19`.
Treat each internal preview as a separate evaluation installation.

Before testing a newer build:

1. Commit or back up repository source.
2. Create and verify a PersistMind storage backup.
3. Preserve the old wheel, manifest, checksums, and evidence.
4. Create a new isolated virtual environment.
5. Verify and install the new wheel manually.
6. Run identity, doctor, storage verification, indexing, search, pack, workflow,
   backup/restore, and uninstall smoke against a disposable copy.

Do not point the trusted updater at an unsigned preview. A future `0.2.x` to
`0.3.x` migration guide will be published only after the target storage and
compatibility contracts are frozen and qualified.
