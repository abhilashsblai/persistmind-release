---
name: persistmind-workflow
description: Use when working in or repairing a PersistMind-governed project, especially for PersistMind preflight, task/session start, pack generation, plans, checkpoints, hooks, MCP setup, verification, or outcome handoff. This skill keeps the coding agent carrying the correct repo path, task identifiers, pack/preflight evidence, intended files/tests, and verification state between stages.
---

# PersistMind Workflow

## Overview

Use this skill whenever a user asks Codex to work with PersistMind in a project repository, repair PersistMind installation, or run a PersistMind-governed coding task. The goal is to prevent repeated mistakes caused by missing stage data: wrong repo path, stale hooks, absent task/session IDs, missing pack IDs, unclear intended files, skipped verification, or premature outcome claims.

PersistMind is stage-based. At every stage, preserve the identifiers and evidence produced by the previous stage, and pass them forward explicitly.

## First Decision

Before running any PersistMind command, classify the situation:

- Source repository development: If the current repo is the PersistMind product source itself, use normal source tests and do not run `persistmind setup` unless the user explicitly asks to test installer or self-hosting behavior.
- Governed project work: If the target repo is an application using PersistMind, use PersistMind stage gates before edits.
- Install or repair: If the user asks to install, repair, check hooks, or configure MCP, verify setup surfaces first, then repair only the target project.
- Read-only audit: If the user asks to inspect, review, explain, or plan, use read-mode preflight and avoid project mutation unless requested.

When the target repository is ambiguous, inspect the working directory and nearby config first. Do not assume the repo from memory, shell cwd, or PATH.

## Required State Packet

Maintain this packet in your working notes and final handoff whenever PersistMind is involved:

```text
repo_path:
persistmind_command:
mode: read | write | install-repair | source-dev
task:
task_session_id:
pack_id:
memory_retrieval_id:
snapshot_id:
plan_id:
plan_step_id:
intended_files:
intended_tests:
changed_files:
verification_commands:
verification_results:
outcome_state:
blockers:
```

Unknown fields should be marked `unknown`, not silently omitted. Update the packet as commands return new IDs.

## Stage Workflow

### 1. Locate Repo And Runtime

- Confirm the absolute target repo path.
- Prefer project-local PersistMind configuration over global assumptions: inspect `.persistmind/`, `.codex/`, `.mcp.json`, agent hook configs, and documented installer ledgers when present.
- If `persistmind` is not on PATH, look for the configured runtime path in project setup files before falling back to a global command.
- Check for stale absolute paths when repairing installs, especially old drive roots, old usernames, or a different clone path.

### 2. Preflight Before Context-Sensitive Work

For read-only work, run a read preflight when available and preserve returned identifiers:

```powershell
persistmind --repo <repo_path> codex preflight --task "<task>" --mode read
```

For implementation work, start or identify the task/session first, then run write preflight tied to that session. Do not proceed with edits on stale preflight output from another repo, task, or branch.

Carry forward at least:

- `task_session_id`
- `pack_id`
- `memory_retrieval_id` or equivalent retrieval evidence
- `snapshot_id` or working-tree evidence
- branch and dirty-state summary

### 3. Plan With Intent

Before edits, create or update a plan with enough detail for hook enforcement:

- objective
- ordered steps
- intended files per step
- intended tests per step
- expected capabilities or surfaces touched
- risk notes for broad/shared changes

If implementation requires files not in the current plan, amend the plan or record why the scope changed before continuing.

### 4. Edit Under The Active Step

During coding, keep the active `plan_step_id` and intended file set available to the agent. Before each meaningful edit, check whether the file belongs to the active step. If it does not, update the plan or stop and explain the mismatch.

Do not treat hook bypasses, temporary approvals, or disabled enforcement as a normal completion path. If a hook blocks a change, capture the exact error and fix the workflow data unless the user explicitly asks for diagnostic bypass testing.

### 5. Verify Behavior And Diff

Before completion, verify both code behavior and PersistMind governance:

- Run the intended tests and any focused regression probes.
- Check the diff against the active pack or plan when available.
- Run impact analysis for changed files when available.
- Re-run `doctor` or `status` only as install health checks; they do not prove the task workflow is complete.

Use concrete command output in the handoff: pass/fail, exact failing command, and the relevant IDs used.

### 6. Record Outcome

Only mark the task complete after verification has run and the outcome is recorded with the same task/session IDs used during implementation. Include:

- final result
- changed files
- tests run
- rejected or deferred scope
- unresolved blockers
- commit hash or deployment reference when applicable

If outcome recording fails, report the task implementation separately from governance finalization. Do not imply that the PersistMind workflow closed cleanly.

## Install And Hook Repair

When the user asks to install or repair PersistMind in another project:

- Use the release or installer source requested by the user.
- Confirm the target repo absolute path before running setup.
- Keep install repair out of the PersistMind source repo unless explicitly testing installer behavior.
- Verify active surfaces after setup: `.persistmind` config, Codex hooks, Gemini hooks if requested, `.mcp.json`, agent instructions, and runtime paths.
- Run direct hook smoke probes in addition to `doctor --summary`.
- Scan active config for stale paths. Historical logs may retain old paths; do not rewrite them unless the user asks.

Setup is not complete until the installed runtime, hook entrypoints, MCP configuration, and direct hook smoke tests all refer to the intended repo.

## Timeouts, Locks, And Worker State

When PersistMind commands time out or report database locks:

- Capture the exact command and error text.
- Check for repo-specific PersistMind, MCP, or hook worker processes before killing anything.
- Prefer bounded, focused preflight or pack probes over repeatedly running broad commands.
- Do not edit the PersistMind database directly as a routine fix.
- Separate install health, governance state, and task implementation state in the report.

## Handoff Format

Use this compact handoff when finishing or pausing:

```text
PersistMind state:
- repo: <absolute path>
- mode: <read/write/install-repair/source-dev>
- task_session_id: <id or unknown>
- pack_id: <id or unknown>
- plan_id/step: <id or unknown>
- changed files: <list>
- verification: <commands and result>
- outcome: <recorded/failed/not applicable>
- remaining risk: <none or concrete issue>
```

For deeper stage rules, load `references/stage-contract.md`.
