# Capability Status

PersistMind uses five maturity terms: **Core**, **Preview**, **Experimental**,
**Disabled**, and **Planned**. Implemented code does not automatically become a
qualified product capability.

| Capability | Status | Current authority |
| --- | --- | --- |
| CLI identity, status, and doctor | Core | Local |
| Repository indexing and lexical search | Core | Local read |
| Deterministic context packs | Core | Local read |
| Impact analysis | Core | Advisory |
| Task, plan, checkpoint, verification, outcome | Core | Human-reviewed local workflow |
| Approved local memory and audit | Core | Local, approval-gated |
| Storage integrity, backup, and restore | Core | Human-reviewed local workflow |
| Read-only stdio MCP | Core | Read-only |
| Semantic retrieval | Experimental | Labs only |
| Architecture analysis | Experimental | Labs only |
| Cognitive improvement | Experimental | Labs only; non-authoritative |
| Anticipation | Experimental | Labs only; non-authoritative |
| Team server | Planned | Unavailable |
| Remote writes | Disabled | None |
| Writable MCP | Disabled | None |
| Automatic self-improvement adoption | Disabled | None |
| Autonomous self-modification | Disabled | None |

Promotion requires release-specific evidence, usage data, safe rollback, and a
runtime profile that explicitly permits the capability.
