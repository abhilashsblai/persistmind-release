# CTX Layer

CTX Layer is a local context, memory, governance, and impact layer for coding
agents. It helps AI coding tools work with better repository context, follow a
repeatable task workflow, check whether their final diff stayed in scope, and
remember useful outcomes for future work.

It is designed for teams that use coding models such as Codex and want more
reliable edits, clearer audit trails, better test selection, and fewer wrong-file
changes.

## What CTX Layer Does

CTX Layer sits beside your repository and gives coding agents a project-aware
workflow:

- Builds deterministic context packs for each task.
- Creates structured plans before code changes.
- Validates file changes against the active plan.
- Checks final diffs against the served context.
- Produces impact reports for changed files.
- Records outcomes and useful summaries as local project memory.
- Generates agent instructions and MCP configuration for supported tools.
- Keeps the control plane local by default.

The result is a tighter coding loop: the model starts with better context, edits
with clearer scope, and finishes with checks that make the work easier to trust.

## Why Use It

Coding models are strongest when they receive the right context and have a
clear task boundary. Without that, they can miss important files, over-edit,
forget project rules, or leave future agents without useful history.

CTX Layer improves the coding process by giving agents:

- Relevant files and memory before they edit.
- Explicit plans tied to intended files and tests.
- Guardrails for critical paths, secrets, migrations, dependencies, and CI files.
- Local checks that compare the final diff to the task context.
- Impact reports that suggest what should be reviewed or tested.
- Durable summaries of what changed and why.

## Common Use Cases

- **AI-assisted feature work**: give Codex a scoped task, retrieve the right
  context, create a plan, edit, validate, and record the outcome.
- **Bug fixes**: identify the relevant area, constrain the edit, and use impact
  output to decide which tests matter.
- **Refactors**: keep edits tied to declared files and make broad changes easier
  to audit.
- **Code review preparation**: run diff checks and impact reports before opening
  a PR.
- **Team agent governance**: standardize how AI agents work across repositories.
- **Project memory**: preserve useful implementation decisions so future tasks
  do not start from zero.
- **MCP integration**: expose CTX Layer tools to compatible agent clients.

## Key Features

- **Context packs**: task-specific snapshots of relevant files, project memory,
  policies, and impact signals.
- **Structured task plans**: JSON-backed plans with objective, steps, intended
  files, intended tests, capabilities, and risk.
- **Plan checkpoints**: validates changed files against the active plan step.
- **Diff checks**: verifies whether the final diff matches the context served to
  the agent.
- **Impact reports**: analyzes changed paths and related risk so teams can choose
  practical tests and review focus.
- **Capability policy**: flags or blocks sensitive actions such as touching
  secrets, modifying migrations, changing dependency files, or editing critical
  paths.
- **Local memory**: records outcomes, summaries, and approved project knowledge.
- **Agent setup**: generates `AGENTS.md`, capability policy, hooks, and MCP
  snippets for project use.
- **Local-first storage**: project state lives in the project workspace unless
  you choose to export or integrate it elsewhere.

## Requirements

- Python 3.11 or newer
- Git
- A terminal with access to the project repository

Optional:

- Codex or another agent that reads `AGENTS.md`
- An MCP-compatible client if you want tool integration

## Install

Install the latest release wheel:

```powershell
python -m pip install --upgrade "https://github.com/abhilashsblai/ctxlayer-release/releases/download/v0.1.0/ctxlayer-0.1.0-py3-none-any.whl"
```

Verify the install:

```powershell
ctxlayer --version
```

Expected output:

```text
ctxlayer 0.1.0
```

## Configure a Project

Run setup from the root of the repository where you want to use CTX Layer:

```powershell
ctxlayer --repo . setup codex --install-hooks --configure-mcp --absolute-mcp-repo
ctxlayer --repo . doctor
```

If the folder is not already a Git repository, add `--init-git`:

```powershell
ctxlayer --repo . setup codex --init-git --install-hooks --configure-mcp --absolute-mcp-repo
```

Setup may create or update:

- `AGENTS.md`
- `ctxlayer.capabilities.yaml`
- `.ctxlayer/`
- local Git hooks, when `--install-hooks` is used
- MCP snippets under `.ctxlayer/mcp/`

Usually commit:

- `AGENTS.md`
- `ctxlayer.capabilities.yaml`

Usually do not commit:

- `.ctxlayer/`

`.ctxlayer/` contains local workspace state, databases, generated context, and
machine-specific MCP snippets.

## Daily Usage With Codex

After setup, Codex should follow the workflow written into `AGENTS.md`. The
typical lifecycle is:

```powershell
ctxlayer --repo . task start --task "<task>"
ctxlayer --repo . pack --task "<task>"
```

Create a structured plan:

```powershell
ctxlayer --repo . plan create --task-session-id <task_session_id> --pack-id <pack_id> --file <plan.json>
```

Checkpoint changed files:

```powershell
ctxlayer --repo . plan checkpoint <plan_id> --step-id <step_id> --path <changed_path>
```

Before finishing, run preflight checks:

```powershell
git diff HEAD | ctxlayer --repo . check-diff --pack-id <pack_id>
git diff --name-only HEAD | ctxlayer --repo . check-diff --pack-id <pack_id> --paths-from-stdin
git diff --name-only HEAD | ctxlayer --repo . impact --paths-from-stdin
```

Record the outcome:

```powershell
ctxlayer --repo . outcome --pack-id <pack_id> --result pass --summary "<what changed and why>"
```

## Useful Commands

Check project health:

```powershell
ctxlayer --repo . doctor
```

Index or refresh repository context:

```powershell
ctxlayer --repo . index
```

Generate a context pack:

```powershell
ctxlayer --repo . pack --task "describe the change"
```

Inspect impact for files:

```powershell
ctxlayer --repo . impact --paths src/app/service.py
```

Run the MCP server:

```powershell
ctxlayer --repo . mcp
```

Render the local dashboard:

```powershell
ctxlayer --repo . dashboard render --output .ctxlayer/dashboard.html
```

## Updating

Install the newer release wheel when a new version is published:

```powershell
python -m pip install --upgrade "https://github.com/abhilashsblai/ctxlayer-release/releases/download/v0.1.0/ctxlayer-0.1.0-py3-none-any.whl"
```

Then verify:

```powershell
ctxlayer --version
ctxlayer --repo . doctor
```

## Notes

CTX Layer is local-first. It does not require source code to be sent to a hosted
service for the core workflow. Each team should still review generated
configuration, hooks, and policies before adopting them across important
repositories.
