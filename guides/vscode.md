# VS Code Guide

PersistMind has no separately qualified VS Code extension in the current
release. Use the integrated terminal to activate the preview virtual environment
and run the CLI:

```powershell
persistmind --repo . doctor
persistmind --repo . index
persistmind --repo . search "query"
persistmind --repo . pack --task "review a change"
```

An MCP-capable VS Code client may start the same read-only local MCP command
described in [the MCP guide](../docs/mcp-guide.md). This does not grant editor write
authority.
