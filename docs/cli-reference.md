# CLI Reference

This page lists the command families qualified for the current internal preview.
Run `persistmind --help` and `<command> --help` for the exact arguments shipped
in the installed wheel. A command being present does not make it supported by
this release profile.

## Identity and health

```powershell
persistmind --version
persistmind status
persistmind --repo . doctor
```

## Source intelligence

```powershell
persistmind --repo . index
persistmind --repo . search "query"
persistmind --repo . pack --task "task description" --seed-path path\to\file.py --budget 2000
persistmind --repo . manifest --pack-id <pack-id>
```

Indexing is explicit. Pack generation must not silently grant write authority or
trigger an unbounded repository scan.

## Workflow

```powershell
persistmind --repo . task start --task "task description"
persistmind --repo . plan create --task-session-id <id> --file plan.json
persistmind --repo . workflow recommend --task "task description" --path path\to\file.py
persistmind --repo . workflow start --task "task description" --path path\to\file.py
persistmind --repo . workflow next --task-session-id <id>
persistmind --repo . verify run --command "python -m pytest -q"
```

The workflow tracks plans, checkpoints, scope, verification, outcomes, and
continuation evidence. Manual review remains mandatory.

## Storage and recovery

```powershell
persistmind --repo . storage status
persistmind --repo . storage topology
persistmind --repo . storage verify --full
persistmind --repo . storage backup create --verify
persistmind --repo . storage backup verify --backup <backup-id>
persistmind --repo . storage backup restore --backup <backup-id> --target <empty-path> --yes
```

Restore only into a clean target and verify it before replacing any live state.

## MCP

```powershell
persistmind mcp --repo C:\absolute\path\to\repo
```

The current profile exposes read-only stdio MCP. See [MCP guide](mcp-guide.md).

## Outside the qualified boundary

Remote/team servers, writable MCP, automatic updating, labs, autonomous source
modification, and advanced intelligence promotion are not supported by
`0.2.1.dev31`, even if a help surface exists.
