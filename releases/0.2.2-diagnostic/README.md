# PersistMind 0.2.2 Diagnostic Bundle

> [!WARNING]
> This is a diagnostic Windows bundle for controlled local testing. It is not a
> production release, public beta, or trusted-updater package.

## Identity

- Version: `0.2.2`
- Source repository: `abhilashsblai/PersistMind`
- Source commit now pushed: `4a70b42ac37f8d6427c87c11c895167ebb2bd653`
- Bundle source: committed diagnostic wheelhouses under
  `bundles/0.2.2/windows-py311`, `bundles/0.2.2/windows-py312`, and
  `bundles/0.2.2/windows-py313`
- Target environment: Windows, CPython 3.11 through 3.13 wheelhouses
- Production status: Not production-ready
- Installed validation target: `C:\codes\FoxFlow`
- Installed validation status: `persistmind doctor --summary` returned
  `status=healthy`, `ok=true` on 2026-07-25.

## Files Included In This Release Repository

| File | SHA-256 |
| --- | --- |
| `install-persistmind.ps1` | `137c60feb672be0300811b47f63cf926f65440e76c96260fbec76becd13d89f2` |
| `bootstrap_persistmind.py` | `f81e391e783849deca0a6356ff9a536e58494c5334b289a4d161d901d3137d4b` |
| `dependency-lock.v1.json` | `7b271f9043d5b3d5dc8eeca36c54d8c511dc15cb01fff45f9adafebac084b897` |

## External Artifact

The installable diagnostic wheelhouses are now committed to this Git repository
under `bundles/0.2.2`. The controlled Google Drive release channel is retained
as historical distribution metadata and backup.

Corrected r2 Drive folder:
`https://drive.google.com/drive/folders/1xyGi0Wd3rsGCaZ13pXUaqbwYp3mS7OeD`

The earlier diagnostic folder
`https://drive.google.com/drive/folders/14XQGkpFKaQSc-YZDVr1x0Nc5gZ88A0-Z`
is superseded because its wheel carried stale generated storage metadata.

Uploaded files:

| File | Drive ID |
| --- | --- |
| `install-persistmind.ps1` | `1e-KYxSeBqxgtOYobreuDvfk7srl6XgVK` |
| `bootstrap_persistmind.py` | `18mGPjIu9UM-8Tn0-L5VBhkmp4UzMZ9nk` |
| `persistmind-0.2.2-py3-none-any.whl` | `1fq6_WT5_x6rMS5VswEdKc4CxS3nSBrDw` |
| `dependency-lock.v1.json` | `1v7Dnwi8MUFIPMRkq8ekUXBQXkUo9f5ze` |

| Artifact | SHA-256 |
| --- | --- |
| `bundles/0.2.2/windows-py311/persistmind-0.2.2-py3-none-any.whl` | `1b953c42396c681d8531c3d2560bdb61b2d9be1d4161dadbbfecb8a221aaf75b` |
| `bundles/0.2.2/windows-py312/persistmind-0.2.2-py3-none-any.whl` | `1b953c42396c681d8531c3d2560bdb61b2d9be1d4161dadbbfecb8a221aaf75b` |
| `bundles/0.2.2/windows-py313/persistmind-0.2.2-py3-none-any.whl` | `1b953c42396c681d8531c3d2560bdb61b2d9be1d4161dadbbfecb8a221aaf75b` |

## 2026-08-05 Refresh

This diagnostic bundle was refreshed from source commit
`4a70b42ac37f8d6427c87c11c895167ebb2bd653`. The refreshed wheel includes the
outcome-closure contract hardening: non-pass terminal `task_close`,
remediation-attempt evidence with wait/backoff/transient recovery accounting,
hydrated accepted-attempt visibility, and MCP tools for working-memory promote
and decline.

## Required Verification Before Use

Before using this diagnostic bundle in another project:

1. Confirm the installer and bootstrap hashes above.
2. Confirm the matching wheelhouse checksums in
   `bundles/0.2.2/<bundle>/SHA256SUMS.txt`.
3. Treat all results as diagnostic evidence only.
4. Do not label this artifact as production-ready.
5. Do not use `persistmind update` or trusted production promotion with this
   unsigned bundle.

Install from a clone:

```powershell
.\installer\install-from-repo.ps1 -Repo C:\Path\To\Project -Agents codex -SkipIndex
```

For Codex installs, the wrapper also installs or refreshes the bundled
Codex-specific `persistmind-workflow` skill at
`%USERPROFILE%\.codex\skills\persistmind-workflow`. Restart Codex after
installation so new sessions can use the skill when working through PersistMind
preflight, plans, checkpoints, verification, and outcomes.

## Known Open Production Blockers

The production blocker ledger remains in the source repository at
`plans/blockers/production-readiness-pending-blockers-2026-07-25.md`.
