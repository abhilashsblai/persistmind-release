# PersistMind usage and command reference

## Install and configure a project

For a fresh installation, first follow the
[verified-install procedure](verified-install.md). Do not execute an installer
directly from a network pipe. The procedure authenticates both the installer
and the local bootstrap before either one runs.

After PersistMind is installed, configure a project with:

```text
persistmind --repo . install --agents codex,claude,cursor
```

For a new folder, add `--init-git`. Omit `--agents` to choose agents
interactively. Setup produces canonical `.persistmind` state and installs only
the native surfaces supported by each selected coding agent.

Verify the installation:

```text
persistmind --repo . doctor
persistmind --repo . storage topology
persistmind --repo . storage verify --full
```

The verified split topology contains seven databases and does not create a new
legacy `workspace.db`.

## Daily workflow

```text
persistmind --repo . workflow recommend --task "<task>"
persistmind --repo . workflow start --task "<task>"
persistmind --repo . workflow next --task-session-id <task_session_id>
```

Lower-level pack/plan/checkpoint flow:

```text
persistmind --repo . task start --task "<task>"
persistmind --repo . pack --task "<task>"
persistmind --repo . plan create --task-session-id <task_session_id> --pack-id <pack_id> --file <plan.json>
persistmind --repo . plan checkpoint <plan_id> --step-id <step_id> --path <changed_path>
git diff HEAD | persistmind --repo . check-diff --pack-id <pack_id>
git diff --name-only HEAD | persistmind --repo . impact --paths-from-stdin
persistmind --repo . outcome --pack-id <pack_id> --result pass --summary "<summary>"
```

## Health and maintenance

```text
persistmind --repo . doctor
persistmind --repo . index
persistmind --repo . storage-report
persistmind --repo . retention show
persistmind --repo . gc --deep
persistmind --repo . maintenance history
```

## Memory and learning

```text
persistmind --repo . memory candidates
persistmind --repo . memory list
persistmind --repo . learning status
persistmind --repo . cie status
```

## MCP

```text
persistmind --repo . mcp
```

Generated MCP snippets live under `.persistmind/mcp/`. Review project-local
configuration before sharing it with a team.

## Update

```text
persistmind update --check
persistmind update
persistmind update --rollback
```

## Uninstall

Dry run:

```text
python uninstall_persistmind.py --project .
```

Execute:

```text
python uninstall_persistmind.py --project . --execute --yes
```

The cleanup supports canonical and legacy installations and protects source
checkouts and user-modified files.
