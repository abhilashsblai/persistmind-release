# Current PersistMind Release

> [!IMPORTANT]
> This is a private internal-preview record, not a public download page. Approved
> testers receive Drive access separately.

## Release identity

- Version: `0.2.1.dev4`
- Release type: Internal Windows Preview
- Commit SHA: `af93e56e54350d82ae0d40a8bdcce71dd0ac7c03`
- Build timestamp: `2026-07-17T01:35:43.627027Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution channel: Private Google Drive
- Production: No
- Public beta: No

## Supported systems

| Requirement | Current status |
| --- | --- |
| Windows 11 | Qualified |
| Windows 10 | Intended internal-preview target; qualification pending |
| Linux | Qualification pending; installation not published |
| macOS | Qualification pending; installation not published |
| Python | 3.11, 3.12, and 3.13 passed on Windows 11 |
| Git | Required for repository workflows |

## Download and access

- Artifact folder: Version-specific private PersistMind Release Drive folder
- Access: Approved internal-preview testers only
- Public artifact URL: Not published
- GitHub release assets: Not an active distribution channel

Approved testers must obtain the folder through the designated private-access
process and verify every value below before installation.

## Artifact verification

- Wheel filename: `persistmind-0.2.1.dev4-py3-none-any.whl`
- Wheel size: `1303153` bytes
- Wheel SHA-256: `e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad`
- Source distribution: `persistmind-0.2.1.dev4.tar.gz`
- Source distribution SHA-256: `1375c3b705bad562b9fc1301125d4f910b6e8757edbd11fba32082703f8ff7dc`
- Packaged ZIP: `PersistMind-Windows-Internal-Preview-0.2.1.dev4.zip`
- ZIP SHA-256: `fbf8324921182d551c6e28a095ebb366ede9c63bca87961f7ff2ec27f81e2123`
- Manifest: `internal-preview-manifest.json`
- Manifest SHA-256: `1a714d9b4415a4277c3ca5b2d3b97f6efe2c0aba30c1a16a2613401f779e870c`
- Signature status: Unsigned internal preview
- Trusted updater status: Ineligible

See [artifact verification](../docs/artifact-verification.md).

## Qualification

| Gate | Result |
| --- | --- |
| Full source suite | 1,168 tests; 0 failures; 0 errors; 7 skipped |
| Windows 10 | Qualification pending |
| Windows 11 | Passed |
| Python 3.11 | Installed-wheel smoke passed |
| Python 3.12 | Installed-wheel smoke passed |
| Python 3.13 | Installed-wheel smoke passed |
| Installed-wheel identity | Passed |
| Backup and restore | Passed |
| Read-only MCP boundary | Passed |
| Uninstall/source preservation | Passed |

## Restrictions

- Non-critical or disposable local repositories only
- Manual human review required
- No production use
- No public beta claim
- No remote writes or team service
- No writable MCP
- No autonomous source modification
- No automatic self-improvement adoption
- No trusted automatic updates

## Known issues

- Windows 10 has not yet produced a machine qualification result.
- Linux and macOS qualification is pending.
- The artifact is unsigned and may trigger host download warnings.
- There is no production, enterprise, compatibility, or response-time SLA.

Read the [release notes](release-notes/0.2.1.dev4.md) and
[known issues](../docs/known-issues.md).
