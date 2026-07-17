# Windows Installation

PersistMind `0.2.1.dev4` is available only to approved private internal-preview
testers. Access to the version-specific Drive folder is provided separately.

## Requirements

- Windows 11 for the directly qualified platform result;
- Windows 10 only as a pending qualification target;
- Python 3.11, 3.12, or 3.13;
- Git and PowerShell; and
- a disposable or non-critical local repository.

## Verify before installation

Compare the artifact with [releases/current.md](../releases/current.md), then
calculate SHA-256:

```powershell
Get-FileHash C:\Path\To\persistmind-0.2.1.dev4-py3-none-any.whl -Algorithm SHA256
```

Expected wheel SHA-256:
`e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad`.

## Install into an isolated environment

```powershell
py -3.12 -m venv C:\PersistMindTest\venv
C:\PersistMindTest\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install C:\Path\To\persistmind-0.2.1.dev4-py3-none-any.whl
persistmind --version
persistmind status
persistmind --repo C:\Path\To\TestRepo doctor
```

The output must identify version `0.2.1.dev4`, commit
`af93e56e54350d82ae0d40a8bdcce71dd0ac7c03`, and profile
`windows-internal-preview`.

Install outside the source checkout and ensure `PYTHONPATH` cannot satisfy
imports accidentally. Do not use the automatic updater for this unsigned
preview.

Linux and macOS installation instructions are intentionally unpublished until
their qualification matrices pass.
