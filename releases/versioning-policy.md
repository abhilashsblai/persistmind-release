# Versioning Policy

PersistMind uses version syntax together with an explicit release channel and
qualification record.

| Form | Meaning |
| --- | --- |
| `X.Y.Z.devN` | Internal development or preview identity |
| `X.Y.ZaN` | Alpha pre-release |
| `X.Y.ZbN` | Beta pre-release |
| `X.Y.Z` | Stable release after production gates pass |
| LTS designation | Stable line with a published maintenance window |

A version string alone never proves maturity. The release record controls the
channel, runtime profile, supported matrix, signature status, and restrictions.

Published artifact identity is immutable. If bytes or release-critical tooling
change, increment the version and restart qualification. Never replace a
published artifact under an existing identity.
