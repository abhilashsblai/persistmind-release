# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal preview, not a public-beta or production
> download. Use it only for non-critical local repositories with manual review.

## Release identity

- Version: `0.2.1.dev18`
- Release type: Internal Windows Preview
- Source commit: [`60924ed94d1d7bcf965bf729ccef947936fd5995`](https://github.com/abhilashsblai/PersistMind/commit/60924ed94d1d7bcf965bf729ccef947936fd5995)
- Build timestamp: `2026-07-17T11:16:15.112007Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution: [Google Drive release folder](https://drive.google.com/drive/folders/1MhEEibPxLZMs6HgIUJVaUNpgJ7NWgch1)
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1rR0O7woaS7hs8nqrpYK-8NOUIEVtJM_q/view?usp=drivesdk)**
- [Checksum-verifying installer](https://drive.google.com/file/d/1ixaWuOj0XpQC4UPnhEBwa1ob4Sr4m84k/view?usp=drivesdk)
- [Wheel](https://drive.google.com/file/d/1yoGAfMg6OzXqHeHOWB5UOwWu_es83fCr/view?usp=drivesdk)
- [Source distribution](https://drive.google.com/file/d/1iryCDChwQu3HE30yCwQaMA9GX7KmjaRb/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1v5dxO3yb6Mx9kz4bJ-xnaOP56T7ozrFs/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/166Nw28khfQrTOeIGQ-FLfk2EBugGmaT7/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1Lt-dmT3kP7iPIlivM5sM_HKsPqztFLVH/view?usp=drivesdk)

The ZIP is the recommended download because it keeps the installer, wheel,
manifest, checksums, and documentation together. GitHub contains no release
binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev18.zip` | 2,860,708 bytes | `738520945882ce43cebbefebbcbc1d9614df1f8a25f4c5ab7c733e70dd263f22` |
| `persistmind-0.2.1.dev18-py3-none-any.whl` | 1,321,058 bytes | `6963ee88abf2ddb90898c11ac07718e6ebce06b98edba5a70424a8c0933d8dce` |
| `persistmind-0.2.1.dev18.tar.gz` | 1,569,604 bytes | `5d56a0ade92755b2079f481adb4da53810e5074f8842db18c39edba8e990b7d9` |
| `internal-preview-manifest.json` | 1,723 bytes | `6e04acbf9bc8493f3e1c8f810d0b84ff8c7a0836fc4bab0f4618065da5a06c7b` |
| `Install-PersistMind.ps1` | 2,478 bytes | `71a80bae61160c2b2fc49c0c92250e25b3b658fa4e7527018f17ac958710dd0d` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

## What changed

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

Read the [release notes](release-notes/0.2.1.dev18.md),
[artifact verification guide](../docs/artifact-verification.md), and
[known issues](../docs/known-issues.md).
