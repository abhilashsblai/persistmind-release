# Uninstall and Cleanup

## Remove the isolated package

Activate the preview virtual environment, then run:

```powershell
python -m pip uninstall persistmind
```

Package removal must not delete repository source or user-owned files.

## Review local state

The `.persistmind` directory may contain indexes, workflow state, approved
memory, audit information, and backups. Preserve or export anything required
before explicit cleanup.

When a release includes an ownership-aware uninstaller, run its dry-run mode
first. Review every proposed path. Cleanup should remove only files and
configuration owned by that installation and preserve modified or unowned
content.

Do not copy uninstall commands from a historical release. Use only the
instructions attached to the installed release record.
