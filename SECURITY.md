# Security Policy

## Supported versions

Only the version identified in [releases/current.md](releases/current.md) is
current. An Internal Preview has no production security-fix or response-time
SLA. Historical tags are unsupported.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when available. If it is unavailable,
contact the repository owner through the maintainer's GitHub profile before
sending sensitive details. Do not publish an unpatched vulnerability,
credentials, tokens, private source, database content, or signing material in a
public issue.

Include the PersistMind version, source commit, artifact SHA-256, operating
system, Python version, affected command, impact, and a minimal redacted
reproduction.

## Release integrity

The private release channel binds version, source commit, filename, byte size,
SHA-256, manifest, runtime profile, and qualification evidence. Checksums detect
byte mismatch but do not authenticate an unsigned publisher. Future public and
stable channels require signature verification.

Private signing keys must never be shared, committed, attached to an issue,
included in a release bundle, or copied into qualification evidence.

See:

- [Release trust model](security/release-trust-model.md)
- [Checksum verification](security/checksum-verification.md)
- [Signature verification](security/signature-verification.md)
- [Vulnerability reporting](security/vulnerability-reporting.md)
