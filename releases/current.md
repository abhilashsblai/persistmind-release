# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal-preview record, not a public-beta or
> production download page. Access to the Drive files may require approval.

## Release identity

- Version: `0.2.1.dev15`
- Release type: Internal Windows Preview
- Source commit: [`1e26c25f91e8a3bc3b7cc98046e63d8b9cd250ca`](https://github.com/abhilashsblai/PersistMind/commit/1e26c25f91e8a3bc3b7cc98046e63d8b9cd250ca)
- Build timestamp: `2026-07-17T06:15:12.482359Z`
- Runtime profile: `windows-internal-preview` (Core Local boundary)
- Distribution channel: designated Google Drive release channel
- Production: No
- Public beta: No
- Officially signed: No

## Download

- **[Qualified Windows preview ZIP](https://drive.google.com/file/d/1lQt8FB7koSMylYCsJ-sUJLr_hhyyLPVB/view?usp=drivesdk)**
- [Wheel](https://drive.google.com/file/d/1Crk6-pUNnPLYK8JAKu4nrLCklKLu6SFk/view?usp=drivesdk)
- [Checksum-verifying installer](https://drive.google.com/file/d/10U67rhNKhAes6Q0AP78bC2xfyk-JZEwq/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1_9DyJAwv4hCDNgw2gDIgBiHZTvAp1Szu/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1pmM5SgplPHV3H5vbXqltPPAQpFg7GkXd/view?usp=drivesdk)

The first link is the recommended download and identifies one exact ZIP, not a
multi-release folder. GitHub contains no release binary.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.1.dev15.zip` | 2,829,621 bytes | `4d5edaf1ff008aa45bb340de15c735f9966bfac48eff2505d9f5d81cc23f4598` |
| `persistmind-0.2.1.dev15-py3-none-any.whl` | 1,308,007 bytes | `4f79e8eaa3dcedff672471fbfdfd1745ccd5ab913af7b2ccb1288e6e9b08fc77` |
| `persistmind-0.2.1.dev15.tar.gz` | 1,551,929 bytes | `12a79691ddbdee46508fe0ed2cee617b888c98fbd54c9428745c2aa5ce21f9e1` |
| `internal-preview-manifest.json` | 1,723 bytes | `c28e0985dcb2275d462769ea97bdf34d185cded993436ea1438d945503a8be64` |
| `Install-PersistMind.ps1` | 2,478 bytes | `565352e5eb4d461307c6404ece21544acf6e1c1b17aa312375b02ea227ae2401` |

- Signature status: unsigned internal preview
- Trusted updater status: ineligible

See [artifact verification](../docs/artifact-verification.md).

## Supported systems

| Requirement | Current status |
| --- | --- |
| Windows 11 | Qualified |
| Windows 10 | Intended internal-preview target; qualification pending |
| Linux | Qualification pending; installation not published |
| macOS | Qualification pending; installation not published |
| Python 3.12 | Qualified on Windows 11 |
| Python 3.11 and 3.13 | Qualification pending for this candidate |
| Git | Required for repository workflows |

## Focused external-project qualification

The exact installed wheel was exercised in a fresh `plugin-ytdownloader`
repository rather than only in its source checkout.

| Gate | Result |
| --- | --- |
| Package identity and checksum | Passed |
| Fresh isolated wheel installation | Passed |
| Setup, indexing, and doctor | Passed |
| Task intake and agent session | Passed |
| Context pack, plan, and write preflight | Passed |
| Scoped implementation and diff check | Passed; no out-of-pack paths |
| Python project tests | 9 passed |
| JavaScript project tests | 8 passed |
| Three plan checkpoints | Passed |
| Verification, outcome, and session closure | Passed |
| Loopback health, token, origin, job, and status checks | Passed |
| Real public YouTube audio download | Passed; 2,191,601-byte M4A |
| Read-only MCP identity probe | Passed |
| Chrome UI load and click | Not run; Chrome was not running |
| Backup, restore, updater, and rollback | Pending for release promotion |

PersistMind recorded the following workflow chain:

- task session `12e0c473336a0967511f27fd5fad20781c041c55ac9cfba6c6024443596d38f2`;
- agent session `f90ded10ef15d2052258ae289e35f6162ee0109923056a700d620fae6629c338`;
- context pack `030c024139d7959c7f68c6382612796ffff6db3416ae2680fea7af9b8d328ccf`;
- plan `a81e98cfa55ebe961269f2ffd044d80c0ae4948db49cb18163a8be978324b7ef`;
- outcome `5bd462053631c686d19f8c1ab2ded3708a26845c3539059141d684d5fe80bb1d`.

The session reached intake, pack, plan, execute, preflight, and outcome states,
ended `pass`, and released its leases. Advanced intelligence remained disabled
by the locked release profile.

## Restrictions and known issues

- Non-critical or disposable local repositories only
- Manual human review required
- No production use or public-beta claim
- No remote writes, team service, writable MCP, or mutation broker
- No autonomous source modification or automatic self-improvement adoption
- Chrome UI automation remains a manual check for this record
- Windows 10, Python 3.11/3.13, Linux, and macOS qualification is pending
- The artifact is unsigned and may trigger host download warnings
- There is no production, enterprise, compatibility, or response-time SLA

Read the [release notes](release-notes/0.2.1.dev15.md) and
[known issues](../docs/known-issues.md).
