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
Get-FileHash C:\Path\To\PersistMind-Windows-Internal-Preview-0.2.1.dev31.zip -Algorithm SHA256
```

Expected ZIP SHA-256:

```text
013ce8741201abd5ae8640f0bce3d7f47cb8d3d5310f8e18c64a779fa0bc9f24
```

After extraction, verify the wheel or run the bundled verifier:

```powershell
Get-FileHash .\persistmind-0.2.1.dev31-py3-none-any.whl -Algorithm SHA256
.\Install-PersistMind.ps1 -VerifyOnly
```

Expected wheel SHA-256:

```text
6c3cc745f347b5a4e11fe64bf098787e7c24697b8332f438a6e1f933e743c7bf
```

Stop if the value, filename, byte size, version, commit, or manifest differs.

## Checksum and signature distinction

SHA-256 proves that two byte sequences match. It does not prove who published
them. `0.2.1.dev31` is explicitly unsigned and ineligible for the trusted
updater. Future public/stable releases require authenticated signature
verification in addition to checksum matching.

See [checksum verification](../security/checksum-verification.md) and
[signature verification](../security/signature-verification.md).
