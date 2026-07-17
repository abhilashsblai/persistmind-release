# Artifact Verification

Do not trust a Drive filename by itself. Download the exact artifact linked from
[releases/current.md](../releases/current.md), then compare all identity fields.

## Required comparisons

1. Product and version
2. Exact filename and byte size
3. Source commit SHA
4. Runtime profile and channel
5. SHA-256 checksum
6. Manifest product/version/commit binding
7. Qualified platform and Python version
8. Signature status
9. Qualification record

## Windows checksum

For the recommended ZIP:

```powershell
Get-FileHash C:\Path\To\PersistMind-Windows-Internal-Preview-0.2.1.dev17.zip -Algorithm SHA256
```

Expected ZIP SHA-256:

```text
fc5c537a4a1ccee52d936f918c6c62b4023ac0d1741247d2c1e0322d056e22f9
```

After extraction, verify the wheel or run the bundled verifier:

```powershell
Get-FileHash .\persistmind-0.2.1.dev17-py3-none-any.whl -Algorithm SHA256
.\Install-PersistMind.ps1 -VerifyOnly
```

Expected wheel SHA-256:

```text
9a95d55d26758c9d02ee338e35b5b29d8dddcc79e0430f498c9e08d02e900c02
```

Stop if the value, filename, byte size, version, commit, or manifest differs.

## Checksum and signature distinction

SHA-256 proves that two byte sequences match. It does not prove who published
them. `0.2.1.dev17` is explicitly unsigned and ineligible for the trusted
updater. Future public/stable releases require authenticated signature
verification in addition to checksum matching.

See [checksum verification](../security/checksum-verification.md) and
[signature verification](../security/signature-verification.md).
