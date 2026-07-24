# Artifact Verification

Do not trust a Drive filename by itself. Download the exact artifact linked from
[releases/current.md](../releases/current.md), then compare its filename, size,
version, source commit, runtime profile, qualification, and SHA-256.

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

SHA-256 proves byte equality; it does not authenticate an unsigned publisher.
This preview is not eligible for the trusted updater.
