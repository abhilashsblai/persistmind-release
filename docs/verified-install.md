# Verified fresh installation

A fresh install has no trusted PersistMind executable yet. The trust anchor is
an independently installed official GitHub CLI (`gh`), not a script downloaded
from the PersistMind release. Verification, download, and execution are
separate operations. Never pipe a network response into PowerShell, Python,
`bash`, or `sh`.

These commands use the `gh` 2.94.0 command contract. `gh` itself requires
GitHub authentication even for these public release-verification operations.
Before starting, either run `gh auth login --hostname github.com --web`, or set
`GH_TOKEN` to a short-lived fine-grained token with read-only **Metadata**,
**Contents**, and **Attestations** repository permissions for both
`abhilashsblai/PersistMind` and `abhilashsblai/persistmind-release`.
`Attestations: read` is required by `gh attestation verify`; a token that only
has ordinary repository read access is insufficient. A new
`GH_CONFIG_DIR` contains no authentication; commands will exit with code 4
until one of those authentication methods is supplied.

## Establish the GitHub CLI trust anchor

Use only an installation channel you already trust:

- Windows: the `GitHub.cli` package from the `winget` source. For the exact
  2.94.0 binary, its Authenticode status is `Valid`, the subject is
  `CN="GitHub, Inc.", O="GitHub, Inc.", L=San Francisco, S=California, C=US`,
  the issuer is `CN=Microsoft ID Verified CS EOC CA 03, O=Microsoft
  Corporation, C=US`, and the signer thumbprint is
  `DD106F0BE59B1399A0A9D6DF0B74A3B11718FDCF`.
- macOS: the `gh` formula from the already-trusted `homebrew/core` tap. If
  Homebrew is not already a trusted package manager on the machine, stop and
  establish that trust separately.
- Debian/Ubuntu: the official `https://cli.github.com/packages` APT repository.
  Its published signing-key fingerprints are
  `2C6106201985B60E6C7AC87323F3D4EA75716059` and
  `7F38BBB59D064DBCB3D84D725612B36462313325`; the qualified keyring SHA-256 is
  `6084d5d7bd8e288441e0e94fc6275570895da18e6751f70f057485dc2d1a811b`.

For example, the qualified Windows package can be requested explicitly with:

```powershell
winget install --id GitHub.cli --exact --version 2.94.0 --source winget
```

On macOS, use `brew install gh` only when the existing Homebrew installation
and `homebrew/core` tap are already trusted. On Debian/Ubuntu, follow the
[official GitHub CLI installation instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
and compare the downloaded keyring and signing key with the values above before
adding the repository. There is no fallback that downloads and executes a
PersistMind-provided verifier.

Do not substitute a package with the same name from another source. Confirm
the version is 2.94.0 or newer and that `release verify`, `release
verify-asset`, and `attestation verify` are built-in commands:

```text
gh --version
gh release verify --help
gh release verify-asset --help
gh attestation verify --help
gh auth status --hostname github.com
```

For an intentionally clean authentication state, set `GH_CONFIG_DIR` to a new
private directory first and then authenticate. The login is not optional:

```powershell
$env:GH_CONFIG_DIR = Join-Path $env:TEMP 'persistmind-gh-verification'
New-Item -ItemType Directory -Force -Path $env:GH_CONFIG_DIR | Out-Null
gh auth login --hostname github.com --web
gh auth status --hostname github.com
```

```bash
export GH_CONFIG_DIR="${XDG_RUNTIME_DIR:-$HOME/.cache}/persistmind-gh-verification"
install -d -m 700 "$GH_CONFIG_DIR"
gh auth login --hostname github.com --web
gh auth status --hostname github.com
```

## Windows PowerShell

Choose the exact tag you intend to install. New trust-qualified releases
contain the policy, installer, and bootstrap assets named below.

```powershell
$tag = 'v0.2.0a23'
$releaseRepo = 'abhilashsblai/persistmind-release'
$sourceRepo = 'abhilashsblai/PersistMind'
$signerWorkflow = 'abhilashsblai/PersistMind/.github/workflows/release.yml'
$download = Join-Path $PWD '.persistmind-installer-download'

if (Test-Path -LiteralPath $download) { throw "Refusing non-empty download path: $download" }
New-Item -ItemType Directory -Path $download | Out-Null

gh release verify $tag -R $releaseRepo --format json
if ($LASTEXITCODE -ne 0) { throw 'Release is not verifiably immutable.' }
$sourceCommit = gh api "repos/$sourceRepo/commits/$tag" --jq .sha
if ($LASTEXITCODE -ne 0 -or $sourceCommit -notmatch '^[0-9a-f]{40}$') {
  throw 'Could not resolve the source tag to a full commit SHA.'
}
$releaseRepoCommit = gh api "repos/$releaseRepo/commits/$tag" --jq .sha
if ($LASTEXITCODE -ne 0 -or $releaseRepoCommit -notmatch '^[0-9a-f]{40}$') {
  throw 'Could not resolve the release-repository tag to a full commit SHA.'
}

gh release download $tag -R $releaseRepo -D $download `
  -p persistmind-release-trust.v1.json `
  -p install-persistmind.ps1 `
  -p bootstrap_persistmind.py
if ($LASTEXITCODE -ne 0) { throw 'Release asset download failed.' }

$policyPath = Join-Path $download 'persistmind-release-trust.v1.json'
$installerPath = Join-Path $download 'install-persistmind.ps1'
$bootstrapPath = Join-Path $download 'bootstrap_persistmind.py'
foreach ($asset in @($policyPath, $installerPath, $bootstrapPath)) {
  gh release verify-asset $tag $asset -R $releaseRepo --format json
  if ($LASTEXITCODE -ne 0) { throw "Release-asset verification failed: $asset" }
}

$policy = Get-Content -Raw -LiteralPath $policyPath | ConvertFrom-Json
if ($policy.schema_version -ne 'persistmind.release-trust.v1' -or
    $policy.release_tag -ne $tag -or
    $policy.source_ref -ne "refs/tags/$tag" -or
    $policy.source_commit -ne $sourceCommit -or
    $policy.release_repo_commit -ne $releaseRepoCommit -or
    $policy.signer_workflow -ne $signerWorkflow) {
  throw 'Release trust policy identity mismatch.'
}

foreach ($asset in @($policyPath, $installerPath, $bootstrapPath)) {
  gh attestation verify $asset --repo $sourceRepo `
    --signer-workflow abhilashsblai/PersistMind/.github/workflows/release.yml `
    --source-ref $policy.source_ref `
    --source-digest $sourceCommit `
    --cert-oidc-issuer https://token.actions.githubusercontent.com `
    --deny-self-hosted-runners --format json
  if ($LASTEXITCODE -ne 0) { throw "Build-provenance verification failed: $asset" }
}

foreach ($asset in @($installerPath, $bootstrapPath)) {
  $record = $policy.assets | Where-Object name -eq (Split-Path -Leaf $asset)
  if (-not $record) { throw "Asset is absent from trust policy: $asset" }
  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $asset).Hash.ToLowerInvariant()
  if ($actual -ne $record.sha256 -or (Get-Item -LiteralPath $asset).Length -ne $record.size) {
    throw "Asset hash or size mismatch: $asset"
  }
}

