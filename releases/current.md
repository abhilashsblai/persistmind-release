# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal preview, not a public-beta or production
> download. Use it only for non-critical local repositories with manual review.

## Release identity

- Version: `0.2.1.dev19`
- Release type: Internal Windows Preview
- Source commit: [`8e0e67aefa0ec5cafe80ac5b180a0708cacfc3a4`](https://github.com/abhilashsblai/PersistMind/commit/8e0e67aefa0ec5cafe80ac5b180a0708cacfc3a4)
- Build timestamp: `2026-07-17T12:29:15.551152Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution: [Google Drive release folder](https://drive.google.com/drive/folders/1KUZKm3wyvy3HqJZBeqMzkQlkd5sRgY-5)
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1WiT3UrMXEb_T4FTbIxHzuwnU-gWHKPju/view?usp=drivesdk)**
- [Checksum-verifying installer](https://drive.google.com/file/d/1A7N_lbDDj539sB-wwhJV-jdnjRf8xYEW/view?usp=drivesdk)
- [Wheel](https://drive.google.com/file/d/1O1KZq-Na3GYZ2cHrE5_1-jK6HjIUG9wQ/view?usp=drivesdk)
- [Source distribution](https://drive.google.com/file/d/1w29kHAEqeXAD0AtsAuRmnm4Is9Gkqqpm/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1F2uLD7pZiLHgGJw_1_Q97inW9-fDCXE5/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1dVPqtYC4qR9vThXx2UvbTsIbwfEmbVK8/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1usK9HAYKXtEFjK4waW_2VgjFAInPqQXf/view?usp=drivesdk)

The ZIP is the recommended download because it keeps the installer, wheel,
manifest, checksums, and documentation together. GitHub contains no release
binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev19.zip` | 2,863,771 bytes | `e397e87e83453e9ffb94d650f0ee29d44db8690347ce071d81b54240e5cd15cf` |
| `persistmind-0.2.1.dev19-py3-none-any.whl` | 1,321,054 bytes | `c9a1d3e41236c3f86fdd9103337522fa2e41eaaf10e086bb94f4064f48f8abd3` |
| `persistmind-0.2.1.dev19.tar.gz` | 1,570,208 bytes | `287f04f4ebf4a13e9742aa212505eff1330c20e84efcf087748724e9a817f673` |
| `internal-preview-manifest.json` | 1,723 bytes | `61835ddb824edad9e3268287d1d8825e48ff45d37a6273574393677a3723c448` |
| `Install-PersistMind.ps1` | 2,923 bytes | `ecb366d43d613c24baf30919ea87ea11db098f9c1f6014692dbd7ef5f9b7521c` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

## What changed

- The extracted ZIP now contains `Install-PersistMind.ps1` and
  `INSTALL-WINDOWS.txt` at its root, matching the documented commands.
- The installer resolves a standalone adjacent wheel or the ZIP's
  `artifacts` wheel without manual path arguments.
- Packaging now executes the root installer with `-VerifyOnly` before creating
  the ZIP, preventing a structurally uninstallable archive from being published.
- Hook policy freshness is bound to the active task, pack, plan status, and plan
  revision instead of the entire task SQLite database/WAL image.
- Routine checkpoint, workflow, and telemetry writes no longer invalidate a
  successful preflight.
- Read-only `workflow brief` and `workflow next` calls cannot overwrite the last
  green preflight snapshot with a false readiness value.
- Source-generation changes, plan amendments, pack rebinding, trust changes,
  and snapshot expiry still fail closed.
- `workflow next` continues to self-heal manual lifecycle tasks that have an
  accepted plan but no stored workflow recommendation.
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

Read the [release notes](release-notes/0.2.1.dev19.md),
[artifact verification guide](../docs/artifact-verification.md), and
[known issues](../docs/known-issues.md).
