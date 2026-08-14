# PersistMind

> Persistent project intelligence for AI engineering.

PersistMind is a local-first project intelligence layer for AI coding agents. It
helps agents understand a repository, retrieve the right context, preserve
approved project knowledge, evaluate the impact of changes, and continue
engineering work across sessions.

It works alongside tools such as Codex, Claude Code, Cursor, and MCP-compatible
clients. PersistMind does not replace the coding agent or Git; it supplies the
persistent context, governance, verification, and project memory around them.

`Current candidate: 0.2.7` `Built: Windows 11 / Python 3.13`
`Profile: windows-stable`
`Platform: Windows` `MCP: Read-only` `Production: Not qualified`

`Source pushed: 210d2ef` `Wheel SHA-256: 6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702`

> [!WARNING]
> Historical Git tags and any former GitHub Releases assets are not the current
> recommended PersistMind distribution. Review
> [Current Release Status](#current-release-status) and
> [releases/current.md](releases/current.md) before installing.

The current release installer scripts are committed under
[installer/](installer/). This repository also includes self-contained
hash-locked Windows diagnostic wheelhouses under
[bundles/0.2.2](bundles/0.2.2/), so a clean Windows machine can install
PersistMind into another local project directly from a clone of this GitHub
repository.

## Current Release Status

PersistMind `0.2.7` is available as an unsigned Windows release candidate for
controlled validation. It was built from pushed source commit
[`210d2ef`](https://github.com/abhilashsblai/PersistMind/commit/210d2ef7dc6421381d823a4a0770667acc679c8a)
on Windows 11 with CPython 3.13.5. It is not a public beta or production
release. See [releases/0.2.7-candidate](releases/0.2.7-candidate/README.md).

The committed `0.2.2` diagnostic wheelhouses were refreshed on 2026-08-05 from
source commit `4a70b42ac37f8d6427c87c11c895167ebb2bd653`. This update carries
the outcome-closure contract hardening: `task_close` for non-pass terminal
states, remediation-attempt accounting with wait/backoff/transient recovery
details, and MCP parity for working-memory promote/decline.

| Item | Status |
| --- | --- |
| Release level | Windows Release Candidate |
| Supported profile | `windows-stable` |
| Windows 11 | Build environment observed; full promotion evidence pending |
| Windows 10 | Qualification pending |
| Linux and macOS | Qualification pending |
| Distribution | This release repository under `releases/0.2.7-candidate` |
| Production use | Not supported |
| Public beta | Not available |
| MCP | Read-only |
| Remote writes | Disabled |
| Autonomous source modification | Disabled |

## Why PersistMind Exists

AI coding agents are powerful, but they commonly lose project context between
sessions. They may retrieve the wrong files, repeat investigations, overlook
business rules, modify code outside the intended scope, or fail to preserve why
a previous decision was made.

PersistMind provides a persistent intelligence layer between the repository and
the coding agent. The intended outcomes are:

- better context selection;
- less repeated investigation;
- safer, more scoped changes;
- continued tasks across sessions; and
- traceable decisions and verification.

Read [What is PersistMind?](docs/what-is-persistmind.md).

## What PersistMind Does

### Builds repository intelligence

Indexes source files and repository structure into an identified local snapshot.

### Creates focused context packs

Selects relevant context within a token budget and records provenance.

### Preserves project memory

Stores approved project facts, decisions, rules, and workflow history without
treating unapproved memory as authority.

### Governs AI engineering work

Tracks tasks, plans, checkpoints, allowed write scope, verification, and
outcomes.

### Evaluates change impact

Surfaces related files and tests before and after a modification.

### Integrates with coding agents

Provides read-only context and repository intelligence to Codex, Claude Code,
Cursor, VS Code clients, and MCP-compatible tools.

## Example

Task:

> Make the address on a WordPress Contact Us page editable through the CMS.

PersistMind can:

1. Locate where the existing address is generated.
2. Identify whether it is hard-coded, stored in theme options, or loaded from
   another source.
3. Retrieve the relevant templates, settings, and approved project rules.
4. Create a scoped implementation plan.
5. Validate the files changed by the agent.
6. Recommend affected tests.
7. Record the final decision and reusable project knowledge after review.

## How PersistMind Works

```text
Task
  -> Repository snapshot
  -> Source indexing and retrieval
  -> Context pack
  -> Agent execution
  -> Diff and verification
  -> Audit and approved memory
```

PersistMind resolves repository state before creating bounded context. Agent
work is checked against the intended plan and scope. Reviewed verification and
outcomes can become durable local evidence.

See [How PersistMind works](docs/how-persistmind-works.md) and the
[architecture overview](docs/architecture.md).

## Capability Status

| Capability | Status | Default profile |
| --- | --- | --- |
| Repository indexing | Core | Core Local |
| Lexical source search | Core | Core Local |
| Context packs | Core | Core Local |
| Impact analysis | Core | Core Local |
| Local project memory | Core | Core Local |
| Governed workflows | Core | Core Local |
| Read-only MCP | Core | Core Local |
| Semantic retrieval | Experimental | Labs |
| Architecture analysis | Experimental | Labs |
| Cognitive improvement and adaptive learning | Experimental | Labs |
| Anticipation | Experimental | Labs |
| Team server | Planned / unavailable | Team Preview |
| Writable MCP | Disabled | None |
| Autonomous self-modification | Disabled | None |

Status terms are **Core**, **Preview**, **Experimental**, **Disabled**, and
**Planned**. Implemented code is not automatically release-qualified. See the
[capability status](docs/capability-status.md).

## Runtime Profiles

### Core Local

The supported internal-preview boundary:

- local repository and filesystem;
- CLI workflows and local mutations;
- local storage, with backup and staged-restore smoke coverage;
- read-only MCP; and
- mandatory human review.

### Labs

Experimental and disabled by default. Labs output is advisory, is not release
evidence, and carries no autonomous authority.

### Team Preview

Not currently available for production. Remote identity, multi-user service,
tenant isolation, and remote writes require separate security and qualification
gates.

Read [Core Local](docs/core-local.md) and
[runtime profiles](docs/runtime-profiles.md).

## Download and Install PersistMind

PersistMind is currently distributed as a controlled Windows release candidate.
This GitHub repository now contains the `0.2.7` wheel, PowerShell installer,
bootstrap helper, uninstall helper, CPython 3.13 offline wheelhouse,
dependency lock, build record, and checksums under
[`releases/0.2.7-candidate`](releases/0.2.7-candidate/README.md).

Before installing, the version, filename, source commit, file size, SHA-256,
dependency lock, and build record must match
[releases/current.md](releases/current.md). The wheel SHA-256 is
`6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702`.

Install from the release folder:

```powershell
cd releases\0.2.7-candidate
$wheelHash = '6dc3283addef93878975060da81f2a0dfa870375fff1570b80e7868180927702'
Get-FileHash .\persistmind-0.2.7-py3-none-any.whl -Algorithm SHA256
Get-FileHash .\dependency-lock.v1.json -Algorithm SHA256
.\install-persistmind.ps1 `
  -BootstrapPath .\bootstrap_persistmind.py `
  -LocalWheelPath .\persistmind-0.2.7-py3-none-any.whl `
  -LocalWheelSha256 $wheelHash `
  -Version 0.2.7
```

Do not use the trusted updater for this unsigned candidate.

The older self-contained `0.2.2` GitHub diagnostic wheelhouses remain under
[bundles/0.2.2](bundles/0.2.2/) for historical controlled validation only.
They are not production-ready, public beta, or trusted-updater packages.

See:

- [Current release](releases/current.md)
- [0.2.7 release candidate](releases/0.2.7-candidate/README.md)
- [Windows installation](docs/windows-installation.md)
- [Artifact verification](docs/artifact-verification.md)
- [Known limitations](docs/limitations.md)

Linux and macOS instructions will be published only after their required
platform and Python-version matrices pass.

## Release Channels

| Channel | Audience | Status | Artifact location |
| --- | --- | --- | --- |
| Release Candidate | Approved testers | Current | This repository |
| Internal Diagnostic | Local Windows validation | Historical | This GitHub repository (`bundles/0.2.2`) |
| Internal Preview | Approved testers | Historical | Private Google Drive |
| Closed Beta | Selected design partners | Planned | Controlled Drive channel |
| Public Beta | Public evaluators | Not available | To be announced |
| Stable | Production users | Not available | To be announced |
| LTS | Long-lived production users | Not available | To be announced |

GitHub is the canonical source for documentation, release metadata,
installation guidance, qualification status, checksums, release history, and
the current candidate artifacts. A download is acceptable only when its
identity and evidence match the current release record.

See [release channels](releases/release-channels.md).

## Updating an Internal Preview

Release candidates are installed manually from a verified release artifact.
Automatic updates are not enabled for unsigned candidate packages.

Before installing a newer preview:

1. Review its release record.
2. Verify the artifact identity and checksum.
3. Back up PersistMind state.
4. Follow the release-specific migration instructions.
5. Install into an isolated environment.
6. Run `persistmind doctor` and the release smoke checks.

Read the [upgrade guide](docs/upgrade-guide.md).

## Release Qualification and Artifact Verification

Every release record publishes the tested source commit, build identity,
platform matrix, installed-artifact results, known limitations, and integrity
metadata.

```text
Tested commit == Built commit == Published commit == Installed commit
```

For `0.2.1.dev31`:

| Target | Result |
| --- | --- |
| Windows 11 | Passed |
| Windows 10 | Qualification pending |
| Python 3.13 | Installed wheel passed |
| Python 3.11 and 3.12 | Qualification pending |
| Fresh disposable-project install/index/search/pack | Passed |
| Codex read preflight | Passed |
| Read-only MCP boundary | Passed |
| Encrypted backup and staged restore | Passed with the explicit development key provider; production keyring path not observed |
| Safe uninstall and source preservation | Passed |
| Trusted updater, rollback, and signing | Pending for promotion |
| Linux and macOS | Qualification pending |

SHA-256 verifies exact bytes but does not authenticate an unsigned publisher.
Public and stable channels require signature verification in addition to
checksums.

- [Qualification policy](releases/qualification-policy.md)
- [Artifact verification](docs/artifact-verification.md)
- [Release trust model](security/release-trust-model.md)

## Coding-Agent Integrations

The current supported integration boundary is local, read-only context through
MCP plus explicitly reviewed CLI workflows.

- [Bundled Codex skill](codex-skills/README.md)
- [Integration overview](docs/integrations.md)
- [Codex guide](guides/codex.md)
- [Claude Code guide](guides/claude.md)
- [Cursor guide](guides/cursor.md)
- [VS Code guide](guides/vscode.md)
- [MCP guide](docs/mcp-guide.md)

## Uninstalling

PersistMind package removal must preserve project source and unowned files.
Review local state before cleanup, and use a dry-run ownership plan whenever an
uninstaller is supplied for a release.

See [Uninstall and Cleanup](docs/uninstall-and-cleanup.md).

## Documentation

### Start and understand

- [Getting started](docs/getting-started.md)
- [What is PersistMind?](docs/what-is-persistmind.md)
- [How PersistMind works](docs/how-persistmind-works.md)
- [Architecture](docs/architecture.md)
- [Core Local](docs/core-local.md)
- [Capability status](docs/capability-status.md)

### Install and operate

- [Supported platforms](docs/supported-platforms.md)
- [Windows installation](docs/windows-installation.md)
- [Artifact verification](docs/artifact-verification.md)
- [CLI reference](docs/cli-reference.md)
- [MCP guide](docs/mcp-guide.md)
- [Storage and backup](docs/storage-and-backup.md)
- [Troubleshooting](docs/troubleshooting.md)
- [FAQ](docs/faq.md)

### Release and trust

- [Current release](releases/current.md)
- [Release channels](releases/release-channels.md)
- [Qualification policy](releases/qualification-policy.md)
- [Versioning policy](releases/versioning-policy.md)
- [Support policy](releases/support-policy.md)
- [Release history](releases/release-history.md)
- [Security model](security/release-trust-model.md)

## Security and Privacy

The current profile is local-first, keeps MCP read-only, and rejects remote
authority expansion. Evidence and support reports must redact credentials,
private source, private paths, database contents, and signing material. Private
keys must never be placed in source control, release bundles, issues, or logs.

- [Security policy](SECURITY.md)
- [Release trust model](security/release-trust-model.md)
- [Vulnerability reporting](security/vulnerability-reporting.md)

## Support and Contributing

- [Support](SUPPORT.md)
- [Contributing](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

The current internal preview has no production, enterprise, response-time, or
compatibility SLA.

## License

PersistMind is distributed under the
[PersistMind Personal Use License](LICENSE). Commercial, enterprise,
institutional, consulting, hosted, and company-wide use requires a separate
written agreement.

Copyright (c) 2026 Abhilash Pillai. All rights reserved.
