# CTX Layer - Context Engineering, Memory, and Governance for AI Coding Agents

Copyright (c) 2026 Abhilash Pillai. All rights reserved.

Developed by Abhilash Pillai.

CTX Layer is a local-first developer tool for AI coding agents such as Codex.
It adds context engineering, repository memory, structured planning,
governance checks, audit trails, MCP integration, and impact analysis to the
AI-assisted software development workflow.

Use CTX Layer when you want coding agents to understand the right files before
they edit, stay inside an approved task plan, choose better tests, and leave a
durable explanation of what changed and why.

![CTX Layer social preview](docs/assets/ctxlayer-social-preview.png)

## What CTX Layer Is

CTX Layer is a local context and memory layer for AI coding tools. It sits
beside a Git repository and gives agents a repeatable workflow:

- Build deterministic context packs for each task.
- Create structured task plans before code changes.
- Validate changed files against the active plan.
- Check final diffs against the context served to the agent.
- Produce impact reports for changed files.
- Record useful outcomes as local project memory.
- Generate `AGENTS.md`, hooks, policies, and MCP configuration for supported
  tools.

The goal is simple: make agentic coding safer, more reviewable, and easier to
repeat across real repositories.

## Built For Modern Agent Workflows

CTX Layer is meant for repositories where AI coding agents are doing real
engineering work, not just one-off code suggestions. It gives Codex and other
agentic development tools a local operating layer for repository context,
project memory, Model Context Protocol integration, governance policy, audit
trails, code review preparation, and test impact analysis.

That makes it a practical fit for teams experimenting with context engineering,
local-first LLM developer tooling, agent memory, MCP servers, and repeatable
AI-assisted software engineering workflows.

## Why Use CTX Layer

Coding models are strongest when they receive the right context and have a
clear task boundary. Without that, they can miss important files, over-edit,
forget project rules, or leave future agents without useful history.

CTX Layer improves AI-assisted development by giving agents:

- Relevant files, policies, and memory before they edit.
- Explicit plans tied to intended files and tests.
- Guardrails for secrets, migrations, dependencies, critical paths, and CI
  files.
- Local checks that compare the final diff to the task context.
- Impact reports that suggest what should be reviewed or tested.
- Durable summaries of decisions, trade-offs, and gotchas for future work.

## Common Use Cases

- **Codex workflows**: give Codex a scoped task, retrieve the right context,
  create a plan, edit, validate, and record the outcome.
- **AI-assisted feature work**: keep generated edits tied to the relevant
  repository files and tests.
- **Bug fixes**: identify the related area, constrain the edit, and use impact
  output to decide which tests matter.
- **Refactors**: keep broad edits tied to declared files and make the change
  easier to audit.
- **Code review preparation**: run diff checks and impact reports before opening
  a pull request.
- **Team agent governance**: standardize how AI agents work across
  repositories.
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
- **Impact reports**: analyzes changed paths and related risk so teams can
  choose practical tests and review focus.
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

Use a normal Python environment, `pipx`, or a virtual environment outside the
project you want CTX Layer to manage. Avoid placing a new `.venv` inside the
target project before setup, because repository indexing may scan it.

Verify the install:

```powershell
ctxlayer --version
```

Expected output:

```text
ctxlayer 0.1.0
```

## Configure a Project

Run setup from the root of the repository where you want to use CTX Layer.

For a new folder that is not already a Git repository:

```powershell
ctxlayer --repo . setup codex --init-git --install-hooks --configure-mcp --absolute-mcp-repo
ctxlayer --repo . doctor
ctxlayer --repo . plan --help
```

For an existing Git repository, omit `--init-git`:

```powershell
ctxlayer --repo . setup codex --install-hooks --configure-mcp --absolute-mcp-repo
ctxlayer --repo . doctor
ctxlayer --repo . plan --help
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

## License

Copyright (c) 2026 Abhilash Pillai. All rights reserved.

CTX Layer is currently free to use for local, personal, non-commercial projects.
Commercial use, enterprise deployment, resale, redistribution as part of a paid
product or service, hosted service use, and internal company-wide rollout require
prior written permission and a separate commercial license from Abhilash Pillai.

See [LICENSE](LICENSE) for the full terms.

## Notes

CTX Layer is local-first. It does not require source code to be sent to a hosted
service for the core workflow. Each team should still review generated
configuration, hooks, and policies before adopting them across important
repositories.
