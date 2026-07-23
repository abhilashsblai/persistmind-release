# Windows Installation

PersistMind `0.2.1.dev31` is available only to approved private internal-preview
testers. The directly qualified path is Windows 11 with Python 3.13.

`0.2.1.dev41` is also available as a newer, qualification-blocked candidate for
targeted testing. Dev31 remains the last qualified preview.

## Dev41 targeted candidate installation

Download the [exact dev41 ZIP](https://drive.google.com/file/d/16trZ7KnP6cLPlJva08YXToWy4Z_l3isf/view?usp=drivesdk).

```powershell
Get-FileHash .\PersistMind-Windows-Internal-Preview-0.2.1.dev41.zip -Algorithm SHA256
```

Expected SHA-256:
`cfef0c82dbee27cce5e76f67d66730fec2f0a1c15fd18b90cc97dad86f8a2ca9`.

Extract the archive and verify its wheel before installation:

```powershell
.\Install-PersistMind.ps1 -VerifyOnly
.\Install-PersistMind.ps1 -VenvPath C:\PersistMind\0.2.1.dev41
C:\PersistMind\0.2.1.dev41\Scripts\python.exe -I -m persistmind --version
```

If Windows has marked the extracted files as downloaded, you may remove that
file-origin mark:

```powershell
Get-ChildItem -Recurse | Unblock-File
```

This does not override enterprise Application Control. If APSW is rejected, or
if installation/`doctor` reports a degraded runtime, stop and use dev31 instead.
Do not bypass organizational policy.

Configure dev41 only in a disposable or non-critical repository:

```powershell
C:\PersistMind\0.2.1.dev41\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo install --agents codex --skip-index
C:\PersistMind\0.2.1.dev41\Scripts\python.exe -I -m persistmind --repo C:\Path\To\TestRepo doctor --summary
```

Do not use `persistmind update` for this unsigned candidate. Review the
[dev41 release record](../releases/release-notes/0.2.1.dev41.md) for the exact
qualification limitation and artifact hashes.

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
