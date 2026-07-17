# Installation

## Windows internal preview

The authoritative commands are bundled in
[`INSTALL-WINDOWS.txt`](https://drive.google.com/file/d/1CDpY7GIAZRpYnsxNrwAKa3BH-1mlh20O/view).
The abbreviated process is:

```powershell
py -3.12 -m venv C:\PersistMindTest\venv
C:\PersistMindTest\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
Get-FileHash C:\Path\To\persistmind-0.2.1.dev4-py3-none-any.whl -Algorithm SHA256
python -m pip install C:\Path\To\persistmind-0.2.1.dev4-py3-none-any.whl
persistmind --version
persistmind status
persistmind --repo C:\Path\To\TestRepo doctor
```

Expected wheel SHA-256:
`e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad`.

Install from a directory outside the source checkout. Do not let an editable
checkout or `PYTHONPATH` satisfy runtime imports.

## Linux and macOS

There is no qualified Linux or macOS artifact in the current release. Do not
infer support from a platform-independent wheel filename.

## Uninstall

Uninstall the Python package from its isolated environment with:

```powershell
python -m pip uninstall persistmind
```

Package uninstall must not be treated as permission to delete repository source
or user data. Review and back up `.persistmind` before any explicit data cleanup.
