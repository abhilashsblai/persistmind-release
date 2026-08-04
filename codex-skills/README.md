# PersistMind Codex Skills

This directory contains Codex-specific skills bundled with the PersistMind
release repository. They are for Codex users; they are not Claude Code, Gemini,
Cursor, or generic MCP instructions.

## PersistMind Workflow

`persistmind-workflow` teaches Codex to carry the right PersistMind stage
information between repository selection, preflight, plans, checkpoints,
verification, and outcomes.

When a new user installs PersistMind into a project with the repository wrapper
and includes Codex in the selected agents, the wrapper installs or refreshes the
skill at:

```powershell
$env:USERPROFILE\.codex\skills\persistmind-workflow
```

Manual install:

```powershell
Copy-Item -Recurse .\codex-skills\persistmind-workflow "$env:USERPROFILE\.codex\skills\persistmind-workflow" -Force
```

The skill does not install PersistMind and does not modify project files by
itself. It only gives Codex the workflow contract to use after PersistMind is
installed in a target project.
