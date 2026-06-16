# CTX Layer Release

CTX Layer is a local context, memory, governance, and impact layer for coding
agents. It gives tools like Codex a project-specific workflow for context packs,
structured plans, checkpoints, diff checks, impact reports, tests, and durable
outcome memory.

This repository is the release repository. It is intentionally small and does
not contain the CTX Layer source code.

## Repository Model

The CTX Layer project uses two repositories:

1. `Advanced-CTX-Layer` is the private source and development repository.
2. `ctxlayer-release` is the public or company-facing release repository.

Build wheels from the private source repository, then attach the wheel to a
versioned release in this repository. Developers install the wheel and use the
`ctxlayer` command; they do not need the private source repository in their
application projects.

## Requirements

- Python 3.11 or newer
- Git, for project setup hooks and repository inspection
- Codex, if you want the generated `AGENTS.md` workflow to guide Codex sessions

Optional:

- Node.js, only if your team also distributes the npm wrapper

## Install From a Release Wheel

Download the wheel from this repository's release page, then install it:

```powershell
python -m pip install --upgrade .\ctxlayer-0.1.0-py3-none-any.whl
```

If your release is hosted on GitHub or another HTTP-accessible release page, you
can install directly from the asset URL:

```powershell
python -m pip install --upgrade "https://github.com/YOUR_ORG/ctxlayer-release/releases/download/v0.1.0/ctxlayer-0.1.0-py3-none-any.whl"
```

Verify the install:

```powershell
ctxlayer --version
```

## Configure a Project

Run these commands from the application repository that should use CTX Layer:

```powershell
ctxlayer --repo . setup codex --install-hooks --configure-mcp --absolute-mcp-repo
ctxlayer --repo . doctor
```

If the project is not already a Git repository, add `--init-git`:

```powershell
ctxlayer --repo . setup codex --init-git --install-hooks --configure-mcp --absolute-mcp-repo
```

## Files Added to a Project

Project setup may create or update:

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

## Normal Codex Workflow

Once a project is configured, Codex should follow the workflow in `AGENTS.md`:

```powershell
ctxlayer --repo . task start --task "<task>"
ctxlayer --repo . pack --task "<task>"
ctxlayer --repo . plan create --task-session-id <task_session_id> --pack-id <pack_id> --file <plan.json>
ctxlayer --repo . plan checkpoint <plan_id> --step-id <step_id> --path <changed_path>
git diff HEAD | ctxlayer --repo . check-diff --pack-id <pack_id>
git diff --name-only HEAD | ctxlayer --repo . impact --paths-from-stdin
ctxlayer --repo . outcome --pack-id <pack_id> --result pass --summary "<what changed and why>"
```

## Building a New Wheel

Only maintainers with access to the private source repository need this step.

From the private `Advanced-CTX-Layer` source repository:

```powershell
python -m pip install --upgrade build
python -m build --wheel --outdir ..\ctxlayer-release\releases
```

Then create a versioned release in this repository and attach the generated
wheel from `releases/`.

## Release Checklist

1. Build the wheel from the private source repository.
2. Verify the wheel installs in a clean Python environment.
3. Run `ctxlayer --version`.
4. Run `ctxlayer --repo . doctor` in a test project.
5. Create a release tag, for example `v0.1.0`.
6. Attach the `.whl` file as the release asset.
7. Update the install URL in this README if the version changes.

## Notes

A Python wheel is a clean distribution artifact, but it is not source-code
protection. It avoids shipping the full development repository, tests, docs,
scripts, and Git history, while still giving developers the installable
`ctxlayer` CLI.
