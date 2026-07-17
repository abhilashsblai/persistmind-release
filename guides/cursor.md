# Cursor Guide

Cursor can consume the local read-only MCP process:

```powershell
persistmind mcp --repo C:\absolute\path\to\repo
```

Point the client configuration at the executable inside the qualified virtual
environment. Use an absolute repository path. The current release does not
claim lifecycle-hook, subagent, autonomous mutation, or writable-MCP support in
Cursor.

Review retrieved provenance and every resulting source diff manually.
