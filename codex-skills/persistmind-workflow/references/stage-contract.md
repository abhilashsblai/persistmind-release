# PersistMind Stage Contract

This reference defines the minimum information a coding agent should preserve and pass between PersistMind stages.

## Stage Matrix

| Stage | Required Inputs | Required Outputs | Common Failure To Avoid |
| --- | --- | --- | --- |
| Repo selection | User request, cwd, absolute repo path | Confirmed `repo_path` and branch | Running commands against the wrong clone |
| Runtime discovery | PATH, project config, installer records | `persistmind_command` and runtime path | Assuming global PATH points to the project runtime |
| Read preflight | Repo, task, mode read | Pack/retrieval/snapshot identifiers | Treating old preflight as current |
| Task/session start | Repo, task objective | `task_session_id` | Editing without a session ID |
| Write preflight | Repo, task, session, mode write | Current `pack_id` and governance status | Mixing IDs from another task |
| Planning | Objective, pack, intended scope | `plan_id`, ordered steps, file/test intent | Hooks blocking because files are not in the plan |
| Active step | `plan_id`, `plan_step_id`, intended files | Changed files tied to the step | Editing outside the active step silently |
| Checkpoint | Step, changed files, evidence | Checkpoint ID or recorded progress | Losing why a change was allowed |
| Verification | Changed files, intended tests | Test results and impact/diff evidence | Claiming success from build-only or doctor-only checks |
| Outcome | Session, pack, verification | Recorded result and handoff | Calling complete without recording outcome |

## Preflight Information

Preflight output is useful only when it is current for all of these dimensions:

- same absolute repo path
- same branch or commit context
- same task/session
- same mode, read or write
- same intended file scope
- no relevant hook or setup changes since the preflight

If any dimension changed, refresh preflight or clearly mark the prior result stale.

## Plan Step Information

Each implementation step should carry:

- stable step ID
- short title
- files expected to change
- tests or probes expected to run
- governance capability needed, if any
- reason the step is necessary

If a new file needs to be edited, update the step before editing. This is especially important for generated files, hook scripts, installer surfaces, and agent config files.

## Verification Information

A completion claim should include both project behavior and PersistMind workflow evidence where relevant:

- project tests, lint, build, or targeted probes
- PersistMind diff or impact check when available
- hook smoke test when hooks were installed or repaired
- MCP tool/list or startup probe when MCP was configured
- outcome or final transition evidence when a task/session was opened

Do not collapse these into a single "doctor healthy" statement. Doctor health means setup is likely coherent; it does not prove the coding task was governed correctly.

## Repair Information

For install and hook repairs, pass these details through the work:

- installer source or release repo path
- target repo path
- selected Python/runtime path
- bootstrap home or PersistMind home
- agents configured
- hook files touched
- MCP config files touched
- stale paths found and whether they were active config or historical logs
- direct hook smoke command and result

When reporting completion, distinguish:

- installed successfully
- hooks configured
- MCP configured
- direct enforcement tested
- full task workflow tested

These are separate claims.
