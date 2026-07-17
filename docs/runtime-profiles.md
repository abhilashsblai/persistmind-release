# Runtime Profiles

Runtime profiles define a supported authority and maturity boundary. A profile
is not a marketing label and cannot expand the evidence attached to a release.

| Profile | Purpose | Current status |
| --- | --- | --- |
| `windows-internal-preview` | Locked local Windows evaluation profile | Qualified in `0.2.1.dev19` |
| Core Local | Local repository, filesystem, CLI, human-reviewed operation | Target boundary represented by the current preview |
| Labs | Explicit experimental capability evaluation | Disabled in the current preview |
| Team Preview | Authenticated multi-user/team service | Future qualification phase |
| Enterprise | Reviewed deployment, authorization, concurrency, and operations | Future |

The current installed wheel refuses deferred/labs activation, team/server mode,
non-loopback binding, and autonomous judgment. It keeps MCP read-only and remote
mutation unavailable.

Future profiles require their own frozen commit, artifact, platform matrix,
security review, and evidence. They are not unlocked merely because code exists.
