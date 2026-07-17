# Security Model

## Assets

PersistMind protects repository source, local indexes, memory, policy records,
workflow evidence, audit history, backups, release artifacts, and signing trust.

## Current trust boundary

The internal Windows preview operates on local repositories and local
filesystem state. It requires manual human review, keeps MCP read-only, rejects
remote writes and non-loopback authority expansion, and does not permit
automatic self-improvement adoption.

## Release integrity

- SHA-256 binds documentation to exact artifact bytes.
- Version, source commit, profile, channel, and signing status are embedded in
  runtime identity.
- Version-specific Drive folders prevent a moving "latest" link from becoming
  release authority.
- The current preview is explicitly unsigned and excluded from the trusted
  production updater.
- Future public/stable channels require authenticated signatures in addition to
  checksums.

## Data handling

Keep sensitive repositories out of preview testing. Evidence and support reports
must redact credentials, tokens, signing material, private source, absolute
private paths, and database content. Memory is data, not authority; approval and
policy checks remain separate.

## Out of scope

The current release does not claim hardened remote authorization, multi-user
isolation, enterprise deployment, organizational connectors, or production
incident response.
