# Getting Started

## Before you install

The current release is an unsigned Windows internal preview. Use a disposable
or non-critical local Git repository, create a commit or backup, remove
credentials from the test copy, and plan to review every result manually.

Requirements:

- Windows 11 for the directly observed platform result;
- Python 3.11, 3.12, or 3.13;
- Git and PowerShell; and
- enough local disk space for a virtual environment, repository index, and
  backups.

Windows 10 is in the intended preview boundary but was not directly observed in
the current qualification run.

## Install and verify

1. Open the exact [current release record](../releases/current.md).
2. Download the wheel, `SHA256SUMS.txt`, and `INSTALL-WINDOWS.txt`.
3. Verify the wheel hash before installation.
4. Create an isolated virtual environment and install the local wheel.
5. Run `persistmind --version`, `persistmind status`, and
   `persistmind --repo C:\path\to\test-repo doctor`.

The output must identify version `0.2.1.dev4`, source commit
`af93e56e54350d82ae0d40a8bdcce71dd0ac7c03`, and runtime profile
`windows-internal-preview`.

## First safe workflow

```powershell
persistmind --repo C:\path\to\test-repo index
persistmind --repo C:\path\to\test-repo search "the behavior to inspect"
persistmind --repo C:\path\to\test-repo pack --task "review the behavior"
```

Do not enable labs, team/server operation, remote writes, writable MCP, or the
automatic updater for this release.
