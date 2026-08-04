# PersistMind 0.2.2 Diagnostic Bundle

> [!WARNING]
> This is a diagnostic Windows bundle for controlled local testing. It is not a
> production release, public beta, or trusted-updater package.

## Identity

- Version: `0.2.2`
- Source repository: `abhilashsblai/PersistMind`
- Source commit now pushed: `7904f4a`
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
| `install-persistmind.ps1` | `da1dde9789e9b04f66c1623e1e146146bc886f98a28701133da381f38241a447` |
| `bootstrap_persistmind.py` | `b1bfdb5efca8dcc686763a91e5d196035401531689021e2ca7a812f0bd883b17` |
| `dependency-lock.v1.json` | `bc22b6100fcd06953d3ad1c71278ab2047d1baa39157857299d68b6f065cbc0d` |

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
| `bundles/0.2.2/windows-py311/persistmind-0.2.2-py3-none-any.whl` | `246d141cbc638ca3509b5cb903110de3b6b9f13f8722147b7dd333a307d6c1ff` |
| `bundles/0.2.2/windows-py312/persistmind-0.2.2-py3-none-any.whl` | `246d141cbc638ca3509b5cb903110de3b6b9f13f8722147b7dd333a307d6c1ff` |
| `bundles/0.2.2/windows-py313/persistmind-0.2.2-py3-none-any.whl` | `daf420ac7642b24f727cb93342fa309c9f8b58372d8e6fa0bd4d1eabba2c8cb0` |

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
