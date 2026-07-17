# Frequently Asked Questions

## Is PersistMind production-ready?

No. The current release is an unsigned internal Windows preview for
non-critical local testing.

## Can I use it commercially?

The included personal-use license excludes commercial, enterprise,
institutional, consulting, hosted, and company-wide use without a separate
written agreement.

## Does PersistMind send my code online?

The current supported profile is local-first and limited to local repositories
and local filesystem state. Release downloads come from Google Drive. Do not
enable or infer support for remote/team integrations in this preview.

## Can it run offline?

After the wheel and its dependencies are available locally, core repository
operations are designed for local execution. Downloading artifacts and any
separately configured external provider are not offline operations.

## Does it support Windows?

Windows 11 passed installed-wheel qualification with Python 3.12. Windows 10
and Python 3.11/3.13 remain pending for this candidate.

## How much RAM and disk space does it need?

There is no qualified universal minimum yet. Usage varies with repository size,
index contents, backup retention, and Python dependencies. Start with a small
disposable repository and monitor `.persistmind` growth.

## How is it different from an AI editor or coding agent?

PersistMind does not replace the editor or agent. It supplies repository
intelligence, bounded context, workflow state, verification evidence, memory,
and audit information around an agent's work.

## Can MCP modify my repository?

Not in the current release boundary. Stdio MCP is read-only and does not have a
transport-bound principal for mutations.

## Can I use the automatic updater?

No. `0.2.1.dev18` is unsigned and must be installed manually after checksum
verification.
