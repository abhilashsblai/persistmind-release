# Windows Guide

## Safe preparation

- Use Windows 11 for the directly qualified environment.
- Use Python 3.13 and Git for the currently qualified path.
- Work on a disposable copy with a clean Git commit.
- Avoid credentials and sensitive repositories.
- Verify `SHA256SUMS.txt` before installation.

## Paths and permissions

PersistMind qualification covered spaces and Unicode in repository paths.
Long paths, antivirus locks, read-only files, SQLite locks, and interrupted I/O
can still produce host-specific failures. Use a user-writable local path, avoid
network shares for preview testing, and never disable security software merely
to make a test pass.

## Recovery

Before mutation testing, create a Git commit and a verified PersistMind backup.
Restore only into an empty location, reopen and verify the restored state, then
decide whether a controlled replacement is necessary. Do not manually delete
live database sidecars while a process may be running.

See [installation](../docs/windows-installation.md) and
[troubleshooting](../docs/troubleshooting.md).
