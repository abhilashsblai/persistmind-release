# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal-preview record, not a public-beta or
> production download page. Access to the Drive files may require approval.

## Newer dev41 candidate

`0.2.1.dev41` is now available in the private Drive channel as a
**qualification-blocked internal candidate**. It is newer than this qualified
release, but it does not replace `0.2.1.dev31` as the recommended preview.

- [Dev41 candidate ZIP](https://drive.google.com/file/d/16trZ7KnP6cLPlJva08YXToWy4Z_l3isf/view?usp=drivesdk)
- [Dev41 Drive folder](https://drive.google.com/drive/folders/158iM5dE7ruqFRP3Fs_fSPeKoIiaFZW8H)
- [Dev41 release record](release-notes/0.2.1.dev41.md)

The exact dev41 wheel passed isolated offline installation and package/resource
identity checks. Full APSW-backed workflow qualification is blocked on the
release host by Windows Application Control, and the source tag contains stale
legacy regression expectations. Use dev41 only for targeted investigation on a
disposable repository; stop if installation or `doctor` reports a degraded
runtime.

## Release identity

- Version: `0.2.1.dev31`
- Release type: Internal Windows Preview
- Source commit: [`2a468449f79272b5d8e8aac15fc9c91a8a42e4a6`](https://github.com/abhilashsblai/PersistMind/commit/2a468449f79272b5d8e8aac15fc9c91a8a42e4a6)
- Build timestamp: `2026-07-19T15:04:09.547278Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution channel: designated Google Drive release channel
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1oCQN8stUdmeHvUQsO7tk-kKUqdd65A8s/view?usp=drivesdk)**
- [Version-specific Drive folder](https://drive.google.com/drive/folders/16ecYOlq4AZghwj7xPWkhxnUiyk7_8Y3y)
- [Wheel](https://drive.google.com/file/d/1e-oXJW5C2h3M1iRwwQLE4Kib_jUUT0k0/view?usp=drivesdk)
- [Source distribution](https://drive.google.com/file/d/1E1R5Pq4bbObvJm0TPACSPslB1m464k2x/view?usp=drivesdk)
- [Checksum-verifying installer](https://drive.google.com/file/d/1jyYHFmSz9hVGDwtCHHQ4DJUxka2gYgSE/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/13ElKWxm_g7qwcyjz_em-HYI-0U-3Eo6o/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1rrGcKiz0rdbzGUfbvAs1iUkFrUHKnDc5/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1N6GKgwN_fJfyDpzNutZP6_FhdGALpGzX/view?usp=drivesdk)

The first link is the recommended download and identifies one exact ZIP. GitHub
contains no release binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev31.zip` | 2,435,321 bytes | `013ce8741201abd5ae8640f0bce3d7f47cb8d3d5310f8e18c64a779fa0bc9f24` |
| `persistmind-0.2.1.dev31-py3-none-any.whl` | 1,115,754 bytes | `6c3cc745f347b5a4e11fe64bf098787e7c24697b8332f438a6e1f933e743c7bf` |
| `persistmind-0.2.1.dev31.tar.gz` | 1,350,330 bytes | `8fc974e35bf2a8c0e5bfdfd3fe153ae36e7d10c5d5eac3afaf90b0a339187611` |
| `internal-preview-manifest.json` | 1,723 bytes | `f2bdaf79e917fc1134eb0039a73ab92d786764eebde36bf9ca7cebbc95f52fc3` |
| `INSTALL-WINDOWS.txt` | 2,259 bytes | `a1e1f66f1dd357679591e779afdf3d2ee86cdb987d0ef9b843df0030916bf884` |
| `Install-PersistMind.ps1` | 2,923 bytes | `f4c8c5b8a3bb1623249b5bec7c1f18854afe416e18de4e00d8b60e04f89cae4f` |
| `SHA256SUMS.txt` | 602 bytes | `1ca1f5055af1dfe6dd81601660a2d4faa08a7f487f457c16a894f8ec5c44a978` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

See [artifact verification](../docs/artifact-verification.md).

## Supported systems

| Requirement | Current status |
| --- | --- |
| Windows 11 | Qualified |
| Windows 10 | Intended internal-preview target; qualification pending |
| Linux and macOS | Qualification pending; installation not published |
| Python 3.13 | Qualified on Windows 11 |
| Python 3.11 and 3.12 | Qualification pending for this candidate |
| Git | Required for repository workflows |

## Installed-wheel qualification

The exact published wheel was installed in a fresh virtual environment and
exercised in a disposable Git repository on Windows 11 Pro with Python 3.13.5.

| Gate | Result |
| --- | --- |
| Package identity and exact source commit | Passed |
| Fresh isolated wheel installation | Passed |
| Setup, indexing, doctor, and storage integrity | Passed |
| Source search and bounded context pack | Passed |
| Codex read preflight | Passed |
| Read-only MCP registration and identity | Passed; 92 tools |
| Encrypted backup and verification | Passed with the explicit development key provider |
| Staged restore with sealed source objects | Passed |
| Safe uninstall and source preservation | Passed |
| Root PowerShell installer checksum mode | Passed |

The qualification verified the FoxFlow-reported read-only storage-routing fix:
task, activity, manifest, and MCP lookups no longer require a Task State writer.
It also verified that `check-diff` uses a writable verification runtime while
keeping source-impact lookup read-only, and that `setup` refreshes agent
surfaces through the dedicated setup service.

## Restrictions and known issues

- Non-critical or disposable local repositories only
- Manual human review required
- No production use or public-beta claim
- No remote writes, team service, writable MCP, or mutation broker
- No autonomous source modification or automatic self-improvement adoption
- Windows 10, Python 3.11/3.12, Linux, and macOS qualification is pending
- The production Windows keyring backup path was not observed because the test
  host's Credential Manager was saturated by pre-existing test credentials
- Qualification is intentionally focused on the corrected storage-routing,
  setup, installed-artifact, and FoxFlow integration paths; no full historical
  regression-suite claim is made
- The artifact is unsigned and may trigger host download warnings
- There is no production, enterprise, compatibility, or response-time SLA

Read the [release notes](release-notes/0.2.1.dev31.md) and
[known issues](../docs/known-issues.md).
