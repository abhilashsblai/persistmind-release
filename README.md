# PersistMind

> Persistent project intelligence for AI engineering.

PersistMind gives AI coding agents durable repository memory, context packs,
impact analysis, governed workflows, hooks, skills, MCP tools, and a verified
seven-database local storage topology.

It works with Codex, Claude Code, Cursor, MCP-compatible clients, and other
coding agents. The core is local-first and does not require Node.js; Node is
used only by the optional npm wrapper.

## Private Windows internal preview

PersistMind `0.2.1.dev4` is available as an **unsigned, private Windows-only
internal preview** for non-critical local repositories and manual human review.
It is not a public beta, production release, or trusted-updater artifact.

- [Internal preview files on Google Drive](https://drive.google.com/drive/folders/1HT9bAsR4S9D1bmJ8MtaX9GiweuHK77U1)
- [Release notes, checksums, qualification, and restrictions](docs/releases/persistmind-0.2.1.dev4-windows-internal-preview.md)

Installer and wheel bytes remain exclusively on Google Drive. This repository
contains only the release record and links.

## Verified fresh installation

The installer creates an isolated environment, verifies the bootstrap and
wheel, creates all seven databases, configures selected coding agents, and runs
verification. Public installation artifacts are always stored in the
[PersistMind Releases Google Drive folder](https://drive.google.com/drive/folders/1aOOJ7fEE9Bv8yS-jzFVvTuBwlx0q7Nz9).
GitHub stores source code, checksums, documentation, and commit history; the
installer does not fall back to GitHub release assets.

### Google Drive installation (Windows)

Download and review
[`install-persistmind.ps1`](https://drive.google.com/file/d/16OChpEU4pVR4OgmmhxddXP511t6uAmcc/view),
then run:

```powershell
.\install-persistmind.ps1 -Repo C:\path\to\project -Agents codex -InitGit
```

Use `-SkipIndex` only when you want PersistMind to build the source index on the
first workflow request. The installer downloads the public bootstrap and wheel
from Google Drive to a temporary directory, verifies both SHA-256 values before
execution, and removes the temporary files afterward. The installer SHA-256 is
`5870b4076c0f6258d241b80baebda7d9863ad62fb8f8f8277f55e92585d41da4`, the pinned
bootstrap SHA-256 is
`6a23c71dc737e66ba5e940453bc86e3d27295ab3aa9ae30867bfa107aeba84e0` and the
wheel SHA-256 is
`39e23e6cfc077ac1677a9af4c6b933fcf44739080437e9d0a35050a614662d14`.

Every new public version must be uploaded beneath the public Drive release
folder and pinned by file ID and SHA-256 in the installer before publication.
The legacy GitHub attestation workflow is documented separately for historical
releases and source provenance.

For explicit developer qualification with local artifacts, supply all local
inputs and the exact version together:

```powershell
./install-persistmind.ps1 -Repo C:\path\to\project -Version <tag> -BootstrapPath .\bootstrap_persistmind.py -LocalWheelPath .\persistmind.whl -LocalWheelSha256 <sha256> -Agents "codex,claude,cursor"
```

```bash
./install-persistmind.sh --repo /path/to/project --version <tag> --bootstrap-path ./bootstrap_persistmind.py --agents codex,claude,cursor
```

If the package is already installed:

```text
persistmind --repo . install --agents codex,claude,cursor
```

The install transaction writes its ownership inventory to
`.persistmind/installation.json`. Existing project source code is never treated
as an owned PersistMind file.

## Update

Run from an installed project:

```text
persistmind update
```

Useful controls:

```text
persistmind update --check
persistmind update --dry-run
persistmind update --channel stable
persistmind update --channel preview
persistmind update --rollback
persistmind update status
```

The updater verifies the release, prepares an immutable engine slot, backs up
project state, migrates legacy state when required, performs the cutover, and
rolls back automatically if post-cutover verification fails.

## Uninstall and start fresh

Download `uninstall_persistmind.py` from the selected release. The default is a
read-only dry run:

```text
python uninstall_persistmind.py --project .
```

After reviewing the plan, execute it:

```text
python uninstall_persistmind.py --project . --execute --yes
```

Discover multiple installations under a folder:

```text
python uninstall_persistmind.py --search-root C:\codes --execute --yes
```

The uninstaller removes both PersistMind and legacy CTX Layer state, databases,
generated agent hooks/skills/rules, MCP entries, Git hooks owned by the product,
keyring credentials, global updater caches, and Python/npm packages. It uses the
installation manifest to restore pre-existing files where possible and preserves
user-modified or unowned files for review.

Product source checkouts are detected and preserved: the cleanup removes local
`.persistmind`/`.ctxlayer` runtime state but does not remove source code,
release scripts, tests, or files needed to build and publish a new release.

Options:

- `--memory-only`: remove memory/state but keep agent surfaces and packages.
- `--keep-global`: retain machine registry, updater slots, and global memory.
- `--keep-packages`: retain Python and npm packages.
- `--include-external-paths`: also remove explicitly configured state outside
  the project root.

## Where files are stored

Project-local state defaults to `.persistmind/`. Machine state defaults to
`%APPDATA%\PersistMind` on Windows and `~/.persistmind` on macOS/Linux.
`PERSISTMIND_HOME` overrides the machine location.

Agent configuration may include:

- `AGENTS.md`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/agents/`
- `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`
- `.cursor/mcp.json`, `.cursor/rules/persistmind.mdc`
- `.mcp.json`, `persistmind.capabilities.yaml`, and local Git hooks

Legacy `.ctxlayer`, `ctxlayer.toml`, `ctxlayer.capabilities.yaml`, `ctxlayer`
CLI, and old MCP/keyring identifiers are recognized during the compatibility
window and migrated without discarding project memory.

## Requirements and safety

- Python 3.11 or newer (the platform installer can provision it)
- Git
- Node.js only for the optional `@persistmind/cli` wrapper

PersistMind is a governance aid, not a substitute for human review on security,
regulated, destructive, or production-critical work.

## Documentation

- [Usage and command reference](docs/usage.md)
- [Release history](docs/releases/)
- [License](LICENSE)

Copyright (c) 2026 Abhilash Pillai. All rights reserved.
