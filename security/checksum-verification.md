# Checksum Verification

SHA-256 compares downloaded bytes with the release record.

## Windows

```powershell
Get-FileHash C:\Path\To\artifact.whl -Algorithm SHA256
```

Compare the complete lowercase or uppercase hexadecimal digest with
[releases/current.md](../releases/current.md). Also compare filename, byte size,
version, and source commit.

Stop when any value differs. Do not rename a mismatched file to the expected
name, edit the manifest, or bypass verification.

A matching checksum does not authenticate the publisher. Use
[signature verification](signature-verification.md) when the release channel
requires it.
