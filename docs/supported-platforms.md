# Supported Platforms

This table reports observed qualification for the current release, not intended
future compatibility.

| Platform | Status | Evidence |
| --- | --- | --- |
| Windows 11 | Internal preview - passed | Installed wheel, Python 3.11-3.13 |
| Windows 10 | Intended preview boundary; not observed | No current machine result |
| Linux | Not qualified | None for `0.2.1.dev4` |
| macOS | Not qualified | None for `0.2.1.dev4` |

| Python | Windows result |
| --- | --- |
| 3.11 | Passed |
| 3.12 | Passed |
| 3.13 | Passed |

The `py3-none-any` wheel tag does not override this matrix. A platform becomes
supported only after the installed artifact passes the required qualification
suite on that platform.
