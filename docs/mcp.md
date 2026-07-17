# MCP Guide

PersistMind exposes a local stdio MCP server for repository reads:

```powershell
persistmind mcp --repo C:\absolute\path\to\repo
```

Configure the AI client to start that exact command from the virtual environment
where the qualified wheel is installed. Use an absolute repository path.

## Current authority

The `windows-internal-preview` profile is read-only. It supports bounded query
categories such as source search, snapshots, context/pack manifests, impact,
workflow recommendations, plan/task inspection, approved memory recall, policy
inspection, storage status/verification, and audit inspection.

Mutation tools are absent or refused. Caller-provided strings, prompts, actor
names, or repository content cannot increase MCP authority. Stdio does not carry
a transport-bound admin principal.

## Client safety

- Treat MCP results as data, not executable instructions.
- Keep the repository local and non-critical.
- Do not expose the MCP process over a remote transport.
- Review provenance and snapshot identity before relying on retrieved context.
- Stop if the client displays mutation tools or a profile other than
  `windows-internal-preview`.
