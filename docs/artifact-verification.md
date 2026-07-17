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
Get-FileHash C:\Path\To\PersistMind-Windows-Internal-Preview-0.2.1.dev15.zip -Algorithm SHA256
```

Expected ZIP SHA-256:

```text
4d5edaf1ff008aa45bb340de15c735f9966bfac48eff2505d9f5d81cc23f4598
```

After extraction, verify the wheel or run the bundled verifier:

```powershell
Get-FileHash .\persistmind-0.2.1.dev15-py3-none-any.whl -Algorithm SHA256
.\Install-PersistMind.ps1 -VerifyOnly
```

Expected wheel SHA-256:

```text
4f79e8eaa3dcedff672471fbfdfd1745ccd5ab913af7b2ccb1288e6e9b08fc77
```

Stop if the value, filename, byte size, version, commit, or manifest differs.

## Checksum and signature distinction

SHA-256 proves that two byte sequences match. It does not prove who published
them. `0.2.1.dev15` is explicitly unsigned and ineligible for the trusted
updater. Future public/stable releases require authenticated signature
verification in addition to checksum matching.

See [checksum verification](../security/checksum-verification.md) and
[signature verification](../security/signature-verification.md).
