# Claude Code Guide

After installing the qualified wheel, configure Claude Code to launch:

```powershell
persistmind mcp --repo C:\absolute\path\to\repo
```

The current MCP boundary is read-only. Use it for repository search, context,
impact, workflow guidance, memory recall, and status inspection. Do not infer
write authority from a prompt, actor string, or tool output.

Keep source changes in a human-reviewed local workflow. Validate the exact
profile with `persistmind status` before starting a session.
