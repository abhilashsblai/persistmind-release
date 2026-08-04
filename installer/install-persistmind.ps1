# PersistMind release installer for Windows.
# For a fresh install, execute this only after following the staged verification guide.
[CmdletBinding()]
param(
    [string]$Repo = ".",
    [string]$Agents = "",
    [ValidateSet("stable", "preview")][string]$Channel = "stable",
    [string]$Version = "",
    [string]$BootstrapPath = "",
    [string]$BootstrapUrl = "",
    [string]$BootstrapSha256 = "",
    [string]$ManifestUrl = "",
    [string]$ManifestSignatureUrl = "",
    [string]$LocalWheelPath = "",
    [string]$LocalWheelSha256 = "",
    [switch]$InitGit,
    [switch]$SkipIndex,
    [switch]$Reinstall
)

$ErrorActionPreference = "Stop"

function Test-CompatiblePython {
    param([string]$Command)
    if (-not $Command) { return $false }
    try {
        & $Command -c "import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)" 2>$null
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
    $usingLocalWheel = [bool]($LocalWheelPath -or $LocalWheelSha256)
    if (-not $BootstrapPath) {
        if (-not $BootstrapUrl -or -not $BootstrapSha256) {
            throw "Provide -BootstrapPath, or the GitHub release -BootstrapUrl and -BootstrapSha256 from the qualified release."
        }
        if ($BootstrapUrl -notmatch '^https://(github\.com|drive\.google\.com|drive\.usercontent\.google\.com|docs\.googleusercontent\.com)/') {
            throw "The bootstrap URL must be hosted on GitHub Releases or Google Drive."
        }
        if ($BootstrapSha256 -notmatch '^[0-9a-fA-F]{64}$') { throw "Bootstrap SHA-256 is invalid." }
        $temporaryDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("persistmind-release-artifacts-" + [guid]::NewGuid().ToString("N"))
        New-Item -ItemType Directory -Path $temporaryDirectory | Out-Null
        $BootstrapPath = Join-Path $temporaryDirectory "bootstrap_persistmind.py"
        Invoke-WebRequest -Uri $BootstrapUrl -OutFile $BootstrapPath -MaximumRedirection 8
        $actualBootstrapHash = (Get-FileHash -LiteralPath $BootstrapPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualBootstrapHash -ne $BootstrapSha256.ToLowerInvariant()) {
            throw "Bootstrap download failed SHA-256 verification."
        }
    }
    if ([bool]$LocalWheelPath -ne [bool]$LocalWheelSha256) {
        throw "-LocalWheelPath and -LocalWheelSha256 must be supplied together."
    }
    if ($usingLocalWheel -and (-not $BootstrapPath -or -not $Version)) {
        throw "Local artifact testing requires -BootstrapPath and the exact -Version."
    }
    if (-not $usingLocalWheel -and (-not $ManifestUrl -or -not $ManifestSignatureUrl)) {
        throw "Release installation requires -ManifestUrl and -ManifestSignatureUrl."
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
    if ($ManifestUrl) { $arguments += @("--manifest-url", $ManifestUrl) }
    if ($ManifestSignatureUrl) {
        $arguments += @("--manifest-signature-url", $ManifestSignatureUrl)
    }
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
