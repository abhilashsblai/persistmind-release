# Windows Installation

PersistMind `0.2.2.dev1` is an unsigned internal preview qualified on Windows 11
with CPython 3.12. Use it only in a non-critical local repository.

## Download and verify

Download the [exact preview ZIP](https://drive.google.com/file/d/1MAQKcVNRBeUnd8LeMv2GbRHLD4dd8mzk/view?usp=drivesdk).

```powershell
Get-FileHash .\PersistMind-Windows-Internal-Preview-0.2.2.dev1.zip -Algorithm SHA256
```

Expected SHA-256:
`26aba71a82beb992628cc81c309a535af280db17ab118402ef2ffd0fe3bce9f4`.

Extract the archive, then verify and install into a new isolated environment:

```powershell
.\Install-PersistMind.ps1 -VerifyOnly
.\Install-PersistMind.ps1 -VenvPath D:\PersistMind\0.2.2.dev1
D:\PersistMind\0.2.2.dev1\Scripts\python.exe -I -m persistmind --version
```

The installer refuses to replace an existing environment. If the Python
launcher cannot resolve Python 3.12, pass an absolute interpreter with
`-PythonCommand`.

## Configure Codex in a project

Commit or back up the repository first, then run:

```powershell
$pm = 'D:\PersistMind\0.2.2.dev1\Scripts\python.exe'
& $pm -I -m persistmind --repo C:\Path\To\Repository install `
  --agents codex `
  --mcp-command $pm `
  --install-hooks `
  --configure-mcp `
  --absolute-mcp-repo `
  --skip-index
& $pm -I -m persistmind --repo C:\Path\To\Repository doctor --summary
```

Review generated files and restart Codex so the project-local hooks and MCP
configuration load. Keep `PERSISTMIND_HOME` on local storage; do not use Google
Drive for live databases, indexes, WALs, or runtime state.

Do not use `persistmind update` for this unsigned preview. Windows 10,
CPython 3.11/3.13, Linux, and macOS are not qualified for this candidate.
