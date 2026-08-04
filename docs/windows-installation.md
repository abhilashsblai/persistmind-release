# Windows Installation

PersistMind `0.2.2` is available in this repository as unsigned internal
diagnostic wheelhouses for Windows x86_64 and CPython 3.11, 3.12, and 3.13.
Use it only in non-critical local repositories.

## Install from this GitHub repository

Clone the release repository, then run the repository-local installer wrapper:

```powershell
git clone https://github.com/abhilashsblai/persistmind-release.git
cd persistmind-release
.\installer\install-from-repo.ps1 `
  -Repo C:\Path\To\Repository `
  -Agents codex `
  -SkipIndex
```

The wrapper selects the matching wheelhouse from `bundles/0.2.2/windows-py311`,
`windows-py312`, or `windows-py313`, verifies the PersistMind wheel hash from
`SHA256SUMS.txt`, installs into an isolated bootstrap environment, and
configures the target project.

To force a Python interpreter or runtime location:

```powershell
.\installer\install-from-repo.ps1 `
  -Repo C:\Path\To\Repository `
  -PythonCommand C:\Path\To\Python312\python.exe `
  -BootstrapHome D:\PersistMind\0.2.2-windows-py312 `
  -Agents codex `
  -SkipIndex
```

## Configure Codex in a project

Commit or back up the repository first, then verify:

```powershell
$pm = "$env:LOCALAPPDATA\PersistMind\0.2.2-windows-py312\Scripts\python.exe"
& $pm -I -m persistmind --repo C:\Path\To\Repository doctor --summary
& $pm -I -m persistmind --repo C:\Path\To\Repository status
```

Review generated files and restart Codex so the project-local hooks and MCP
configuration load. Keep `PERSISTMIND_HOME` on local storage; do not use Google
Drive for live databases, indexes, WALs, or runtime state.

Do not use `persistmind update` for this unsigned diagnostic package. Linux and
macOS are not qualified for this candidate.

## Historical internal preview ZIP

The older `0.2.2.dev1` internal preview ZIP remains documented in
`releases/current.md` for approved testers and traceability. New clean-machine
validation should prefer the self-contained GitHub wheelhouses above unless a
specific test requires the historical Drive artifact.
