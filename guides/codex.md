# Codex Guide

Install and verify PersistMind before connecting Codex. For the current preview,
use only a disposable or non-critical local repository.

## Codex skill

The release repository bundles a Codex-specific skill named
`persistmind-workflow`. It is for Codex users only. It is not required by Claude
Code, Gemini, Cursor, or generic MCP clients.

When PersistMind is installed from this repository with `-Agents codex`, the
installer wrapper installs or refreshes the skill in:

```powershell
$env:USERPROFILE\.codex\skills\persistmind-workflow
```

Restart Codex after installation so it can load the skill. During PersistMind
tasks, use the skill to make Codex carry the right stage information between
repo selection, preflight, task sessions, context packs, plans, checkpoints,
verification, and outcomes.

Configure Codex to start the read-only MCP command from the qualified virtual
environment:

```powershell
persistmind mcp --repo C:\absolute\path\to\repo
```

Tell Codex to inspect repository state through search, context packs, impact,
workflow recommendations, approved memory, and verification evidence. MCP does
not grant mutation authority. Perform writes through an explicitly reviewed
local CLI workflow and review the Git diff before recording an outcome.

Do not install project-local agent surfaces in the PersistMind product source
repository unless intentionally testing installer or self-hosting behavior.
