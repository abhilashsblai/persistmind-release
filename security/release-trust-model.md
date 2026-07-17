# Release Trust Model

## Trust inputs

A PersistMind release is identified by:

- product and version;
- release channel and runtime profile;
- exact source commit and build timestamp;
- artifact filename, byte size, and SHA-256;
- manifest identity and checksum;
- signature status; and
- qualification evidence for the installed artifact.

No single filename, Drive link, Git tag, or README statement is sufficient.

## Current private preview

`0.2.1.dev17` is checksum-verified but unsigned. It is distributed only to
approved testers and is not trusted by the automatic updater. GitHub publishes
the direct Drive link and immutable identity metadata, but hosts no artifact.

## Future signed channels

Public Beta, Stable, and LTS require an authenticated signature over immutable
release metadata plus byte-level checksum verification. The verification key
may be distributed; the private signing key must remain isolated and must never
be copied into source control, CI logs, support reports, or release packages.

## Authority boundary

Release trust cannot enable runtime authority that the qualified profile
disables. The current profile keeps MCP read-only, remote writes disabled, and
autonomous source modification unavailable.
