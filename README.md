# PersistMind

> Persistent project intelligence for AI engineering.

PersistMind is a local-first project intelligence layer for AI coding agents. It
helps agents understand a repository, retrieve the right context, preserve
approved project knowledge, evaluate the impact of changes, and continue
engineering work across sessions.

It works alongside tools such as Codex, Claude Code, Cursor, and MCP-compatible
clients. PersistMind does not replace the coding agent or Git; it supplies the
persistent context, governance, verification, and project memory around them.

`Release: Internal Windows Preview` `Profile: Core Local`
`Platform: Windows` `MCP: Read-only` `Production: Not qualified`

> [!WARNING]
> Historical Git tags and any former GitHub-hosted artifacts are not the current
> recommended PersistMind distribution. GitHub Releases is not an active
> delivery channel. Always review [Current Release Status](#current-release-status)
> and [releases/current.md](releases/current.md) before installing.

## Current Release Status

PersistMind `0.2.1.dev18` is available only for approved private Windows internal
testing. It is not a public beta or production release.

| Item | Status |
| --- | --- |
| Release level | Internal Windows Preview |
| Supported profile | Core Local (`windows-internal-preview`) |
| Windows 11 | Qualified on the current candidate |
| Windows 10 | Internal-preview target; qualification pending |
| Linux and macOS | Qualification pending |
| Distribution | Private Google Drive channel for approved testers |
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
- local storage, with backup and recovery qualification still pending;
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

PersistMind is currently distributed privately to approved Windows internal
preview testers. This GitHub repository provides product documentation, release
notes, qualification information, artifact metadata, and installation guidance.
It does not host release binaries. The current qualified artifact is stored in
the designated Google Drive release channel.

**[Download the exact `0.2.1.dev18` Windows preview ZIP](https://drive.google.com/file/d/1rR0O7woaS7hs8nqrpYK-8NOUIEVtJM_q/view?usp=drivesdk)**

This link identifies one release artifact, not a folder containing multiple
versions. Access may require approval. Before installing, the version, filename,
source commit, file size, SHA-256, manifest, and signature status must match
[releases/current.md](releases/current.md). The ZIP SHA-256 is
`738520945882ce43cebbefebbcbc1d9614df1f8a25f4c5ab7c733e70dd263f22`.

See:

- [Current release](releases/current.md)
- [Windows installation](docs/windows-installation.md)
- [Artifact verification](docs/artifact-verification.md)
- [Known limitations](docs/limitations.md)

Linux and macOS instructions will be published only after their required
platform and Python-version matrices pass.

## Release Channels

| Channel | Audience | Status | Artifact location |
| --- | --- | --- | --- |
| Internal Preview | Approved testers | Current | Private Google Drive |
| Closed Beta | Selected design partners | Planned | Controlled Drive channel |
| Public Beta | Public evaluators | Not available | To be announced |
| Stable | Production users | Not available | To be announced |
| LTS | Long-lived production users | Not available | To be announced |

GitHub is the canonical source for documentation, release metadata,
installation guidance, qualification status, checksums, and release history. A
download is acceptable only when its identity and evidence match the current
release record.

See [release channels](releases/release-channels.md).

## Updating an Internal Preview

Internal preview builds are installed manually from a verified release artifact.
Automatic updates are not enabled for unsigned internal-preview packages.

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

For `0.2.1.dev18`:

| Target | Result |
| --- | --- |
| Windows 11 | Passed |
| Windows 10 | Qualification pending |
| Python 3.12 | Installed wheel passed |
| Python 3.11 and 3.13 | Qualification pending |
| Fresh disposable-project workflow | Passed |
| Repository identity with legacy patch bytes | Passed |
| Split preflight, pack, plan, and diff workflow | Passed |
| Read-only MCP boundary | Passed |
| Real-project feedback | Requested from approved testers |
| Backup, restore, updater, and rollback | Pending for promotion |
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
