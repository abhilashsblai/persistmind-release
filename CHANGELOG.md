# Changelog

## 0.2.1.dev17 - 2026-07-17

### Fixed

- `workflow next` now supports the documented manual `task start → pack → plan`
  lifecycle instead of requiring a hidden recommendation created only by
  `workflow start`.
- Missing split workflow recommendations are reconstructed from authoritative
  task text, bound pack, accepted plan paths/capabilities, and impact evidence,
  then persisted for subsequent calls.
- Existing affected tasks self-heal on their next `workflow next` invocation;
  `workflow brief` is no longer a required workaround.

### Qualification

- Exact-commit Windows 11/Python 3.12 installed-wheel lifecycle passed.
- The original FoxFlow task was repaired and then succeeded through the installed
  dev16 reader using the persisted recovered snapshot.

## 0.2.1.dev16 - 2026-07-17

### Fixed

- Git patch identity no longer assumes every committed byte is UTF-8; legacy
  Windows-1252 content is hashed deterministically instead of crashing source scans.
- Codex preflight, plan validation, and pack lookup now use the same split-v1
  Task and Activity authorities.
- Plans reject legacy, missing, foreign, and incorrectly task-bound pack IDs.
- CLI and MCP pack creation now honor diff-derived seed paths.
- Diff verification preserves `verification_incomplete` instead of reporting a
  misleading `internal_error` when no scoped violation exists.

### Qualification

- Exact-commit wheel and source archive built from PersistMind commit `d4666d0`.
- Isolated Windows 11/Python 3.12 wheel installation and disposable-project
  lifecycle smoke passed.
- Published installer, wheel, manifest, checksums, guide, and release ZIP to the
  private Internal Windows Previews Drive channel.

### Known limitations

- This remains an unsigned internal preview for non-critical repositories.
- Windows 10, Python 3.11/3.13, Linux, and macOS qualification is pending.
- Real-project acceptance remains tester feedback rather than a production claim.

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
