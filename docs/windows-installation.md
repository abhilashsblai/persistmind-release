# Windows Installation

PersistMind `0.2.1.dev19` is available only to approved private internal-preview
testers. The directly qualified path is Windows 11 with Python 3.12.

## Download and verify

Download the [exact qualified ZIP](https://drive.google.com/file/d/1WiT3UrMXEb_T4FTbIxHzuwnU-gWHKPju/view?usp=drivesdk).

```powershell
Get-FileHash .\PersistMind-Windows-Internal-Preview-0.2.1.dev19.zip -Algorithm SHA256
```

Expected ZIP SHA-256:
`e397e87e83453e9ffb94d650f0ee29d44db8690347ce071d81b54240e5cd15cf`.

Extract it and verify the wheel:

```powershell
.\Install-PersistMind.ps1 -VerifyOnly
```

## Install into an isolated environment

From the extracted directory:

```powershell
.\Install-PersistMind.ps1 -VenvPath C:\PersistMind\0.2.1.dev19
C:\PersistMind\0.2.1.dev19\Scripts\python.exe -I -m persistmind --version
```

The installer refuses to replace an existing environment. A `uv` installation
can supply Python 3.12 if the `py` launcher cannot. An absolute interpreter may
also be provided with `-PythonCommand`.

## Configure a project

Commit or back up the repository first:

```powershell
C:\PersistMind\0.2.1.dev19\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo setup codex --install-hooks --configure-mcp --absolute-mcp-repo
C:\PersistMind\0.2.1.dev19\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo doctor --summary
```

Review all generated files and restart the agent after reviewing MCP
configuration. Do not use the automatic updater for this unsigned preview.

Linux and macOS installation instructions are intentionally unpublished until
their qualification matrices pass.
