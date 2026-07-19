# Windows Installation

PersistMind `0.2.1.dev31` is available only to approved private internal-preview
testers. The directly qualified path is Windows 11 with Python 3.13.

## Download and verify

Download the [exact qualified ZIP](https://drive.google.com/file/d/1oCQN8stUdmeHvUQsO7tk-kKUqdd65A8s/view?usp=drivesdk).

```powershell
Get-FileHash .\PersistMind-Windows-Internal-Preview-0.2.1.dev31.zip -Algorithm SHA256
```

Expected ZIP SHA-256:
`013ce8741201abd5ae8640f0bce3d7f47cb8d3d5310f8e18c64a779fa0bc9f24`.

Extract it and verify the wheel:

```powershell
.\Install-PersistMind.ps1 -VerifyOnly
```

## Install into an isolated environment

From the extracted directory:

```powershell
.\Install-PersistMind.ps1 -VenvPath C:\PersistMind\0.2.1.dev31
C:\PersistMind\0.2.1.dev31\Scripts\python.exe -I -m persistmind --version
```

The installer refuses to replace an existing environment. A `uv` installation
can supply Python 3.13 if the `py` launcher cannot. An absolute interpreter may
also be provided with `-PythonCommand`.

## Configure a project

Commit or back up the repository first:

```powershell
C:\PersistMind\0.2.1.dev31\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo setup codex --install-hooks --configure-mcp --absolute-mcp-repo
C:\PersistMind\0.2.1.dev31\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo doctor --summary
```

Review all generated files and restart the agent after reviewing MCP
configuration. Do not use the automatic updater for this unsigned preview.

Linux and macOS installation instructions are intentionally unpublished until
their qualification matrices pass.
