# Troubleshooting

## Identity does not match

Run:

```powershell
persistmind --version
persistmind status
persistmind --repo C:\path\to\repo doctor
```

Stop if the version, source commit, or runtime profile differs from
[releases/current.md](../releases/current.md). Check that the intended virtual
environment is active and that `PYTHONPATH` is not importing a checkout.

## PowerShell blocks activation

Use an execution policy approved by the machine owner, or invoke the virtual
environment's Python executable directly. Do not bypass organizational policy.

## Installation or dependency failure

Confirm Python is 3.11-3.13, upgrade pip inside the isolated environment, and
install the wheel from a local path. Record the complete redacted pip error.

## Indexing failure

Check repository permissions, available disk space, long or locked paths, and
antivirus activity. Retry only after confirming no active PersistMind process is
using the repository state. Preserve `.persistmind` before remediation.

## SQLite or storage warning

Run `persistmind --repo . storage status` and
`persistmind --repo . storage verify --full`. Do not delete or replace database
files manually. Create a verified backup before attempting recovery.

## MCP connection failure

Confirm the client starts `persistmind mcp --repo <absolute-path>` using the
same virtual environment. The current server is stdio and read-only. A request
for a mutation tool should fail or find no such tool.

## Updater rejects the release

This is expected for the unsigned internal preview. Install it manually; do not
weaken signature or manifest verification.

## Reporting an issue

Follow [SUPPORT.md](../SUPPORT.md). Redact credentials, private source, private
paths, and database contents.
