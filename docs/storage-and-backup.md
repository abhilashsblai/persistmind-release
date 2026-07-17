# Storage and Backup

PersistMind stores current-preview state locally under the repository's
`.persistmind` area. Logical roles separate source intelligence, task state,
activity, audit, knowledge, policy, and learning data.

## Inspect and verify

```powershell
persistmind --repo . storage status
persistmind --repo . storage topology
persistmind --repo . storage verify --full
```

## Create and verify a backup

```powershell
persistmind --repo . storage backup create --verify
persistmind --repo . storage backup verify --backup <backup-id>
```

## Restore safely

```powershell
persistmind --repo . storage backup restore --backup <backup-id> --target <empty-path> --yes
```

Restore into an empty target, reopen it, verify integrity and expected task,
memory, audit, and source state, then decide whether a controlled replacement is
needed. Never delete or swap active database files while PersistMind processes
may be running.
