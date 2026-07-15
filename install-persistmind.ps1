# PersistMind release installer for Windows.
# For a fresh install, execute this only after following the staged verification guide.
[CmdletBinding()]
param(
    [string]$Repo = ".",
    [string]$Agents = "",
    [ValidateSet("stable", "preview")][string]$Channel = "stable",
    [string]$Version = "",
    [string]$BootstrapPath = "",
    [string]$LocalWheelPath = "",
    [string]$LocalWheelSha256 = "",
    [switch]$InitGit,
    [switch]$SkipIndex,
    [switch]$Reinstall
)

$ErrorActionPreference = "Stop"
$driveArtifactVersion = "0.2.0a24"
$driveBootstrapUrl = "https://drive.usercontent.google.com/download?id=1PppMk20fKrsw8lmGlkyHwmbnRAkZG9fd&export=download&confirm=t"
$driveBootstrapSha256 = "6a23c71dc737e66ba5e940453bc86e3d27295ab3aa9ae30867bfa107aeba84e0"
$driveWheelUrl = "https://drive.usercontent.google.com/download?id=1qxQK9uaEb2medjGFNMrLzZU2KzjbJDuW&export=download&confirm=t"
$driveWheelSha256 = "2f8a68bd22c3d797df1a4941991b8de5414137722cb76f70b29c9f6efcfc2b02"

function Test-CompatiblePython {
    param([string]$Command)
    if (-not $Command) { return $false }
    try {
        & $Command -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>$null
        return $LASTEXITCODE -eq 0
    } catch { return $false }
}

function Find-CompatiblePython {
    $names = @($env:PERSISTMIND_PYTHON, "python", "python3")
    foreach ($name in $names) {
        if (-not $name) { continue }
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if ($command -and (Test-CompatiblePython $command.Source)) { return $command.Source }
    }
    $roots = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python"),
        (Join-Path $env:ProgramFiles "Python")
    )
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        foreach ($candidate in Get-ChildItem -LiteralPath $root -Filter python.exe -Recurse -ErrorAction SilentlyContinue) {
            if (Test-CompatiblePython $candidate.FullName) { return $candidate.FullName }
        }
    }
    return $null
}

function Assert-Sha256 {
    param(
        [string]$Path,
        [string]$Expected,
        [string]$Label
    )
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($actual -ne $Expected.ToLowerInvariant()) {
        throw "$Label SHA-256 mismatch. Expected $Expected, got $actual."
    }
}

$python = Find-CompatiblePython
if (-not $python) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "Python 3.11+ is required and winget is unavailable. Install Python 3.11+ and rerun this command."
    }
    Write-Host "persistmind-install: installing Python 3.13 for the current user"
    & $winget.Source install --id Python.Python.3.13 --exact --scope user --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget could not install Python 3.13" }
    $python = Find-CompatiblePython
    if (-not $python) { throw "Python was installed but could not be located; open a new shell and rerun." }
}

$temporaryDirectory = $null
$bootstrap = $null
try {
    $usingLocalArtifacts = [bool]($BootstrapPath -or $LocalWheelPath -or $LocalWheelSha256)
    if (-not $usingLocalArtifacts) {
        if ($Version -and $Version.TrimStart("v") -ne $driveArtifactVersion) {
            throw "Google Drive is pinned to PersistMind $driveArtifactVersion."
        }
        $Version = $driveArtifactVersion
        $temporaryDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("persistmind-drive-artifacts-" + [guid]::NewGuid().ToString("N"))
        New-Item -ItemType Directory -Path $temporaryDirectory | Out-Null
        $BootstrapPath = Join-Path $temporaryDirectory "bootstrap_persistmind.py"
        $LocalWheelPath = Join-Path $temporaryDirectory "persistmind-$driveArtifactVersion-py3-none-any.whl"
        $LocalWheelSha256 = $driveWheelSha256

        Write-Host "persistmind-install: downloading checksum-pinned Google Drive artifacts"
        Invoke-WebRequest -Uri $driveBootstrapUrl -OutFile $BootstrapPath -UseBasicParsing
        Assert-Sha256 -Path $BootstrapPath -Expected $driveBootstrapSha256 -Label "Bootstrap"
        Invoke-WebRequest -Uri $driveWheelUrl -OutFile $LocalWheelPath -UseBasicParsing
        Assert-Sha256 -Path $LocalWheelPath -Expected $driveWheelSha256 -Label "Wheel"
    }
    if ([bool]$LocalWheelPath -ne [bool]$LocalWheelSha256) {
        throw "-LocalWheelPath and -LocalWheelSha256 must be supplied together."
    }
    if ($usingLocalArtifacts -and (-not $BootstrapPath -or -not $LocalWheelPath -or -not $LocalWheelSha256 -or -not $Version)) {
        throw "Local artifact testing requires -BootstrapPath, -LocalWheelPath, -LocalWheelSha256, and the exact -Version."
    }
    $bootstrap = (Resolve-Path -LiteralPath $BootstrapPath).Path
    if (-not (Test-Path -LiteralPath $Repo)) {
        if (-not $InitGit) {
            throw "Repository path does not exist. Create it first or pass -InitGit: $Repo"
        }
        New-Item -ItemType Directory -Path $Repo -Force | Out-Null
    }
    $resolvedRepo = (Resolve-Path -LiteralPath $Repo).Path
    $arguments = @("-I", $bootstrap, "--repo", $resolvedRepo, "--channel", $Channel)
    if ($Agents) { $arguments += @("--agents", $Agents) }
    if ($Version) { $arguments += @("--version", $Version) }
    if ($LocalWheelPath) {
        $arguments += @(
            "--local-wheel", (Resolve-Path -LiteralPath $LocalWheelPath).Path,
            "--local-wheel-sha256", $LocalWheelSha256
        )
    }
    if ($InitGit) { $arguments += "--init-git" }
    if ($SkipIndex) { $arguments += "--skip-index" }
    if ($Reinstall) { $arguments += "--reinstall" }
    & $python @arguments
    if ($LASTEXITCODE -ne 0) { throw "PersistMind installation failed with exit code $LASTEXITCODE" }
} finally {
    if ($temporaryDirectory) { Remove-Item -LiteralPath $temporaryDirectory -Recurse -Force -ErrorAction SilentlyContinue }
}

Write-Host "persistmind-install: complete. Open a new shell if 'persistmind' is not yet on PATH."
