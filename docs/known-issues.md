# Known Issues

## Current release

- Windows 10 is named in the intended preview boundary but was not directly
  observed in the `0.2.1.dev31` qualification run.
- Linux and macOS qualification is pending for this artifact.
- Python 3.11 and Python 3.12 qualification is pending for this artifact.
- The production Windows keyring backup path was not observed because the test
  host's Credential Manager was saturated by pre-existing test credentials.
- Qualification focused on the corrected storage-routing, setup,
  installed-artifact, and FoxFlow integration paths; a clean full historical
  regression-suite claim is not made.
- Trusted updater, rollback, and signing gates remain pending for promotion.
- The preview is unsigned and cannot be installed through the trusted updater.
- Windows may display warnings for downloaded unsigned archive or wheel files.
- There is no production, enterprise, or response-time SLA.
- Resource requirements are repository-dependent and do not yet have a
  qualified universal minimum.

The focused disposable-project workflow completed without data corruption or
uncontrolled mutation. New issues should be reported under
[SUPPORT.md](../SUPPORT.md).
