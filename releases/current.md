# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal-preview record, not a public-beta or
> production download page. Access to the Drive files may require approval.

## Release identity

- Version: `0.2.1.dev29`
- Release type: Internal Windows Preview
- Source commit: [`f83781d5022af1834f842c3dfeffb438c6013ba4`](https://github.com/abhilashsblai/PersistMind/commit/f83781d5022af1834f842c3dfeffb438c6013ba4)
- Build timestamp: `2026-07-19T13:23:34.397349Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution channel: designated Google Drive release channel
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1vwEKHmyvq1MDz5edbuhUh1329FXo79eP/view?usp=drivesdk)**
- [Version-specific Drive folder](https://drive.google.com/drive/folders/1fVt44iXYZEzmkpuIKbZT8bxl_48JjyNn)
- [Wheel](https://drive.google.com/file/d/1pt56geMeUykchgKkwZpQzJTsBY4QO2Kg/view?usp=drivesdk)
- [Source distribution](https://drive.google.com/file/d/1Z5VPZHc142wNulaNf3lN3uHhneBL0wt6/view?usp=drivesdk)
- [Checksum-verifying installer](https://drive.google.com/file/d/1BHXxZdQestopEoKQe1fCC_4Gl0irxRQg/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1Albdipzg58T0py8zhyH4DAlcu-fz0Nvj/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1_EME8XkhZO6XwL7EA8QC3_cXGvogJ7tK/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1uuNT4N-BW9vWtd3sBujlHwdKmzUYhKdF/view?usp=drivesdk)

The first link is the recommended download and identifies one exact ZIP. GitHub
contains no release binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev29.zip` | 2,434,007 bytes | `ab64122adb3b7820ef11e130f3e15339553a1683b57d2f847b490f999d8ff709` |
| `persistmind-0.2.1.dev29-py3-none-any.whl` | 1,115,538 bytes | `df73341a2598a1415bcb366deeb2523cd61537608f6800b05bf2e3f2a70dfa5f` |
| `persistmind-0.2.1.dev29.tar.gz` | 1,349,274 bytes | `8f7b473bcf6bcb2fb19dd26f95764b11ab2d2270dabfa06a67a7896499bc4022` |
| `internal-preview-manifest.json` | 1,723 bytes | `0aefa2f3de29dbf263dc11cf35d5e2f22d5cdf6e1d64f5aceee6a5ff839212a9` |
| `INSTALL-WINDOWS.txt` | 2,259 bytes | `d1e333c9804cd9eead73c9245eb9a994eb686091972583e803491ab19c0bfce9` |
| `Install-PersistMind.ps1` | 2,923 bytes | `44a51963ea87ef9a08ab6fec026f395653eaed72368aa4bd6181285ad06b7f9c` |
| `SHA256SUMS.txt` | 602 bytes | `f955b3c4f181a3a2c040f8b7f6777f82e16c4deb26dc9b6055c0b8c43426fdc6` |

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

The qualification uncovered and fixed a staged-restore collision involving the
content-addressed `objects/sha256` directory. The regression test and exact
installed-wheel restore both passed after the fix.

## Restrictions and known issues

- Non-critical or disposable local repositories only
- Manual human review required
- No production use or public-beta claim
- No remote writes, team service, writable MCP, or mutation broker
- No autonomous source modification or automatic self-improvement adoption
- Windows 10, Python 3.11/3.12, Linux, and macOS qualification is pending
- The production Windows keyring backup path was not observed because the test
  host's Credential Manager was saturated by pre-existing test credentials
- The source tree still contains legacy tests that import retired monolithic
  APIs; the next-generation release checks and storage regression tests pass,
  but the full historical suite is not clean
- The artifact is unsigned and may trigger host download warnings
- There is no production, enterprise, compatibility, or response-time SLA

Read the [release notes](release-notes/0.2.1.dev29.md) and
[known issues](../docs/known-issues.md).
