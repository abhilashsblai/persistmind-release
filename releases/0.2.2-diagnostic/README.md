# PersistMind 0.2.2 Diagnostic Bundle

> [!WARNING]
> This is a diagnostic Windows bundle for controlled local testing. It is not a
> production release, public beta, or trusted-updater package.

## Identity

- Version: `0.2.2`
- Source repository: `abhilashsblai/PersistMind`
- Source commit now pushed: `6259b04`
- Bundle source: local diagnostic wheelhouse
  `C:\codes\PersistMind\.tmp\production-readiness-2026-07-25\wheelhouse-py313-v022`
- Target environment: Windows, CPython 3.13 wheelhouse
- Production status: Not production-ready

## Files Included In This Release Repository

| File | SHA-256 |
| --- | --- |
| `install-persistmind.ps1` | `da1dde9789e9b04f66c1623e1e146146bc886f98a28701133da381f38241a447` |
| `bootstrap_persistmind.py` | `b1bfdb5efca8dcc686763a91e5d196035401531689021e2ca7a812f0bd883b17` |
| `dependency-lock.v1.json` | See file in this directory |

## External Artifact

The installable wheel is intentionally not committed to this Git repository.
It should be distributed through the controlled Google Drive release channel.

| Artifact | SHA-256 |
| --- | --- |
| `persistmind-0.2.2-py3-none-any.whl` | `67736c5f2b6e962c389b08686cf5c72a82895fed621a7e48b6c6798667bee820` |

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
