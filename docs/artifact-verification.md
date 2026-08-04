# Artifact Verification

Do not trust a filename by itself. For the self-contained GitHub diagnostic
bundles, compare every wheelhouse file against the committed `SHA256SUMS.txt`
and verify that `dependency-lock.v1.json` names the expected Python minor
version.

## GitHub diagnostic bundle verification

From the release repository root:

```powershell
$bundle = "bundles\0.2.2\windows-py312"
Get-Content "$bundle\SHA256SUMS.txt" | ForEach-Object {
  $parts = $_ -split "\s+", 2
  if ($parts.Count -ne 2) { throw "Malformed checksum line: $_" }
  $expected = $parts[0].ToLowerInvariant()
  $path = Join-Path $bundle $parts[1].Trim()
  $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -ne $expected) { throw "Checksum mismatch: $path" }
}
```

Use `windows-py311`, `windows-py312`, or `windows-py313` to match the Python
version used for installation. The committed installer wrapper performs the
PersistMind wheel hash check automatically before installing.

Expected PersistMind wheel hashes:

| Bundle | Python | PersistMind wheel SHA-256 |
| --- | --- | --- |
| `bundles/0.2.2/windows-py311` | 3.11 | `246d141cbc638ca3509b5cb903110de3b6b9f13f8722147b7dd333a307d6c1ff` |
| `bundles/0.2.2/windows-py312` | 3.12 | `246d141cbc638ca3509b5cb903110de3b6b9f13f8722147b7dd333a307d6c1ff` |
| `bundles/0.2.2/windows-py313` | 3.13 | `daf420ac7642b24f727cb93342fa309c9f8b58372d8e6fa0bd4d1eabba2c8cb0` |

SHA-256 proves byte equality; it does not authenticate an unsigned publisher.
This diagnostic bundle is not eligible for the trusted updater.

## Historical Drive preview verification

For the older `0.2.2.dev1` Drive preview, download the exact artifact linked
from [releases/current.md](../releases/current.md), then compare its filename,
size, version, source commit, runtime profile, qualification, and SHA-256.

## Windows checksum

```powershell
Get-FileHash C:\Path\To\PersistMind-Windows-Internal-Preview-0.2.2.dev1.zip -Algorithm SHA256
```

Expected ZIP SHA-256:

```text
26aba71a82beb992628cc81c309a535af280db17ab118402ef2ffd0fe3bce9f4
```

After extraction:

```powershell
Get-FileHash .\persistmind-0.2.2.dev1-py3-none-any.whl -Algorithm SHA256
.\Install-PersistMind.ps1 -VerifyOnly
```

Expected wheel SHA-256:

```text
40e0e3d9369d9e6f0285825611492844d11fefecf932040ccb50b8b7d9f2a11d
```

The manifest must identify version `0.2.2.dev1`, source commit
`ee5ede7df9aef29d6e99c9ef16ef7ff0d185838a`, profile
`windows-internal-preview`, Windows 11, and CPython 3.12.

This preview is also not eligible for the trusted updater.