& $installerPath -Repo . -Version $tag -BootstrapPath $bootstrapPath
```

Every command must succeed before the installer is executed. Keep the JSON
output if release provenance must be audited later.

## macOS or Linux

The POSIX procedure enforces the same policy:

```bash
set -euo pipefail
tag='v0.2.0a23'
release_repo='abhilashsblai/persistmind-release'
source_repo='abhilashsblai/PersistMind'
download="$PWD/.persistmind-installer-download"

[ ! -e "$download" ] || { echo "refusing existing download path: $download" >&2; exit 1; }
install -d -m 700 "$download"

gh release verify "$tag" -R "$release_repo" --format json
source_commit="$(gh api "repos/$source_repo/commits/$tag" --jq .sha)"
release_repo_commit="$(gh api "repos/$release_repo/commits/$tag" --jq .sha)"
case "$source_commit" in
  *[!0-9a-f]*|'') echo 'could not resolve source tag to a commit' >&2; exit 1 ;;
esac
[ "${#source_commit}" -eq 40 ] || { echo 'source commit is not a full SHA' >&2; exit 1; }
case "$release_repo_commit" in
  *[!0-9a-f]*|'') echo 'could not resolve release repository commit' >&2; exit 1 ;;
esac
[ "${#release_repo_commit}" -eq 40 ] || { echo 'release repository commit is not a full SHA' >&2; exit 1; }
gh release download "$tag" -R "$release_repo" -D "$download" \
  -p persistmind-release-trust.v1.json \
  -p install-persistmind.sh \
  -p bootstrap_persistmind.py

policy="$download/persistmind-release-trust.v1.json"
installer="$download/install-persistmind.sh"
bootstrap="$download/bootstrap_persistmind.py"
for asset in "$policy" "$installer" "$bootstrap"; do
  gh release verify-asset "$tag" "$asset" -R "$release_repo" --format json
done

for asset in "$policy" "$installer" "$bootstrap"; do
  gh attestation verify "$asset" --repo "$source_repo" \
    --signer-workflow abhilashsblai/PersistMind/.github/workflows/release.yml \
    --source-ref "refs/tags/$tag" \
    --source-digest "$source_commit" \
    --cert-oidc-issuer https://token.actions.githubusercontent.com \
    --deny-self-hosted-runners --format json
done

# Run only after the policy itself has passed release-asset and build-attestation
# verification. This uses an already-trusted local Python, not downloaded code.
python3 - "$policy" "$tag" "$source_commit" "$release_repo_commit" <<'PY'
import json, sys
policy = json.load(open(sys.argv[1], encoding="utf-8"))
expected = (sys.argv[2], sys.argv[3], sys.argv[4])
actual = (policy.get("release_tag"), policy.get("source_commit"), policy.get("release_repo_commit"))
if actual != expected:
    raise SystemExit("release trust policy commit identity mismatch")
PY

bash "$installer" --repo . --version "$tag" --bootstrap-path "$bootstrap"
```

If `gh release verify` reports a mutable release or missing release
attestation, stop. Releases published before this contract do not gain these
properties retroactively.
