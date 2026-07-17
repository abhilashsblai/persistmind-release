# PersistMind Releases

PersistMind provides persistent project intelligence and governed local
workflows for AI engineering.

This repository contains release documentation, checksums, links, and source
history only. Installer, wheel, source-distribution, and ZIP bytes are hosted
exclusively in Google Drive.

## Current release

**PersistMind 0.2.1.dev4 - Internal Windows Preview**

- [Open the exact `0.2.1.dev4` release folder](https://drive.google.com/drive/folders/1HT9bAsR4S9D1bmJ8MtaX9GiweuHK77U1)
- [Download the packaged ZIP](https://drive.google.com/file/d/1Si6ETnyg5F66gFSgw_nUkhhh_-7-vKWY/view)
- [Download the Python wheel](https://drive.google.com/file/d/1w0FkMNt3gTQ3d6oM-DMeKt6knyLzyNun/view)
- [Download `SHA256SUMS.txt`](https://drive.google.com/file/d/1QeKqS7iEQZk8eRJjzzjqgzkuj3K7je1e/view)
- [Read the Windows installation instructions](https://drive.google.com/file/d/1CDpY7GIAZRpYnsxNrwAKa3BH-1mlh20O/view)
- [Read the release notes](docs/releases/persistmind-0.2.1.dev4-windows-internal-preview.md)

The folder link above opens only the current release. It does not open the
parent folder containing multiple releases.

## Integrity

Verify downloads before installation:

| Artifact | SHA-256 |
| --- | --- |
| Wheel | `e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad` |
| Source distribution | `1375c3b705bad562b9fc1301125d4f910b6e8757edbd11fba32082703f8ff7dc` |
| Packaged ZIP | `fbf8324921182d551c6e28a095ebb366ede9c63bca87961f7ff2ec27f81e2123` |

Source commit:
[`af93e56e54350d82ae0d40a8bdcce71dd0ac7c03`](https://github.com/abhilashsblai/PersistMind/commit/af93e56e54350d82ae0d40a8bdcce71dd0ac7c03)

## Qualification and restrictions

The same wheel passed installed-package qualification on Windows with Python
3.11, 3.12, and 3.13. Windows 11 was directly qualified; Windows 10 was not
directly observed in this run.

This release is unsigned and restricted to disposable or non-critical local
repositories with manual human review. It is not a public beta, production
release, or trusted automatic-update artifact. Linux, macOS, remote writes,
writable MCP, and autonomous source modification are unsupported.

Do not use the signed production updater for this preview. Follow the supplied
Windows instructions and install the checksum-verified wheel into an isolated
virtual environment.

## Distribution policy

- Release bytes: Google Drive only.
- GitHub: documentation, checksums, links, and source history only.
- No wheel, installer, ZIP, or source distribution may be committed here.
- Each README release link must target one exact version folder, never the
  multi-release parent folder.

## License

[PersistMind Personal Use License](LICENSE)

Copyright (c) 2026 Abhilash Pillai. All rights reserved.
