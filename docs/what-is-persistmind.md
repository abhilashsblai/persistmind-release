# What is PersistMind?

PersistMind is a local-first project intelligence and governance layer for AI
coding agents. It helps an agent build an identified view of a repository,
retrieve task-relevant context, remember approved knowledge, evaluate change
impact, and preserve evidence across sessions.

PersistMind does not replace Git, the editor, the coding agent, tests, or human
review. It connects those activities through a durable workflow:

- repository state is indexed into a snapshot;
- relevant context is compiled with provenance and a budget;
- tasks, plans, checkpoints, and scope are recorded;
- verification is linked to the actual change; and
- reviewed outcomes can inform future local memory.

The current release supports only the [Core Local](core-local.md) boundary. Code
for a broader capability does not imply that the capability is enabled,
qualified, or authoritative.
