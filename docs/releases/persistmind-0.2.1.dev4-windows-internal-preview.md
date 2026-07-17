# PersistMind 0.2.1.dev4 - Internal Windows Preview

Released July 17, 2026 for restricted private testing.

This is an unsigned Windows-only internal preview for disposable or
non-critical local repositories. It requires manual human review. It is not a
public beta, production release, or trusted automatic-update artifact.

## Downloads

All release bytes are stored exclusively in the designated Google Drive
location:

- [Complete internal preview folder](https://drive.google.com/drive/folders/1HT9bAsR4S9D1bmJ8MtaX9GiweuHK77U1)
- [Packaged ZIP](https://drive.google.com/file/d/1Si6ETnyg5F66gFSgw_nUkhhh_-7-vKWY/view)
- [Python wheel](https://drive.google.com/file/d/1w0FkMNt3gTQ3d6oM-DMeKt6knyLzyNun/view)
- [SHA256SUMS.txt](https://drive.google.com/file/d/1QeKqS7iEQZk8eRJjzzjqgzkuj3K7je1e/view)
- [Windows installation instructions](https://drive.google.com/file/d/1CDpY7GIAZRpYnsxNrwAKa3BH-1mlh20O/view)

No installer, wheel, source distribution, or ZIP is attached to GitHub.

## Identity and integrity

- Version: `0.2.1.dev4`
- Runtime profile: `windows-internal-preview`
- Source commit: [`af93e56e54350d82ae0d40a8bdcce71dd0ac7c03`](https://github.com/abhilashsblai/PersistMind/commit/af93e56e54350d82ae0d40a8bdcce71dd0ac7c03)
- Wheel SHA-256: `e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad`
- Source distribution SHA-256: `1375c3b705bad562b9fc1301125d4f910b6e8757edbd11fba32082703f8ff7dc`
- ZIP SHA-256: `fbf8324921182d551c6e28a095ebb366ede9c63bca87961f7ff2ec27f81e2123`
- Officially signed: No

Verify the downloaded artifact against `SHA256SUMS.txt` before installation.

## Qualification

The full source suite passed on the frozen commit. The exact same built wheel
was installed outside the source checkout and passed the complete Windows smoke
scenario on Python 3.11, 3.12, and 3.13. The scenario covered identity and
profile enforcement, repository indexing and changes, search, deterministic
context packs, workflow and scope controls, memory, read-only MCP policy,
storage integrity, backup/restore, and uninstall/source preservation.

- Windows 11: passed
- Windows 10: not directly observed in this qualification run
- Python 3.11: passed
- Python 3.12: passed
- Python 3.13: passed
- Linux and macOS: not qualified and not supported by this preview

## Restricted boundary

Use only with local files and local Git repositories that are disposable or
non-critical. Create a commit or backup first and manually review every change.

The profile keeps deferred/labs capabilities disabled, MCP read-only, remote
writes disabled, autonomous source modification disabled, and unsigned bytes
outside the trusted production updater. Production-authoritative CIE,
anticipation, automatic self-improvement adoption, team/server operation,
organizational connectors, and cross-repository authority are unsupported.

Do not use this preview on production branches, security-sensitive or
regulated repositories, repositories containing credentials, Linux, or macOS.

## Trust statement

The production updater and signature verification were not modified or
bypassed. The official signing key was not requested, copied, or exposed. The
formal beta Drive folders were not touched.
