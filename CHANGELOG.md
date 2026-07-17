# Changelog

## 0.2.1.dev4 - 2026-07-17

### Added

- Locked `windows-internal-preview` runtime profile.
- Exact release identity in version, status, and diagnostics.
- Installed-wheel qualification on Windows with Python 3.11-3.13.
- Manifest, checksum, limitation, installation, and evidence records.

### Changed

- Release artifacts moved to a private version-specific Google Drive channel.
- GitHub became documentation, metadata, qualification, and history only.

### Fixed

- Release qualification tooling now validates continuation, memory evidence,
  uninstall preservation, and strict machine-result schemas.

### Security

- Remote writes, writable MCP, and autonomous source modification remain
  disabled.
- The unsigned preview is explicitly excluded from the trusted updater.

### Known limitations

- Windows 10 qualification is pending.
- Linux and macOS qualification is pending.
- No production, public-beta, enterprise, or support-SLA claim.
