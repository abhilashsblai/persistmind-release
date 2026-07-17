# Changelog

## 0.2.1.dev15 - 2026-07-17

### Added

- Frozen exact-commit Windows Internal Preview release record.
- Drive-only artifact links, checksums, manifest identity, and limitations.
- Installed-wheel qualification in a fresh external Chrome-extension project.

### Fixed

- Project setup fallback when Python is supplied through `uv`.
- Evidence-directory handling in release qualification.
- Generated commands that could invoke an unrelated global executable.
- Plan-to-preflight reuse of the task's bound context pack.

### Security

- Remote writes, writable MCP, and autonomous source modification remain disabled.
- The unsigned preview remains excluded from the trusted updater.

### Known limitations

- Windows 10, Python 3.11/3.13, Linux, and macOS qualification is pending.
- Chrome UI automation remains a manual check.
- Backup/recovery, updater/rollback, and signing gates remain pending.
- No production, public-beta, enterprise, or support-SLA claim.
