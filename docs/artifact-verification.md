# Artifact Verification

Do not trust a Drive filename by itself. Before installation, compare the
download with [releases/current.md](../releases/current.md).

## Required comparisons

1. Product and version
2. Exact filename and byte size
3. Source commit SHA
4. Runtime profile and channel
5. SHA-256 checksum
6. Manifest product/version/commit binding
7. Python compatibility
8. Signature status
9. Qualification record

## Windows checksum

```powershell
Get-FileHash C:\Path\To\persistmind-0.2.1.dev4-py3-none-any.whl -Algorithm SHA256
```

Expected current wheel SHA-256:

```text
e91b3f403cb76816cfa608b5848a96c82054e07a0cc3c4e4898c2084af5e9bad
```

Stop if the value, filename, byte size, version, commit, or manifest differs.

## Checksum and signature distinction

SHA-256 proves that two byte sequences match. It does not prove who published
them. `0.2.1.dev4` is explicitly unsigned and ineligible for the trusted updater.
Future public/stable releases require authenticated signature verification in
addition to checksum matching.

See [checksum verification](../security/checksum-verification.md) and
[signature verification](../security/signature-verification.md).
