# Current PersistMind Release

> [!IMPORTANT]
> This is an unsigned private internal preview for non-critical local
> repositories. It is not a public beta, production release, or trusted-updater
> package.

## Release identity

- Version: `0.2.2.dev1`
- Release type: Internal Windows Preview
- Source commit: [`ee5ede7df9aef29d6e99c9ef16ef7ff0d185838a`](https://github.com/abhilashsblai/PersistMind/commit/ee5ede7df9aef29d6e99c9ef16ef7ff0d185838a)
- Build timestamp: `2026-07-24T10:48:19.959180Z`
- Runtime profile: `windows-internal-preview`
- Distribution: designated Google Drive internal-preview channel
- Qualified environment: Windows 11, CPython 3.12
- Production/public beta/officially signed: No

## Download

- **[Windows preview ZIP](https://drive.google.com/file/d/1MAQKcVNRBeUnd8LeMv2GbRHLD4dd8mzk/view?usp=drivesdk)**
- [Version-specific Drive folder](https://drive.google.com/drive/folders/1nlWifdT2dub2azRIBwrTw6sE5-U4pTJb)
- [Wheel](https://drive.google.com/file/d/1olV9rEedzJWNzaimpvHtBdX7iAv2sK53/view?usp=drivesdk)
- [Source distribution](https://drive.google.com/file/d/1MCJVxFOwvrbqM562GVF-H90Nhz-EapQI/view?usp=drivesdk)
- [Checksum-verifying installer](https://drive.google.com/file/d/19j0amPS67XsyNrzXCgvIaeH240uQ9xfx/view?usp=drivesdk)
- [Windows installation guide](https://drive.google.com/file/d/1P_iXYce4HJPDw4zdc4ydDdOvIpy4CTsH/view?usp=drivesdk)
- [Release manifest](https://drive.google.com/file/d/1A4si0TovFBGVfCVbq6Oy3Su8J-wju8eG/view?usp=drivesdk)
- [SHA-256 list](https://drive.google.com/file/d/1U2lZNRR1vjT1QS7EJXoX-sqtW0I3icKT/view?usp=drivesdk)

GitHub contains source and release metadata, not release binaries.

## Artifact verification

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `PersistMind-Windows-Internal-Preview-0.2.2.dev1.zip` | 2,885,852 bytes | `26aba71a82beb992628cc81c309a535af280db17ab118402ef2ffd0fe3bce9f4` |
| `persistmind-0.2.2.dev1-py3-none-any.whl` | 1,407,471 bytes | `40e0e3d9369d9e6f0285825611492844d11fefecf932040ccb50b8b7d9f2a11d` |
| `persistmind-0.2.2.dev1.tar.gz` | 1,513,590 bytes | `ce9cae494b2837e4a763f327da66a5fee133bdb0854374d7a3c37c183b98fe5a` |
| `internal-preview-manifest.json` | 4,290 bytes | `76c9d726f4a44ff56255fd43ab16d21a4ecfea8ccccfd566ab920f5ed57bb370` |
| `INSTALL-WINDOWS.txt` | 2,256 bytes | `528c7adb640ef9005253fb332bb2cd1dee2b1a2d78cf023a6d68412f84ecd39b` |
| `Install-PersistMind.ps1` | 2,919 bytes | `2fcd8c7c42e55a0e12f71c13bccb5be88dc5ad6fc14dc6e3d50c37c15646a97a` |
| `SHA256SUMS.txt` | 599 bytes | `825ac15e30d276c1cdb874dffbe2f351e2bec5a68f746f280224a5dd3c22ca9a` |

## Installed-wheel qualification

The exact published wheel passed on Windows 11 with CPython 3.12:

- fresh isolated installation and healthy `doctor`;
- indexing, search, context pack, workflow, and storage verification;
- backup verification and staged-restore verification;
- Codex hook execution and a read-only MCP probe exposing 60 tools;
- safe project cleanup with source preservation; and
- reproduction of the FoxFlow plan failure as the intended typed
  `validation_failed` result instead of `internal_error`.

The complete source suite passed on the final release commit with the
repository's environment-dependent skips.

## Restrictions and known limitations

- Non-critical local repositories only; manual human review is mandatory.
- Windows 10 and Python 3.11/3.13 were not observed for this candidate.
- Linux and macOS are not qualified.
- The pinned MiniLM bundle was unavailable during qualification, so search used
  the documented local semantic fallback.
- Project cleanup removed generated agent surfaces and preserved source, but
  retained runtime storage when its ownership verifier detected
  runtime-generated unjournaled files.
- The artifact is unsigned and ineligible for `persistmind update`.
- No remote writes, team service, writable MCP, or autonomous source mutation.

See [release notes](release-notes/0.2.2.dev1.md) and
[artifact verification](../docs/artifact-verification.md).
