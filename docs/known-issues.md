# Known Issues

## Current release

- Windows 10 is named in the intended preview boundary but was not directly
  observed in the `0.2.1.dev19` qualification run.
- Linux and macOS qualification is pending for this artifact.
- Python 3.11 and Python 3.13 qualification is pending for this artifact.
- Acceptance in a real, non-disposable project remains tester feedback rather
  than release qualification.
- Independent updater and rollback promotion gates remain pending.
- The preview is unsigned and cannot be installed through the trusted updater.
- Windows may display warnings for downloaded unsigned archive or wheel files.
- There is no production, enterprise, or response-time SLA.
- Resource requirements are repository-dependent and do not yet have a
  qualified universal minimum.

The isolated installed-wheel lifecycle completed without data corruption or
uncontrolled mutation. New real-project issues should be reported under
[SUPPORT.md](../SUPPORT.md).
