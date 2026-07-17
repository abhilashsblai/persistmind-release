# Release Qualification Policy

PersistMind release claims are valid only when one immutable identity flows
through source testing, build, installation, qualification, and publication.

```text
Tested commit == Built commit == Published commit == Installed commit
```

Changing source, release tooling, evidence schemas, manifests, or artifact bytes
requires a new version identity and a restarted qualification pipeline.

## Evidence required for every release

- exact source commit and clean-tree confirmation;
- version, channel, runtime profile, and build timestamp;
- artifact names, byte sizes, SHA-256 values, and signature status;
- installed-artifact tests outside the source checkout;
- operating systems and Python versions actually observed;
- storage integrity and backup/restore evidence;
- updater/rollback evidence when the updater is in scope;
- known limitations and unresolved blockers;
- installation, migration, and recovery instructions; and
- version-specific distribution location and access policy.

## Internal Preview

Requires a frozen commit, clean build, checksum, explicit unsupported boundary,
at least one installed-artifact machine result, and recovery instructions. May
be unsigned. Production use is prohibited.

## Closed Beta

Requires all beta blockers classified and closed, selected design partners,
appropriate platform coverage, upgrade/rollback and recovery evidence, genuine
usage telemetry, and a monitored soak.

## Public Beta

Requires signed distribution, public installation and support policy, security
review, broader platform evidence, operational telemetry, and stable recovery.

## Stable

Requires the declared production matrix, signed artifacts, compatibility and
support policy, monitoring, disaster-recovery exercises, long-duration soak,
and formal approval.

## LTS

Requires Stable plus a maintenance window, patch policy, upgrade paths,
deprecation notice, and end-of-support date.

Use [the qualification template](templates/qualification-template.md) for each
candidate.
