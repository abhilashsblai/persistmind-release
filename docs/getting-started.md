# Getting Started

## Before you install

The current release is an unsigned Windows internal preview. Use a disposable
or non-critical local Git repository, create a commit or backup, remove
credentials from the test copy, and review every result manually.

The qualified path is Windows 11 with Python 3.12, Git, and PowerShell. Windows
10, Python 3.11/3.13, Linux, and macOS remain pending.

## Install and verify

1. Open the exact [current release record](../releases/current.md).
2. Download its version-specific ZIP link.
3. Verify the ZIP SHA-256 before extraction.
4. Run `Install-PersistMind.ps1 -VerifyOnly`.
5. Install into a new isolated environment.
6. Invoke PersistMind through that environment's exact Python executable.
7. Configure a disposable or non-critical repository and run `doctor --summary`.

The output must identify version `0.2.1.dev18`, source commit
`60924ed94d1d7bcf965bf729ccef947936fd5995`, and runtime profile
`windows-internal-preview`.

## First governed workflow

Use the generated project instructions. A mutation task must have a task
session, agent session, context pack, plan, write preflight, verification,
checkpoints, outcome, and closed session. Do not rely on a bare global
`persistmind` command when qualifying a specific installed candidate.

Do not enable labs, team/server operation, remote writes, writable MCP, or the
automatic updater for this release.
