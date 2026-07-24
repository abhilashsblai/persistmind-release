# Changelog

## 0.2.2.dev1 - 2026-07-24

### Fixed

- Return typed, actionable plan-validation failures while preserving task and
  pack references.
- Distinguish unrelated failure operation IDs while deduplicating identical
  validation retries.
- Refresh packaged architecture/interface contracts and validate them in the
  release suite.
- Emit manifest-compatible Windows qualification identities.

### Qualification and publication

- Passed the full source suite on the final release commit.
- Passed exact-wheel Windows 11/Python 3.12 installation, doctor, index,
  search, context-pack, workflow, storage, backup, restore, Codex hook, MCP,
  and source-preserving cleanup gates.
- Published the exact ZIP, wheel, source distribution, installer, manifest,
  guide, and checksums to the version-specific Google Drive folder.

### Security

- Remains unsigned, local-only, non-production, and ineligible for the trusted
  updater.

## 0.2.1.dev41 candidate - 2026-07-23

### Added

- Published exact-commit dev41 wheel, source distribution, Windows ZIP,
  checksum-verifying installer, installation guide, candidate manifest, and
  checksums to the private Google Drive internal-preview channel.
- Added release-repository installation instructions and immutable Drive links.

### Candidate changes

- Migrates the legacy pytest suite to the next-generation authority and schema
  architecture.
- Adds bounded context-snippet retrieval and improves read-only hook gating.
- Includes the next-generation authority schema upgrade lifecycle, preview
  installation rollback corrections, and the dev38-dev40 authority, workflow,
  reporting, and schema-head changes.

### Qualification status

- Exact source identity, build record, isolated offline wheel installation,
  packaged runtime resources, and CLI help passed.
- Full APSW-backed install/index/search/pack/workflow qualification is blocked
  on the release host because Windows Application Control rejects the pinned
  native APSW module.
- The complete source suite passed locally in serial and four-worker modes.
- The cross-platform GitHub matrix was blocked before a runner started by the
  account billing/spending limit, so no cross-platform result is claimed.
- Dev41 does not replace dev31 as the current qualified preview.

### Security

- The candidate is unsigned, non-production, private, local-only, and
  ineligible for the trusted updater.
- Do not bypass organizational Application Control policy.

## 0.2.1.dev31 - 2026-07-19

### Fixed

- Read-only task, activity, manifest, and MCP lookups no longer attempt to
  resolve a Task State writer.
- `check-diff` and pack-aware impact verification now use the correct writable
  verification runtime while source-impact lookup remains read-only.
- The CLI now routes `setup` and `setup auto` through the dedicated agent
  surface service, so reinstalling an exact release refreshes project hooks and
  MCP launchers instead of querying an unrelated Control authority table.

### Qualification

- Twenty focused storage-routing, setup, authority, and Windows-preview tests
  passed.
- The exact installed dev31 wheel passed Windows 11/Python 3.13 identity,
  doctor, indexing, search, context-pack, workflow, MCP, backup, staged restore,
  uninstall, and packaged installer verification.
- FoxFlow now invokes the canonical dev31 environment for project and Codex MCP
  surfaces; the originally failing read-only lookups and scoped `check-diff`
  pass from that installed release.

### Security

- The preview remains unsigned, non-production, local-only, and ineligible for
  the trusted updater.
- Remote writes, writable MCP, and autonomous source modification remain disabled.

### Known limitations

- Windows 10, Python 3.11/3.12, Linux, and macOS qualification is pending.
- The production Windows keyring backup path was not observed because the test
  host's Credential Manager was saturated by pre-existing test credentials.
- Qualification was intentionally focused; no full historical regression-suite
  claim is made.

## 0.2.1.dev29 - 2026-07-19

### Added

- Next-generation eight-authority storage and application architecture.
- Drive-hosted Windows preview package, exact checksums, and installed-wheel
  qualification for Windows 11 with Python 3.13.
- Read-only MCP coverage across all 92 registered tools.

### Fixed

- Migration, concurrency, Windows path, and PowerShell release regressions.
- Staged backup restore when sealed source objects already create the target
  content-addressed directory.

### Security

- The preview remains unsigned, non-production, local-only, and ineligible for
  the trusted updater.
- Remote writes, writable MCP, and autonomous source modification remain disabled.

### Known limitations

- Windows 10, Python 3.11/3.12, Linux, and macOS qualification is pending.
- The production Windows keyring backup path was not observed because the test
  host's Credential Manager was saturated by pre-existing test credentials.
- Legacy source-suite modules still require migration to the next-generation API.

## 0.2.1.dev19 - 2026-07-17

### Fixed

- The preview ZIP now exposes the installer and installation guide at its root,
  as required by the published GitHub instructions.
- The installer searches both its own directory and the bundle's `artifacts`
  directory for the exact wheel.
- Packaging runs the documented root-level `-VerifyOnly` command before ZIP
  creation.

### Qualification

- The broken dev18 root and nested installation commands were reproduced.
- The corrected dev19 ZIP was extracted and installed into FoxFlow using the
  published command sequence.
- Setup, MCP probes, doctor, governed preflight, and the Supabase write-channel
  hook passed from the installed wheel.

## 0.2.1.dev18 - 2026-07-17

### Fixed

- Preflight hook freshness now uses task-bound semantic source, pack, plan, and
  trust revisions instead of hashing the complete SQLite database and WAL.
- Routine task/checkpoint telemetry no longer makes a green preflight stale.
- Read-only workflow inspection no longer publishes or downgrades hook policy
  readiness.
- Real plan amendments, pack rebinding, source updates, trust changes, and
  snapshot expiry continue to fail closed.

### Qualification

- Exact-commit Windows 11/Python 3.12 installed-wheel lifecycle passed.
- Dev18 was installed into FoxFlow, setup surfaces were regenerated, the exact
  affected preflight passed, and the installed hook allowed the formerly blocked
  Supabase SQL tool in about 8 ms.

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
