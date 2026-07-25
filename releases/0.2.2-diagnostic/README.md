# PersistMind 0.2.2 Diagnostic Bundle

> [!WARNING]
> This is a diagnostic Windows bundle for controlled local testing. It is not a
> production release, public beta, or trusted-updater package.

## Identity

- Version: `0.2.2`
- Source repository: `abhilashsblai/PersistMind`
- Source commit now pushed: `7904f4a`
- Bundle source: local diagnostic wheelhouse
  `C:\codes\PersistMind\.tmp\production-readiness-2026-07-25\wheelhouse-py313-v022-r2`
- Target environment: Windows, CPython 3.13 wheelhouse
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

The installable wheel is intentionally not committed to this Git repository.
It should be distributed through the controlled Google Drive release channel.

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
| `persistmind-0.2.2-py3-none-any.whl` | `daf420ac7642b24f727cb93342fa309c9f8b58372d8e6fa0bd4d1eabba2c8cb0` |

## Required Verification Before Use

Before using this diagnostic bundle in another project:

1. Confirm the installer and bootstrap hashes above.
2. Confirm the wheel hash above if installing from Drive or local wheelhouse.
3. Treat all results as diagnostic evidence only.
4. Do not label this artifact as production-ready.
5. Do not use `persistmind update` or trusted production promotion with this
   unsigned bundle.

## Known Open Production Blockers

The production blocker ledger remains in the source repository at
`plans/blockers/production-readiness-pending-blockers-2026-07-25.md`.
