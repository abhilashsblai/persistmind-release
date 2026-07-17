# Updater

## Current release

The automatic updater is not an installation path for `0.2.1.dev15`. This
internal preview is checksum-verified but not signed with the official release
key. Install it manually from its version-specific Drive folder.

## Trusted-channel design

A trusted update must bind one immutable artifact to its product, version,
source commit, channel, size, SHA-256, Python compatibility, and signed
manifest. The updater must verify those values before staging a candidate and
must preserve rollback data until post-install verification succeeds.

GitHub is not a binary fallback. Update bytes belong in Google Drive and must
match the signed release metadata. A checksum alone detects accidental or
unkeyed byte changes; it does not provide publisher authentication.

## Rollback expectations

A qualified updater should stage an immutable engine slot, back up affected
state, perform a bounded cutover, run installed-package verification, and roll
back on failure. These expectations describe a future signed channel and do not
promote the current internal preview.
