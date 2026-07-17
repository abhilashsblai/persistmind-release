# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal preview, not a public-beta or production
> download. Use it only for non-critical local repositories with manual review.

## Release identity

- Version: `0.2.1.dev17`
- Release type: Internal Windows Preview
- Source commit: [`14ff2cc1af4ce0fc72a786756d1e9e37ac105648`](https://github.com/abhilashsblai/PersistMind/commit/14ff2cc1af4ce0fc72a786756d1e9e37ac105648)
- Build timestamp: `2026-07-17T10:40:45.798752Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution: [Google Drive release folder](https://drive.google.com/drive/folders/160qS1SAmgByBDnGoVwsnc1hVOCzorN6c)
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1VlU4tRxs0wudWkba6oYdVcjSG66gvosF/view?usp=drivesdk)**
- [Checksum-verifying installer](https://drive.google.com/file/d/1d5gmp0kqsxW7Zsu0LIU0HTAy1Ts76AmQ/view?usp=drivesdk)
- [Wheel](https://drive.google.com/file/d/1-k1Gzl77EAsL8CfH95t6hPiiH2xT33pW/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1s4cFBUgEg3UVt2_-8jac2jeVvs3yfoDU/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1XgOc5oENlSlEm68TsZ--4lI8qgXnbDLs/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1BfFYk2Kw-yzJKbdWkgGoRKipsXF8Xnwq/view?usp=drivesdk)

The ZIP is the recommended download because it keeps the installer, wheel,
manifest, checksums, and documentation together. GitHub contains no release
binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev17.zip` | 2,857,933 bytes | `fc5c537a4a1ccee52d936f918c6c62b4023ac0d1741247d2c1e0322d056e22f9` |
| `persistmind-0.2.1.dev17-py3-none-any.whl` | 1,320,209 bytes | `9a95d55d26758c9d02ee338e35b5b29d8dddcc79e0430f498c9e08d02e900c02` |
| `persistmind-0.2.1.dev17.tar.gz` | 1,567,710 bytes | `464cdc053249a89fde6b0d8161bb736faf3a0fd2efbe028a844c052f1de1cbe7` |
| `internal-preview-manifest.json` | 1,723 bytes | `fac2e8bed7823c2b22aa7746257946e02bd2e8d445a576355a36bb7f3f62563d` |
| `Install-PersistMind.ps1` | 2,478 bytes | `ef40de185db5b14e3de2bb3d7536336303d36c6b68098d974d23f317a02b6a4f` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

## What changed

- `workflow next` self-heals manual lifecycle tasks that have an accepted plan
  but no stored workflow recommendation.
- The recovered recommendation is derived from split-v1 task, pack, plan,
  capability, path, and impact evidence and is persisted once.
- `workflow brief` is no longer needed to refresh these tasks.
- Repository identity reads Git patch output as bytes and safely handles legacy
  Windows-1252 content without changing normal UTF-8 identity behavior.
- Split-v1 Codex preflight, plans, and packs now share one authoritative Task and
  Activity path.
- Plan validation rejects missing, foreign, legacy, or incorrectly bound pack IDs.
- CLI and MCP pack generation honor diff-derived seed paths.
- Diff verification preserves the real incomplete status instead of converting
  it to `internal_error`.

## Qualification

The exact wheel built from the recorded commit passed an isolated Windows
11/Python 3.12 installation and a disposable-repository lifecycle covering
setup, all seven split databases, indexing, search, deterministic context packs,
task/plan/checkpoint/verification/outcome flow, scope rejection, approved memory,
read-only MCP, backup/restore, restart, and uninstall source preservation.

Real-project behavior remains an explicit tester-feedback gate. Windows 10,
Python 3.11/3.13, Linux, macOS, signing, and production updater qualification are
still pending.

Read the [release notes](release-notes/0.2.1.dev17.md),
[artifact verification guide](../docs/artifact-verification.md), and
[known issues](../docs/known-issues.md).
