# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal preview, not a public-beta or production
> download. Use it only for non-critical local repositories with manual review.

## Release identity

- Version: `0.2.1.dev16`
- Release type: Internal Windows Preview
- Source commit: [`d4666d0d25d3c3780cda21aef3cdb33065723993`](https://github.com/abhilashsblai/PersistMind/commit/d4666d0d25d3c3780cda21aef3cdb33065723993)
- Build timestamp: `2026-07-17T09:21:01.951548Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution: [Google Drive release folder](https://drive.google.com/drive/folders/1ph9uZt0_DjIZEGzdM14geH_SaOC9SanL)
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1hZY6mh-cxkEFF6GR617Kj4ncCWF7Sfym/view?usp=drivesdk)**
- [Checksum-verifying installer](https://drive.google.com/file/d/1lpbfEK0qT8kqzNnVVQroeGGbNdxxrHYL/view?usp=drivesdk)
- [Wheel](https://drive.google.com/file/d/1LPh_58gOfb3poZRYBVaGKy3stq853zpn/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1k8izgXDoX2yK1IshJAcPqE9Q-RVRSs0z/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1FmHiMr8dwHLDHo1A4qdwO9AqL2GBoutp/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1pplh2TJwvjJ9qFSPqLxRy4oW3NHJ9qTo/view?usp=drivesdk)

The ZIP is the recommended download because it keeps the installer, wheel,
manifest, checksums, and documentation together. GitHub contains no release
binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev16.zip` | 2,857,095 bytes | `8d3cd96d018d5cb145254949eeefa6190f3d6bec8a7343e3e72b028a4296b295` |
| `persistmind-0.2.1.dev16-py3-none-any.whl` | 1,319,803 bytes | `52a088a8938e5b94021487abf3d303c218b2b147b151b779c5a88727739264a3` |
| `persistmind-0.2.1.dev16.tar.gz` | 1,567,258 bytes | `cb17b4f899640bbb5febadea13ac4c31ae245d0cad20b1c8e582f8a7ee749c31` |
| `internal-preview-manifest.json` | 1,723 bytes | `4e9bbceaf8278e9ce9971e255aab556656114b747c58fdd7f9e7879c9cb64053` |
| `Install-PersistMind.ps1` | 2,478 bytes | `7e116e6290c8b94831b0916ea305f0597232578a586ad0bcc75bf36b31f6015b` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

## What changed

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

Read the [release notes](release-notes/0.2.1.dev16.md),
[artifact verification guide](../docs/artifact-verification.md), and
[known issues](../docs/known-issues.md).
