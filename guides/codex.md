# Codex Guide

Install and verify PersistMind before connecting Codex. For the current preview,
use only a disposable or non-critical local repository.

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
