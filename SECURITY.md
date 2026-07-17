# Security Policy

## Supported release

Only the release identified in [releases/current.md](releases/current.md) is
current. Its maturity, supported platforms, and security limitations are stated
in that file. An internal preview does not carry a production security SLA.

## Reporting a vulnerability

Use GitHub private vulnerability reporting for this repository when available.
If it is unavailable, contact the repository owner through the maintainer's
GitHub profile before sending sensitive details. Do not publish an unpatched
vulnerability, credentials, private repository content, or signing material in
a public issue.

Include the PersistMind version, source commit, artifact SHA-256, operating
system, Python version, affected command, impact, and minimal reproduction.
Redact tokens, credentials, user names, absolute private paths, source content,
database contents, and logs unrelated to the failure.

## Release trust

PersistMind release bytes are distributed through version-specific Google
Drive folders. GitHub contains documentation and metadata only. Verify SHA-256
before installation. A release is trusted by the production updater only when
its manifest and artifact satisfy the signed-channel policy; checksum-only
internal previews are not trusted updater inputs.

See [docs/security-model.md](docs/security-model.md) for the threat model and
[docs/release-qualification.md](docs/release-qualification.md) for publication
gates.
