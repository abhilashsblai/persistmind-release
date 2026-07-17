# Release Policy

PersistMind release maturity is evidence-based. Implemented code does not become
supported merely because it can be imported or invoked.

```text
Internal Preview -> Closed Beta -> Public Beta -> Stable -> LTS
```

## Internal Preview

Narrow, explicitly restricted evaluation. May be unsigned. Requires a frozen
commit, installed-artifact smoke, checksums, limitations, and a bounded runtime
profile. No production claim.

## Closed Beta

Qualified artifact shared with selected design partners. Requires all beta
blockers classified and closed, broader platform results appropriate to the
declared boundary, upgrade/rollback and recovery evidence, and a monitored soak.

## Public Beta

Publicly available pre-production channel. Requires signed distribution,
documented support and compatibility policies, security review, operational
telemetry, and stable recovery behavior.

## Stable

Production-approved channel with supported-platform matrices, signed artifacts,
operational monitoring, disaster-recovery exercises, compatibility policy, and
release approval evidence.

## LTS

A stable line with an explicit maintenance window, patch policy, supported
upgrade paths, and end-of-support date.

Every release must meet [release qualification](release-qualification.md) and
publish its evidence before its maturity label is used.
