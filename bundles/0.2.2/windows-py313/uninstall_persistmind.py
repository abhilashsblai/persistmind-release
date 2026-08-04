#!/usr/bin/env python3
"""Remove PersistMind and legacy PersistMind state, surfaces, and packages.

The default mode is a read-only dry run. Destructive changes require both
``--execute`` and ``--yes``. The script intentionally uses only the Python
standard library so it still works when the persistmind package is damaged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


CONTRACT_MARKERS = (
    "<!-- persistmind-agent-contract -->",
    "<!-- persistmind-agent-contract -->",
)
KEYRING_SERVICES = ("persistmind.storage.kek.v1",)
SKIP_SEARCH_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
}


def persistmind_home(env: dict[str, str] | None = None) -> Path:
    values = os.environ if env is None else env
    if values.get("PERSISTMIND_HOME"):
        return Path(values["PERSISTMIND_HOME"]).expanduser().resolve()
    if values.get("PERSISTMIND_HOME"):
        return Path(values["PERSISTMIND_HOME"]).expanduser().resolve()
    if os.name == "nt" and values.get("APPDATA"):
        canonical = (Path(values["APPDATA"]) / "PersistMind").resolve()
        legacy = (Path(values["APPDATA"]) / "persistmind").resolve()
    else:
        canonical = (Path.home() / ".persistmind").resolve()
        legacy = (Path.home() / ".persistmind").resolve()
    return canonical if canonical.exists() or not legacy.exists() else legacy


def global_homes(env: dict[str, str] | None = None) -> set[Path]:
    values = os.environ if env is None else env
    homes = {persistmind_home(values)}
    for name in ("PERSISTMIND_HOME", "PERSISTMIND_HOME"):
        if values.get(name):
            homes.add(Path(values[name]).expanduser().resolve())
    if os.name == "nt" and values.get("APPDATA"):
        homes.update(
            {
                (Path(values["APPDATA"]) / "PersistMind").resolve(),
                (Path(values["APPDATA"]) / "persistmind").resolve(),
            }
        )
    if os.name == "nt" and values.get("LOCALAPPDATA"):
        homes.update(
            {
                (Path(values["LOCALAPPDATA"]) / "PersistMind").resolve(),
                (Path(values["LOCALAPPDATA"]) / "persistmind").resolve(),
            }
        )
    homes.update({Path.home() / ".persistmind"})
    return {path.resolve() for path in homes}


def registered_projects(home: Path) -> set[Path]:
    path = home / "projects.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return set()
    projects = value.get("projects") if isinstance(value, dict) else None
    if not isinstance(projects, dict):
        return set()
    result: set[Path] = set()
    for key, record in projects.items():
        raw = record.get("path") if isinstance(record, dict) else key
        if raw:
            result.add(Path(str(raw)).expanduser().resolve())
    return result


def search_projects(roots: Iterable[Path]) -> set[Path]:
    """Find project roots containing PersistMind or legacy project state."""
    found: set[Path] = set()
    for root in roots:
        root = root.expanduser().resolve()
        if not root.is_dir():
            continue
        for current, dirs, _files in os.walk(root, followlinks=False):
            dirs[:] = [name for name in dirs if name not in SKIP_SEARCH_DIRS]
            if ".persistmind" in dirs:
                found.add(Path(current).resolve())
                for state_dir in (".persistmind",):
                    if state_dir in dirs:
                        dirs.remove(state_dir)
    return found


def _toml(repo: Path) -> dict[str, Any]:
    try:
        path = repo / "persistmind.toml"
        if not path.exists():
            path = repo / "persistmind.toml"
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def is_persistmind_source_checkout(repo: Path) -> bool:
    try:
        value = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return False
    project = value.get("project") if isinstance(value, dict) else None
    name = str(project.get("name") or "") if isinstance(project, dict) else ""
    return name.casefold() in {"persistmind", "persistmind", "advanced-persistmind"}


def project_data_paths(repo: Path) -> tuple[set[Path], set[Path]]:
    """Return (workspace paths, separately configured archive paths)."""
    config = _toml(repo)
    toolchain = config.get("persistmind") if isinstance(config.get("persistmind"), dict) else {}
    if isinstance(config.get("persistmind"), dict):
        toolchain = {**toolchain, **config["persistmind"]}
    default_workspace = ".persistmind"
    workspace_value = str(toolchain.get("workspace_dir") or default_workspace)
    workspace = Path(workspace_value).expanduser()
    if not workspace.is_absolute():
        workspace = repo / workspace

    archives: set[Path] = set()
    maintenance = config.get("maintenance")
    if not isinstance(maintenance, dict):
        maintenance = toolchain.get("maintenance") if isinstance(toolchain, dict) else None
    if isinstance(maintenance, dict) and maintenance.get("cold_archive_path"):
        archive = Path(str(maintenance["cold_archive_path"])).expanduser()
        if not archive.is_absolute():
            archive = repo / archive
        archives.add(archive.resolve())

    anticipation = config.get("anticipation")
    transfer = anticipation.get("transfer") if isinstance(anticipation, dict) else None
    if isinstance(transfer, dict):
        library = str(transfer.get("library") or "user")
        if library not in {"", "user", "off"}:
            candidate = Path(library).expanduser()
            if not candidate.is_absolute():
                candidate = repo / candidate
            archives.add(candidate.resolve())
    return {
        workspace.resolve(),
        (repo / ".persistmind").resolve(),
        (repo / ".persistmind").resolve(),
    }, archives


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def _safe_recursive_target(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    anchor = Path(resolved.anchor)
    return resolved != anchor and resolved != Path.home().resolve()


@dataclass
class Cleaner:
    execute: bool
    include_external_paths: bool = False
    actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    @property
    def prefix(self) -> str:
        return "REMOVE" if self.execute else "WOULD REMOVE"

    def remove(self, path: Path, *, recursive: bool = False, scope: Path | None = None) -> None:
        path = Path(os.path.abspath(path.expanduser()))
        if not path.exists() and not path.is_symlink():
            return
        if recursive and not _safe_recursive_target(path):
            self.warnings.append(f"refused unsafe recursive target: {path}")
            return
        if scope is not None and not _within(path, scope) and not self.include_external_paths:
            self.warnings.append(f"external path skipped (use --include-external-paths): {path}")
            return
        self.actions.append(f"{self.prefix}: {path}")
        if not self.execute:
            return
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)
        except OSError as exc:
            self.failures.append(f"failed to remove {path}: {exc}")

    def prune_empty(self, path: Path) -> None:
        path = Path(os.path.abspath(path.expanduser()))
        if not path.is_dir():
            return
        try:
            empty = next(path.iterdir(), None) is None
        except OSError:
            return
        if not empty:
            return
        self.actions.append(f"{self.prefix}: empty directory {path}")
        if self.execute:
            try:
                path.rmdir()
            except OSError as exc:
                self.failures.append(f"failed to remove empty directory {path}: {exc}")

    def remove_owned_workspace(self, path: Path, *, scope: Path | None = None) -> None:
        path = Path(os.path.abspath(path.expanduser()))
        if not path.exists() and not path.is_symlink():
            return
        if scope is not None and not _within(path, scope) and not self.include_external_paths:
            self.warnings.append(f"external path skipped (use --include-external-paths): {path}")
            return
        try:
            entries = _verified_workspace_entries(path)
        except (OSError, RuntimeError, ValueError) as exc:
            self.warnings.append(
                f"workspace ownership verification failed; preserved {path}: {exc}"
            )
            return
        ordered = sorted(entries, key=lambda item: (len(item.parts), item.as_posix()), reverse=True)
        for relative in ordered:
            target = path / relative
            self.actions.append(f"{self.prefix}: {target}")
            if not self.execute:
                continue
            try:
                if target.is_symlink():
                    raise RuntimeError(f"journaled entry became a symlink: {relative.as_posix()}")
                if target.is_file():
                    target.unlink()
                elif target.is_dir():
                    target.rmdir()
            except (OSError, RuntimeError) as exc:
                self.failures.append(f"failed to remove journaled workspace entry {target}: {exc}")
                return
        self.actions.append(f"{self.prefix}: {path}")
        if self.execute:
            try:
                path.rmdir()
            except OSError as exc:
                self.failures.append(f"failed to remove empty owned workspace {path}: {exc}")

    def write_text(self, path: Path, content: str, reason: str) -> None:
        self.actions.append(f"{'EDIT' if self.execute else 'WOULD EDIT'}: {path} ({reason})")
        if not self.execute:
            return
        try:
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            self.failures.append(f"failed to edit {path}: {exc}")

    def restore(self, path: Path, backup: Path, *, scope: Path | None = None) -> None:
        path = Path(os.path.abspath(path.expanduser()))
        backup = backup.expanduser().resolve()
        if scope is not None and not _within(path, scope) and not self.include_external_paths:
            self.warnings.append(f"external restore skipped (use --include-external-paths): {path}")
            return
        self.actions.append(
            f"{'RESTORE' if self.execute else 'WOULD RESTORE'}: {path} from {backup}"
        )
        if not self.execute:
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)
        except OSError as exc:
            self.failures.append(f"failed to restore {path} from {backup}: {exc}")

    def run(self, command: list[str], label: str) -> None:
        rendered = subprocess.list2cmdline(command)
        self.actions.append(f"{'RUN' if self.execute else 'WOULD RUN'}: {rendered} ({label})")
        if not self.execute:
            return
        try:
            result = subprocess.run(command, text=True, check=False)
        except OSError as exc:
            self.warnings.append(f"could not run {rendered}: {exc}")
            return
        if result.returncode:
            self.failures.append(f"command exited {result.returncode}: {rendered}")


def remove_ctx_toml_table(text: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped in {"[mcp_servers.persistmind]"}:
            skipping = True
            while output and not output[-1].strip():
                output.pop()
            continue
        if skipping and stripped.startswith("[") and stripped.endswith("]"):
            skipping = False
        if not skipping:
            output.append(line)
    return "".join(output).rstrip() + ("\n" if output else "")


def clean_toml_mcp(cleaner: Cleaner, path: Path) -> None:
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    after = remove_ctx_toml_table(before)
    if after == before:
        return
    if after.strip():
        cleaner.write_text(path, after, "remove PersistMind MCP tables")
    else:
        cleaner.remove(path)


def clean_json_mcp(cleaner: Cleaner, path: Path) -> None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return
    if not isinstance(value, dict):
        return
    servers = value.get("mcpServers")
    if not isinstance(servers, dict) or not ({"persistmind"} & set(servers)):
        return
    servers.pop("persistmind", None)
    servers.pop("persistmind", None)
    if not servers:
        value.pop("mcpServers", None)
    if value:
        cleaner.write_text(
            path,
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            "remove PersistMind MCP server",
        )
    else:
        cleaner.remove(path)


def clean_instruction_file(cleaner: Cleaner, path: Path) -> None:
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    offsets = [before.find(marker) for marker in CONTRACT_MARKERS]
    offsets = [offset for offset in offsets if offset >= 0]
    if not offsets:
        after = before
        if (
            after.startswith("# Agent Usage Contract") and "must activate PersistMind" in after
        ) or (after.startswith("@AGENTS.md") and "PersistMind MCP/context workflow" in after):
            cleaner.remove(path)
            return
        heading = "## PersistMind"
        start = after.find(heading)
        if start >= 0 and "persistmind --repo" in after[start:]:
            end = after.find("\n## ", start + len(heading))
            if end >= 0:
                after = after[:start].rstrip() + "\n\n" + after[end + 1 :]
        after = after.replace(
            "`.git/`, `.persistmind/`, `.codex/`, `.claude/`, or",
            "`.git/`, `.codex/`, `.claude/`, or",
        )
        legacy_intro = (
            "This workspace uses **the PersistMind as its single source of project memory**"
        )
        if legacy_intro in after and "## Memory (PersistMind only)" in after:
            start = after.find(legacy_intro)
            end = after.find("## Skills", start)
            if end >= 0:
                after = after[:start].rstrip() + "\n\n" + after[end:]
        legacy_learning = "### Correction-learning memory"
        start = after.find(legacy_learning)
        if start >= 0 and "save the reusable lesson to the PersistMind" in after[start:]:
            after = after[:start].rstrip() + "\n"
        if after != before:
            cleaner.write_text(path, after, "remove legacy CTX instruction blocks")
        return
    offset = min(offsets)
    cleaner.warnings.append(
        f"{path}: PersistMind has no end marker; cleanup removes content from its marker to EOF"
    )
    after = before[:offset].rstrip()
    if after:
        cleaner.write_text(
            path, after + "\n", "remove PersistMind agent contract from marker to EOF"
        )
    else:
        cleaner.remove(path)


def clean_gitignore(cleaner: Cleaner, path: Path) -> None:
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    lines = before.splitlines()
    after_lines = [line for line in lines if line.strip() not in {".persistmind/"}]
    if after_lines == lines:
        return
    if after_lines:
        cleaner.write_text(
            path,
            "\n".join(after_lines).rstrip() + "\n",
            "remove PersistMind ignore entries",
        )
    else:
        cleaner.remove(path)


def clean_claude_settings(cleaner: Cleaner, path: Path) -> None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return
    if not isinstance(value, dict) or not isinstance(value.get("hooks"), dict):
        return
    hooks = value["hooks"]
    changed = False
    for event in list(hooks):
        groups = hooks[event]
        if not isinstance(groups, list):
            continue
        kept = [
            group
            for group in groups
            if not any(brand in json.dumps(group).casefold() for brand in ("persistmind",))
        ]
        if kept != groups:
            changed = True
            if kept:
                hooks[event] = kept
            else:
                del hooks[event]
    if not changed:
        return
    if not hooks:
        value.pop("hooks", None)
    if value:
        cleaner.write_text(
            path,
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            "remove PersistMind Claude hooks",
        )
    else:
        cleaner.remove(path)


def clean_gemini_settings(cleaner: Cleaner, path: Path) -> None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return
    if not isinstance(value, dict):
        return
    changed = False
    servers = value.get("mcpServers")
    if isinstance(servers, dict) and "persistmind" in servers:
        servers.pop("persistmind", None)
        changed = True
        if not servers:
            value.pop("mcpServers", None)
    hooks = value.get("hooks")
    if isinstance(hooks, dict):
        for event in list(hooks):
            groups = hooks[event]
            if not isinstance(groups, list):
                continue
            kept = [
                group
                for group in groups
                if "persistmind" not in json.dumps(group, sort_keys=True).casefold()
            ]
            if kept != groups:
                changed = True
                if kept:
                    hooks[event] = kept
                else:
                    hooks.pop(event, None)
        if not hooks:
            value.pop("hooks", None)
    if not changed:
        return
    if value:
        cleaner.write_text(
            path,
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            "remove PersistMind Gemini hooks and MCP server",
        )
    else:
        cleaner.remove(path)


def remove_owned_plugin(cleaner: Cleaner, root: Path, *, scope: Path) -> None:
    ownership = root / ".persistmind-plugin-ownership.json"
    try:
        value = json.loads(ownership.read_text(encoding="utf-8"))
        records = value.get("files") if isinstance(value, dict) else None
    except (OSError, UnicodeError, json.JSONDecodeError):
        return
    if (
        not isinstance(value, dict)
        or value.get("schema_version") != "persistmind.plugin_ownership.v1"
        or not isinstance(records, list)
    ):
        return
    expected: dict[str, str] = {}
    for record in records:
        if not isinstance(record, dict) or not record.get("path") or not record.get("sha256"):
            return
        expected[str(record["path"])] = str(record["sha256"])
    current = {
        path.relative_to(root).as_posix(): _file_sha256(path)
        for path in root.rglob("*")
        if path.is_file() and path != ownership
    }
    if current != expected:
        cleaner.warnings.append(f"modified or unowned plugin files preserved for review: {root}")
        return
    cleaner.remove(root, recursive=True, scope=scope)


def clean_project_surfaces(cleaner: Cleaner, repo: Path) -> None:
    clean_instruction_file(cleaner, repo / "AGENTS.md")
    clean_instruction_file(cleaner, repo / "CLAUDE.md")
    clean_instruction_file(cleaner, repo / "GEMINI.md")
    clean_gitignore(cleaner, repo / ".gitignore")

    codex_config = repo / ".codex" / "config.toml"
    try:
        generated_codex = codex_config.read_text(encoding="utf-8").startswith(
            ("# Generated by PersistMind.", "# Generated by PersistMind.")
        )
    except (OSError, UnicodeError):
        generated_codex = False
    if generated_codex:
        cleaner.remove(codex_config)
    else:
        clean_toml_mcp(cleaner, codex_config)
    hooks_json = repo / ".codex" / "hooks.json"
    try:
        if any(
            brand in hooks_json.read_text(encoding="utf-8").casefold() for brand in ("persistmind",)
        ):
            cleaner.remove(hooks_json)
    except (OSError, UnicodeError):
        pass
    for wrapper_name in (
        "persistmind-hook.ps1",
        "persistmind-hook.sh",
        "persistmind-hook.ps1",
        "persistmind-hook.sh",
    ):
        cleaner.remove(repo / ".codex" / wrapper_name)
    for name in (
        "persistmind-explorer",
        "persistmind-worker",
        "persistmind-reviewer",
        "persistmind-verifier",
        "ctx-explorer",
        "ctx-worker",
        "ctx-reviewer",
        "ctx-verifier",
    ):
        cleaner.remove(repo / ".codex" / "agents" / f"{name}.toml")
        cleaner.remove(repo / ".claude" / "agents" / f"{name}.md")

    clean_claude_settings(cleaner, repo / ".claude" / "settings.json")
    cleaner.remove(repo / ".claude" / "skills" / "persistmind-loop", recursive=True, scope=repo)
    cleaner.remove(repo / ".claude" / "skills" / "ctx-loop", recursive=True, scope=repo)
    cleaner.remove(repo / ".agents" / "skills" / "persistmind-loop", recursive=True, scope=repo)
    cleaner.remove(repo / ".agents" / "skills" / "ctx-loop", recursive=True, scope=repo)
    cursor_rule = repo / ".cursor" / "rules" / "persistmind.mdc"
    try:
        cursor_text = cursor_rule.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        cursor_text = ""
    if (
        "<!-- persistmind-agent-contract -->" in cursor_text
        and "## Cursor Enforcement Note" in cursor_text
    ):
        cleaner.remove(cursor_rule)
    clean_json_mcp(cleaner, repo / ".cursor" / "mcp.json")
    clean_gemini_settings(cleaner, repo / ".gemini" / "settings.json")
    remove_owned_plugin(
        cleaner,
        repo / ".grok" / "plugins" / "persistmind",
        scope=repo,
    )
    clean_json_mcp(cleaner, repo / ".mcp.json")
    cleaner.remove(repo / "persistmind.toml")
    cleaner.remove(repo / "persistmind.toml")

    package_json = repo / "package.json"
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        package = None
    if isinstance(package, dict):
        installed_names = sorted(
            {
                name
                for group in ("dependencies", "devDependencies", "optionalDependencies")
                if isinstance(package.get(group), dict)
                for name in ("@persistmind/cli",)
                if name in package[group]
            }
        )
        npm = shutil.which("npm.cmd" if os.name == "nt" else "npm") or shutil.which("npm")
        if installed_names and npm:
            for group in ("dependencies", "devDependencies", "optionalDependencies"):
                values = package.get(group)
                if not isinstance(values, dict):
                    continue
                for name in installed_names:
                    values.pop(name, None)
                if not values:
                    package.pop(group, None)
            cleaner.write_text(
                package_json,
                json.dumps(package, indent=2) + "\n",
                "remove project-local CLI dependency",
            )
            cleaner.run(
                [
                    npm,
                    "--prefix",
                    str(repo),
                    "install",
                    "--package-lock-only",
                    "--ignore-scripts",
                ],
                "refresh package lock after removing project-local CLI dependency",
            )
            lock_path = repo / "package-lock.json"
            try:
                lock = json.loads(lock_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                lock = None
            if isinstance(lock, dict):
                packages = lock.get("packages")
                if isinstance(packages, dict):
                    for key, value in list(packages.items()):
                        if key in {f"node_modules/{name}" for name in installed_names} or (
                            isinstance(value, dict) and value.get("name") in installed_names
                        ):
                            packages.pop(key, None)
                dependencies = lock.get("dependencies")
                if isinstance(dependencies, dict):
                    for name in installed_names:
                        dependencies.pop(name, None)
                cleaner.write_text(
                    lock_path,
                    json.dumps(lock, indent=2) + "\n",
                    "remove stale project-local CLI lock entries",
                )

    for capabilities, schema in (
        (repo / "persistmind.capabilities.yaml", "persistmind.capabilities.v1"),
        (repo / "persistmind.capabilities.yaml", "persistmind.capabilities.v1"),
    ):
        try:
            if f"schema_version: {schema}" in capabilities.read_text(encoding="utf-8"):
                cleaner.remove(capabilities)
        except (OSError, UnicodeError):
            pass
    verifier = repo / "tools" / "verify-production-assets.mjs"
    try:
        verifier_text = verifier.read_text(encoding="utf-8")
        if (
            "Production asset verification failed" in verifier_text
            and ".next/standalone/.next/static" in verifier_text
        ):
            cleaner.remove(verifier)
    except (OSError, UnicodeError):
        pass

    for hook_name in ("pre-commit", "post-commit"):
        hook = repo / ".git" / "hooks" / hook_name
        try:
            if any(
                brand in hook.read_text(encoding="utf-8").casefold() for brand in ("persistmind",)
            ):
                cleaner.remove(hook)
        except (OSError, UnicodeError):
            pass

    git = shutil.which("git")
    if git and (repo / ".git").exists():
        for notes_ref in ("refs/notes/persistmind",):
            probe = subprocess.run(
                [git, "-C", str(repo), "show-ref", "--verify", "--quiet", notes_ref],
                check=False,
            )
            if probe.returncode == 0:
                cleaner.run(
                    [git, "-C", str(repo), "update-ref", "-d", notes_ref],
                    "remove PersistMind audit Git-notes ref",
                )
                cleaner.warnings.append(
                    f"{repo}: deleted Git-notes ref; unreachable Git objects remain until normal Git GC"
                )

    for path in (
        repo / ".codex" / "agents",
        repo / ".claude" / "agents",
        repo / ".claude" / "skills",
        repo / ".cursor" / "rules",
        repo / ".gemini",
        repo / ".grok" / "plugins",
        repo / ".grok",
        repo / ".codex",
        repo / ".claude",
        repo / ".cursor",
        repo / "tools",
    ):
        cleaner.prune_empty(path)


def clean_manifest_surfaces(cleaner: Cleaner, repo: Path, workspaces: Iterable[Path]) -> bool:
    manifest_path = next(
        (
            workspace / "installation.json"
            for workspace in workspaces
            if (workspace / "installation.json").is_file()
        ),
        None,
    )
    if manifest_path is None:
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        cleaner.warnings.append(f"installation manifest is unreadable: {manifest_path}")
        return False
    if not isinstance(manifest, dict) or manifest.get("schema_version") not in {
        "persistmind.installation.v1",
        "persistmind.installation.v1",
    }:
        cleaner.warnings.append(f"unsupported installation manifest: {manifest_path}")
        return False
    records = manifest.get("owned_surfaces")
    if not isinstance(records, list):
        cleaner.warnings.append(f"installation manifest has no surface inventory: {manifest_path}")
        return False
    allowed_backup_roots = {(home / "install-backups").resolve() for home in global_homes()}
    for record in records:
        if not isinstance(record, dict) or not record.get("path"):
            continue
        path = Path(str(record["path"])).expanduser()
        if not path.is_absolute():
            cleaner.warnings.append(f"relative owned surface refused: {path}")
            continue
        after = str(record.get("after_sha256") or "")
        current = _file_sha256(path) if path.is_file() else None
        if current is None:
            continue
        if after and current != after:
            cleaner.warnings.append(f"user-modified owned surface preserved for review: {path}")
            continue
        if bool(record.get("created")):
            cleaner.remove(path, scope=repo)
            continue
        if bool(record.get("modified")) and record.get("backup"):
            backup = Path(str(record["backup"])).expanduser().resolve()
            if (
                not any(_within(backup, root) for root in allowed_backup_roots)
                or not backup.is_file()
            ):
                cleaner.warnings.append(f"owned-surface backup is unavailable or unsafe: {backup}")
                continue
            cleaner.restore(path, backup, scope=repo)
    return True


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def keyring_accounts(repo: Path, workspaces: Iterable[Path]) -> set[str]:
    accounts: set[str] = set()
    for workspace in workspaces:
        fingerprint = hashlib.sha256(str(workspace.resolve()).encode("utf-8")).hexdigest()
        key_ids = {f"workspace-kek-v1-{fingerprint[:16]}"}
        if workspace.is_dir():
            for path in workspace.rglob("*.json"):
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    continue
                for token in text.replace('"', " ").replace("'", " ").split():
                    token = token.strip(" ,:{}[]")
                    if token.startswith("workspace-kek-"):
                        key_ids.add(token)
        accounts.update(f"{fingerprint}:{key_id}" for key_id in key_ids)
    return accounts


def remove_keyring_accounts(cleaner: Cleaner, accounts: set[str]) -> None:
    if not accounts:
        return
    if not cleaner.execute:
        for service in KEYRING_SERVICES:
            for account in sorted(accounts):
                cleaner.actions.append(f"WOULD DELETE KEYRING: {service} / {account}")
        return
    try:
        import keyring  # type: ignore[import-not-found]
    except ImportError:
        cleaner.warnings.append(
            "keyring package unavailable; OS credential entries were not removed"
        )
        return
    for service in KEYRING_SERVICES:
        for account in sorted(accounts):
            try:
                if keyring.get_password(service, account) is not None:
                    keyring.delete_password(service, account)
                    cleaner.actions.append(f"DELETE KEYRING: {service} / {account}")
            except Exception as exc:  # keyring backends expose environment-specific errors.
                cleaner.warnings.append(
                    f"could not delete keyring account {service} / {account}: {exc}"
                )


def clean_project(cleaner: Cleaner, repo: Path, *, remove_surfaces: bool) -> set[str]:
    repo = repo.expanduser().resolve()
    if not repo.exists():
        cleaner.warnings.append(f"registered project no longer exists: {repo}")
        return set()
    workspaces, archives = project_data_paths(repo)
    accounts = keyring_accounts(repo, workspaces)
    source_checkout = is_persistmind_source_checkout(repo)
    if remove_surfaces and source_checkout:
        cleaner.warnings.append(
            f"PersistMind source checkout detected; preserving source-owned surfaces: {repo}"
        )
    if remove_surfaces and not source_checkout:
        used_manifest = clean_manifest_surfaces(cleaner, repo, workspaces)
        if not used_manifest:
            clean_project_surfaces(cleaner, repo)
    for archive in sorted(archives):
        cleaner.remove(archive, recursive=archive.is_dir(), scope=repo)
    for workspace in sorted(workspaces):
        cleaner.remove_owned_workspace(workspace, scope=repo)
    return accounts


def _verified_workspace_entries(workspace: Path) -> list[Path]:
    if workspace.is_symlink() or not workspace.is_dir():
        raise RuntimeError("workspace is not a regular directory")
    marker_path = workspace / ".persistmind-install-owner.json"
    installation_path = workspace / "installation.json"
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    installation = json.loads(installation_path.read_text(encoding="utf-8"))
    binding = installation.get("workspace_ownership") if isinstance(installation, dict) else None
    if not isinstance(marker, dict) or not isinstance(binding, dict):
        raise RuntimeError("ownership marker or installation binding is invalid")
    for key in ("transaction_id", "nonce"):
        if not marker.get(key) or marker.get(key) != binding.get(key):
            raise RuntimeError(f"ownership {key} does not match")
    if binding.get("created_root") is not True:
        raise RuntimeError("installation does not own creation of the workspace root")
    if Path(str(marker.get("workspace") or "")).resolve() != workspace.resolve():
        raise RuntimeError("ownership marker names a different workspace")
    journal_path = Path(str(binding.get("journal") or "")).expanduser().resolve()
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    if not isinstance(journal, dict) or journal.get("status") != "committed":
        raise RuntimeError("ownership journal is missing or not committed")
    if any(journal.get(field) != marker.get(field) for field in ("transaction_id", "nonce")):
        raise RuntimeError("ownership journal does not match the marker")
    owned = journal.get("owned_entries")
    if not isinstance(owned, dict) or not owned:
        raise RuntimeError("ownership journal has no itemized entries")
    current: set[str] = set()
    for item in workspace.rglob("*"):
        if item.is_symlink():
            raise RuntimeError(f"workspace contains a symlink: {item.relative_to(workspace)}")
        current.add(item.relative_to(workspace).as_posix())
    unknown = sorted(current - set(owned))
    if unknown:
        raise RuntimeError("workspace contains unjournaled entries: " + ", ".join(unknown))
    return [Path(value) for value in current]


def clean_global_state(cleaner: Cleaner, home: Path, *, clean_codex_config: bool = True) -> None:
    if clean_codex_config:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        clean_toml_mcp(cleaner, codex_home.expanduser() / "config.toml")
    candidates = global_homes() | {home.resolve()}
    for path in sorted(candidates):
        cleaner.remove(path, recursive=True)
    pattern_override = os.environ.get("PERSISTMIND_PATTERN_LIBRARY") or os.environ.get(
        "PERSISTMIND_PATTERN_LIBRARY"
    )
    if pattern_override:
        pattern_path = Path(pattern_override).expanduser()
        if pattern_path != Path(os.devnull):
            cleaner.remove(
                pattern_path,
                recursive=pattern_path.is_dir(),
                scope=Path.home(),
            )


def uninstall_packages(cleaner: Cleaner) -> None:
    cleaner.run(
        [
            sys.executable,
            "-m",
            "pip",
            "uninstall",
            "-y",
            "persistmind",
            "persistmind",
        ],
        "current Python environment",
    )
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm") or shutil.which("npm")
    if npm:
        cleaner.run([npm, "uninstall", "--global", "@persistmind/cli"], "global npm wrapper")
        cleaner.run([npm, "uninstall", "--global", "@persistmind/cli"], "global npm wrapper")
        if os.name == "nt" and os.environ.get("APPDATA"):
            npm_prefix = Path(os.environ["APPDATA"]) / "npm"
            for command in ("persistmind", "persistmind-mcp", "persistmind", "persistmind-mcp"):
                for suffix in ("", ".cmd", ".ps1"):
                    cleaner.remove(npm_prefix / f"{command}{suffix}")
    else:
        cleaner.warnings.append("npm not found; global @persistmind/cli package was not checked")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Completely remove PersistMind and legacy PersistMind. Defaults to a read-only dry run."
    )
    result.add_argument("--execute", action="store_true", help="perform the reported removals")
    result.add_argument("--yes", action="store_true", help="confirm destructive system cleanup")
    result.add_argument(
        "--project",
        action="append",
        default=[],
        type=Path,
        help="additional project root (repeatable)",
    )
    result.add_argument(
        "--search-root",
        action="append",
        default=[],
        type=Path,
        help="recursively discover unregistered .persistmind projects",
    )
    result.add_argument(
        "--no-registered-projects",
        action="store_true",
        help="do not read projects from the global registry",
    )
    result.add_argument(
        "--memory-only",
        action="store_true",
        help="remove project/global memory but keep agent files and packages",
    )
    result.add_argument(
        "--keep-global",
        action="store_true",
        help="keep registry, updater cache, engines, and global memories",
    )
    result.add_argument(
        "--keep-packages", action="store_true", help="do not uninstall pip/npm packages"
    )
    result.add_argument(
        "--include-external-paths",
        action="store_true",
        help="allow configured workspace/archive paths outside project roots",
    )
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.execute and not args.yes:
        print("error: --execute requires --yes", file=sys.stderr)
        return 2

    home = persistmind_home()
    projects = {path.expanduser().resolve() for path in args.project}
    if not args.no_registered_projects:
        for candidate_home in global_homes():
            projects.update(registered_projects(candidate_home))
    projects.update(search_projects(args.search_root))

    current = Path.cwd().resolve()
    if (current / ".persistmind").is_dir():
        projects.add(current)

    cleaner = Cleaner(
        execute=args.execute,
        include_external_paths=args.include_external_paths,
    )
    accounts: set[str] = set()
    for repo in sorted(projects):
        accounts.update(clean_project(cleaner, repo, remove_surfaces=not args.memory_only))
    remove_keyring_accounts(cleaner, accounts)

    if not args.keep_global:
        clean_global_state(cleaner, home, clean_codex_config=not args.memory_only)
    if not args.memory_only and not args.keep_packages:
        uninstall_packages(cleaner)

    mode = "EXECUTION" if args.execute else "DRY RUN"
    print(f"PersistMind uninstall {mode}")
    print(f"Global home: {home}")
    print(f"Projects discovered: {len(projects)}")
    for project in sorted(projects):
        print(f"  {project}")
    for action in cleaner.actions:
        print(action)
    for warning in cleaner.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for failure in cleaner.failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    if not projects:
        print(
            "WARNING: no projects discovered; pass --project or --search-root for unregistered installations.",
            file=sys.stderr,
        )
    if not args.execute:
        print("No changes were made. Review the plan, then rerun with --execute --yes.")
    return 1 if cleaner.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
