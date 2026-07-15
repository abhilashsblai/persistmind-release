# PersistMind

> Persistent project intelligence for AI engineering.

PersistMind gives AI coding agents durable repository memory, context packs,
impact analysis, governed workflows, hooks, skills, MCP tools, and a verified
seven-database local storage topology.

It works with Codex, Claude Code, Cursor, MCP-compatible clients, and other
coding agents. The core is local-first and does not require Node.js; Node is
used only by the optional npm wrapper.

## Verified fresh installation

The installer creates an isolated environment, verifies the signed manifest and
wheel, creates all seven databases, configures selected coding agents, and runs
verification. A fresh machine must first authenticate the release assets using
an independently installed official GitHub CLI. A pristine `GH_CONFIG_DIR` is
not authenticated automatically; run `gh auth login` or provide a short-lived
fine-grained `GH_TOKEN` with read-only Metadata, Contents, and Attestations
permissions for both the source and release repositories.

Follow the complete [verified-install procedure](docs/verified-install.md).
It verifies release immutability, release-asset membership, source workflow
provenance, tag, source commit, issuer, runner class, and asset digests
before executing either the installer or bootstrap. Verification, download,
and execution remain separate commands; never pipe downloaded code to a shell.

Releases published before this contract do not satisfy it retroactively.

After the staged procedure has verified both local files, non-interactive agent
selection is available without weakening the bootstrap binding:

```powershell
./install-persistmind.ps1 -Repo C:\path\to\project -Version v0.2.0a23 -BootstrapPath .\bootstrap_persistmind.py -Agents "codex,claude,cursor"
```

```bash
./install-persistmind.sh --repo /path/to/project --version v0.2.0a23 --bootstrap-path ./bootstrap_persistmind.py --agents codex,claude,cursor
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
