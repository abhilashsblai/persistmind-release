# Install PersistMind from the self-contained wheelhouses committed in this
# release repository.
[CmdletBinding()]
param(
    [string]$Repo = ".",
    [string]$Agents = "codex",
    [string]$PythonCommand = "",
    [string]$BootstrapHome = "",
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
    } catch {
        return $false
    }
}

function Get-PythonMinor {
    param([string]$Command)
    $minor = & $Command -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')" 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $minor) {
        throw "Unable to determine Python version for: $Command"
    }
    return [string]$minor
}

function Find-CompatiblePython {
    $names = @($PythonCommand, $env:PERSISTMIND_PYTHON, "python", "python3")
    foreach ($name in $names) {
        if (-not $name) { continue }
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if ($command -and (Test-CompatiblePython $command.Source)) { return $command.Source }
        if ((Test-Path -LiteralPath $name -PathType Leaf) -and (Test-CompatiblePython $name)) {
            return (Resolve-Path -LiteralPath $name).Path
        }
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
    throw "Python 3.11, 3.12, or 3.13 is required. Install Python first or pass -PythonCommand."
}

function Test-AgentSelected {
    param(
        [string]$AgentList,
        [string]$AgentName
    )
    if (-not $AgentList) { return $false }
    $names = $AgentList -split "," | ForEach-Object { $_.Trim().ToLowerInvariant() }
    return $names -contains $AgentName.ToLowerInvariant()
}

function Install-CodexWorkflowSkill {
    param([string]$ReleaseRoot)
    $source = Join-Path $ReleaseRoot "codex-skills\persistmind-workflow"
    if (-not (Test-Path -LiteralPath $source -PathType Container)) {
        Write-Warning "persistmind-install: Codex workflow skill not found at $source"
        return
    }
    if (-not $env:USERPROFILE) {
        Write-Warning "persistmind-install: USERPROFILE is not set; skipping Codex skill install"
        return
    }
    $skillsRoot = Join-Path $env:USERPROFILE ".codex\skills"
    $target = Join-Path $skillsRoot "persistmind-workflow"
    New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "persistmind-install: installed Codex skill persistmind-workflow to $target"
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$releaseRoot = Resolve-Path -LiteralPath (Join-Path $scriptRoot "..")
$python = Find-CompatiblePython
$minor = Get-PythonMinor $python
$bundle = Join-Path $releaseRoot "bundles\0.2.2\windows-py$minor"
if (-not (Test-Path -LiteralPath $bundle -PathType Container)) {
    throw "No committed PersistMind wheelhouse exists for Python $minor at $bundle"
}

$wheel = Join-Path $bundle "persistmind-0.2.2-py3-none-any.whl"
$sums = Join-Path $bundle "SHA256SUMS.txt"
if (-not (Test-Path -LiteralPath $wheel -PathType Leaf)) {
    throw "PersistMind wheel is missing: $wheel"
}
if (-not (Test-Path -LiteralPath $sums -PathType Leaf)) {
    throw "SHA256SUMS.txt is missing: $sums"
}

$wheelName = Split-Path -Leaf $wheel
$expectedHash = $null
foreach ($line in Get-Content -LiteralPath $sums) {
    $parts = $line -split "\s+", 2
    if ($parts.Count -eq 2 -and $parts[1].Trim() -eq $wheelName -and $parts[0] -match "^[0-9a-fA-F]{64}$") {
        $expectedHash = $parts[0].ToLowerInvariant()
        break
    }
}
if (-not $expectedHash) {
    throw "SHA256SUMS.txt does not contain an entry for $wheelName"
}

$actualHash = (Get-FileHash -LiteralPath $wheel -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $expectedHash) {
    throw "PersistMind wheel hash mismatch. Expected $expectedHash but found $actualHash"
}

if (-not $BootstrapHome) {
    $BootstrapHome = Join-Path $env:LOCALAPPDATA "PersistMind\0.2.2-windows-py$minor"
}

$env:PERSISTMIND_PYTHON = $python
$env:PERSISTMIND_BOOTSTRAP_HOME = $BootstrapHome
$installer = Join-Path $scriptRoot "install-persistmind.ps1"
$bootstrap = Join-Path $scriptRoot "bootstrap_persistmind.py"

$parameters = @{
    Repo = $Repo
    Agents = $Agents
    Channel = "preview"
    Version = "0.2.2"
    BootstrapPath = $bootstrap
    LocalWheelPath = $wheel
    LocalWheelSha256 = $expectedHash
}
if ($SkipIndex) { $parameters.SkipIndex = $true }
if ($Reinstall) { $parameters.Reinstall = $true }

& $installer @parameters
if ($LASTEXITCODE -ne 0) {
    throw "PersistMind installation failed with exit code $LASTEXITCODE"
}

Write-Host "persistmind-install: installed from committed wheelhouse $bundle"
Write-Host "persistmind-install: runtime home $BootstrapHome"

if (Test-AgentSelected -AgentList $Agents -AgentName "codex") {
    Install-CodexWorkflowSkill -ReleaseRoot $releaseRoot
} else {
    Write-Host "persistmind-install: Codex skill skipped because -Agents does not include codex"
}
