# How PersistMind Works

## 1. Define the task

The developer supplies the objective, repository, and intended authority.

## 2. Resolve repository state

PersistMind identifies the Git/worktree state and uses an explicit source index
and snapshot. Indexing is not silently expanded by a context request.

## 3. Retrieve bounded context

Search and context-pack construction select relevant source under a token budget
and preserve provenance and snapshot identity.

## 4. Govern execution

Tasks, plans, checkpoints, intended paths, and verification commands define the
reviewable workflow. Retrieved context never grants write authority.

## 5. Verify the result

Actual changed paths, linked tests, command results, and outcomes are compared
with the plan and allowed scope.

## 6. Preserve reviewed knowledge

Approved facts, decisions, outcomes, and continuation records can be recalled in
later sessions. Candidate memory remains non-authoritative until an explicit
approval path promotes it.

See [architecture](architecture.md), [storage and backup](storage-and-backup.md),
and [capability status](capability-status.md).
