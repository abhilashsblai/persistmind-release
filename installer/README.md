# PersistMind Installer Bundle

This directory mirrors the current first-install and cleanup scripts from the
PersistMind source repository. It is intended as the stable, reviewable installer
entry point for release preparation and controlled validation.

## Files

| File | Purpose |
| --- | --- |
| `install-persistmind.ps1` | Windows first-install wrapper. Locates or installs Python 3.11-3.13, verifies the bootstrap, and installs from signed release metadata or an explicitly qualified local wheel. |
| `bootstrap_persistmind.py` | Standard-library bootstrap that verifies signed release metadata and installs a hash-locked wheelhouse offline. |
| `install-persistmind.sh` | POSIX installer wrapper for release preparation and non-Windows validation. |
| `uninstall_persistmind.py` | Cleanup utility for PersistMind-owned installed surfaces. |

## Current Source Hashes

| File | SHA-256 |
| --- | --- |
| `install-persistmind.ps1` | `1c63d1302f850c840cd465864bdc3bf0dea4b08f4a55c24264e2604e25b88946` |
| `bootstrap_persistmind.py` | `6b37d3a4613974aa090354ea7b25cf8abc8772dbc4139b38c004945e70f72371` |
| `install-persistmind.sh` | `b5a52c37ecb85c7f5bafe87d5695cc3087a6cf83da514d372728b35cb34bf29e` |
| `uninstall_persistmind.py` | `3c92f6986f53f2b668db4449cf11c224de997cea031a865692aace2e48edf5cd` |

These hashes identify the committed files in this repository. They are not a
substitute for signed release manifests, detached signatures, wheel hashes, or
qualification evidence for a specific published release.
