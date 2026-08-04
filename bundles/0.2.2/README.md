# PersistMind 0.2.2 Self-Contained Windows Bundles

This directory contains hash-locked offline wheelhouses for installing
PersistMind 0.2.2 from this GitHub repository without Google Drive or a local
source-tree build cache.

## Supported Environments

| Directory | Python | Platform |
| --- | --- | --- |
| `windows-py311` | CPython 3.11 | Windows x86_64 |
| `windows-py312` | CPython 3.12 | Windows x86_64 |
| `windows-py313` | CPython 3.13 | Windows x86_64 |

Each wheelhouse includes:

- `persistmind-0.2.2-py3-none-any.whl`
- all runtime dependency wheels required for offline installation
- `dependency-lock.v1.json`
- `SHA256SUMS.txt`

## Install From A Clone

From the root of this release repository:

```powershell
.\installer\install-from-repo.ps1 `
  -Repo C:\Path\To\Project `
  -Agents codex `
  -SkipIndex
```

The wrapper detects the active Python minor version, selects the matching
wheelhouse, verifies the PersistMind wheel hash from `SHA256SUMS.txt`, creates
an isolated bootstrap environment, and configures the target project.

To force a specific Python:

```powershell
.\installer\install-from-repo.ps1 `
  -Repo C:\Path\To\Project `
  -PythonCommand C:\Path\To\Python312\python.exe `
  -Agents codex `
  -SkipIndex
```

## Verification

After install:

```powershell
$pm = "$env:LOCALAPPDATA\PersistMind\0.2.2-windows-py312\Scripts\python.exe"
& $pm -I -m persistmind --repo C:\Path\To\Project doctor --summary
& $pm -I -m persistmind --repo C:\Path\To\Project status
```

Adjust the runtime path to `py311`, `py312`, or `py313` based on the Python
minor version selected by the installer. If you pass `-BootstrapHome`, use that
path instead.

## Restrictions

These are unsigned internal diagnostic bundles. They are intended for controlled
local Windows validation in non-critical repositories only. They are not a
public beta, production release, or trusted-updater artifact.
