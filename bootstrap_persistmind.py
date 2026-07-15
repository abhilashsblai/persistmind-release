#!/usr/bin/env python3
"""Verified first-install bootstrap for PersistMind release wheels.

This file intentionally uses only the standard library until it creates the
private PersistMind environment. Release verification then runs inside that
environment with the pinned cryptography dependency.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import venv
import zipfile
from pathlib import Path
from typing import Any

REPOSITORY = "abhilashsblai/persistmind-release"
API_ROOT = "https://api.github.com"
MANIFEST_NAME = "persistmind-update-manifest.v2.json"
SIGNATURE_NAME = f"{MANIFEST_NAME}.sig"
ROOT_KEYS = (
    "2zTxhUn/x3MO0ju5mXYuEmbJfAGWj6BE9nWkgBb43do=",
    "kuh85P8eq5Qp1S4kIUJ2LoUfxZX+TbEstEaKgJtlV4A=",
)
MAX_METADATA_BYTES = 1_000_000
MAX_WHEEL_BYTES = 250_000_000
PRODUCT_ID = "c8ee8be4-1cc8-4e78-972f-c73f8615f2f7"


def main() -> None:
    parser = argparse.ArgumentParser(description="Install PersistMind from a verified GitHub release")
    parser.add_argument("--repo", default=".", help="project repository to configure")
    parser.add_argument(
        "--agents", help="comma-separated agent list; omit for an interactive prompt"
    )
    parser.add_argument("--channel", choices=("stable", "preview"), default="stable")
    parser.add_argument("--version", help="install an exact release version")
    parser.add_argument("--init-git", action="store_true")
    parser.add_argument("--skip-index", action="store_true")
    parser.add_argument("--reinstall", action="store_true")
    parser.add_argument("--local-wheel", help=argparse.SUPPRESS)
    parser.add_argument("--local-wheel-sha256", help=argparse.SUPPRESS)
    parser.add_argument("--internal", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if bool(args.local_wheel) != bool(args.local_wheel_sha256):
        raise SystemExit("local wheel testing requires both path and SHA-256")
    if args.local_wheel and not args.version:
        raise SystemExit("local wheel testing requires an exact version")
    if sys.version_info < (3, 11):
        raise SystemExit("PersistMind requires Python 3.11 or newer")
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        raise SystemExit(f"project repository does not exist: {repo}")
    environment = _environment_root()
    python = _venv_python(environment)
    if not args.internal:
        _prepare_environment(environment, python)
        command = [str(python), str(Path(__file__).resolve()), *sys.argv[1:], "--internal"]
        raise SystemExit(subprocess.call(command))
    if args.local_wheel:
        wheel = _verify_local_wheel(
            Path(args.local_wheel), str(args.version), str(args.local_wheel_sha256)
        )
        _install_wheel(python, wheel, reinstall=args.reinstall)
        installed_version = str(args.version).removeprefix("v")
    else:
        release = _resolve_release(args.channel, args.version)
        manifest_bytes = _asset_bytes(release, MANIFEST_NAME, MAX_METADATA_BYTES)
        signature = _asset_bytes(release, SIGNATURE_NAME, 16_384)
        manifest = _verify_manifest(
            release, manifest_bytes, signature, args.channel, args.version
        )
        artifact = _wheel_artifact(manifest)
        wheel = _download_wheel(release, artifact)
        try:
            _install_wheel(python, wheel, reinstall=args.reinstall)
        finally:
            shutil.rmtree(wheel.parent, ignore_errors=True)
        installed_version = str(manifest["version"])
    _write_launchers(environment, python)
    command = _project_install_command(python, repo, args)
    result = subprocess.call(command)
    if result:
        raise SystemExit(result)
    print(f"persistmind-bootstrap: installed PersistMind {installed_version}")
    print("persistmind-bootstrap: future updates: persistmind update")


def _project_install_command(
    python: Path, repo: Path, args: argparse.Namespace
) -> list[str]:
    command = [
        str(python),
        "-I",
        "-m",
        "persistmind",
        "--repo",
        str(repo),
        "install",
        "--runtime-executable",
        str(python.resolve()),
        "--runtime-prefix-arg=-I",
        "--runtime-prefix-arg=-m",
        "--runtime-prefix-arg=persistmind",
        "--runtime-source",
        "release-bootstrap",
    ]
    if args.agents:
        command.extend(["--agents", args.agents])
    if args.init_git:
        command.append("--init-git")
    if args.skip_index:
        command.append("--skip-index")
    return command


def _environment_root() -> Path:
    override = os.environ.get("PERSISTMIND_BOOTSTRAP_HOME")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "PersistMind" / "bootstrap"
    return (
        Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        / "persistmind"
        / "bootstrap"
    )


def _venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _prepare_environment(root: Path, python: Path) -> None:
    if not python.is_file():
        root.parent.mkdir(parents=True, exist_ok=True)
        venv.EnvBuilder(with_pip=True, clear=False).create(root)
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "cryptography==49.0.0",
            "packaging>=24",
        ],
        check=True,
    )


def _headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "persistmind-bootstrap/1"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _json(url: str) -> Any:
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=_headers()), timeout=30
        ) as response:
            data = response.read(MAX_METADATA_BYTES + 1)
    except urllib.error.HTTPError as exc:
        hint = (
            " Set GH_TOKEN for a private release repository." if exc.code in (401, 403, 404) else ""
        )
        raise SystemExit(f"GitHub release request failed ({exc.code}).{hint}") from exc
    if len(data) > MAX_METADATA_BYTES:
        raise SystemExit("GitHub release response exceeds the bootstrap size policy")
    return json.loads(data)


def _resolve_release(channel: str, exact: str | None) -> dict[str, Any]:
    if exact:
        tag = exact if exact.startswith("v") else f"v{exact}"
        value = _json(f"{API_ROOT}/repos/{REPOSITORY}/releases/tags/{urllib.parse.quote(tag)}")
    elif channel == "stable":
        value = _json(f"{API_ROOT}/repos/{REPOSITORY}/releases/latest")
    else:
        releases = _json(f"{API_ROOT}/repos/{REPOSITORY}/releases?per_page=100")
        values = [item for item in releases if not item.get("draft") and item.get("prerelease")]
        if not values:
            raise SystemExit("no published preview release is available")
        value = values[0]
    if not isinstance(value, dict) or value.get("draft"):
        raise SystemExit("GitHub returned an invalid release")
    return value


def _assets(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    values = release.get("assets")
    if not isinstance(values, list):
        raise SystemExit("release has no asset list")
    result = {str(item.get("name")): item for item in values if isinstance(item, dict)}
    if len(result) != len(values):
        raise SystemExit("release has invalid or duplicate asset names")
    return result


def _asset_bytes(release: dict[str, Any], name: str, maximum: int) -> bytes:
    asset = _assets(release).get(name)
    if not asset:
        raise SystemExit(f"release is missing {name}")
    request = urllib.request.Request(str(asset["browser_download_url"]), headers=_headers())
    with urllib.request.urlopen(request, timeout=60) as response:
        value = response.read(maximum + 1)
    if len(value) > maximum:
        raise SystemExit(f"release asset {name} exceeds the bootstrap size policy")
    return value


def _verify_manifest(
    release: dict[str, Any],
    document: bytes,
    encoded_signature: bytes,
    channel: str,
    exact: str | None,
) -> dict[str, Any]:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from packaging.specifiers import SpecifierSet
    from packaging.version import Version

    try:
        signature = base64.b64decode(encoded_signature.strip(), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SystemExit("release manifest signature is not valid base64") from exc
    for encoded_key in ROOT_KEYS:
        try:
            Ed25519PublicKey.from_public_bytes(base64.b64decode(encoded_key)).verify(
                signature, document
            )
            break
        except InvalidSignature:
            continue
    else:
        raise SystemExit("release manifest signature is not trusted")
    value = json.loads(document)
    required = {
        "schema_version",
        "repository",
        "release_tag",
        "version",
        "channel",
        "requires_python",
        "artifacts",
    }
    if not isinstance(value, dict) or not required.issubset(value):
        raise SystemExit("release manifest is incomplete")
    if (
        value["schema_version"] != "persistmind.update_manifest.v2"
        or value["repository"] != REPOSITORY
        or value.get("product_id") != PRODUCT_ID
    ):
        raise SystemExit("release manifest identity is invalid")
    if (
        value["release_tag"] != release.get("tag_name")
        or value["release_tag"] != f"v{value['version']}"
    ):
        raise SystemExit("release tag and manifest version disagree")
    version = Version(str(value["version"]))
    if exact and version != Version(exact.removeprefix("v")):
        raise SystemExit("GitHub returned a different release than requested")
    if not exact and channel == "stable" and version.is_prerelease:
        raise SystemExit("stable channel returned a prerelease")
    if value["channel"] != ("preview" if version.is_prerelease else "stable"):
        raise SystemExit("release channel and version disagree")
    if bool(release.get("prerelease")) != version.is_prerelease:
        raise SystemExit("GitHub prerelease state and manifest version disagree")
    if not SpecifierSet(str(value["requires_python"])).contains(
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        prereleases=True,
    ):
        raise SystemExit("this PersistMind release does not support the installed Python")
    return value


def _wheel_artifact(manifest: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        item for item in manifest["artifacts"] if str(item.get("filename", "")).endswith(".whl")
    ]
    if len(artifacts) != 1:
        raise SystemExit("release manifest must contain exactly one wheel")
    artifact = artifacts[0]
    filename = str(artifact["filename"])
    if Path(filename).name != filename:
        raise SystemExit("release wheel filename is unsafe")
    if int(artifact.get("size", 0)) <= 0 or int(artifact["size"]) > MAX_WHEEL_BYTES:
        raise SystemExit("release wheel size is invalid")
    if len(str(artifact.get("sha256", ""))) != 64:
        raise SystemExit("release wheel digest is invalid")
    return artifact


def _download_wheel(release: dict[str, Any], artifact: dict[str, Any]) -> Path:
    name = str(artifact["filename"])
    asset = _assets(release).get(name)
    if not asset or int(asset.get("size", -1)) != int(artifact["size"]):
        raise SystemExit("release wheel asset does not match its signed manifest")
    target = Path(tempfile.mkdtemp(prefix="persistmind-bootstrap-")) / name
    digest = hashlib.sha256()
    request = urllib.request.Request(str(asset["browser_download_url"]), headers=_headers())
    with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as handle:
        total = 0
        while block := response.read(1024 * 1024):
            total += len(block)
            if total > MAX_WHEEL_BYTES:
                raise SystemExit("release wheel exceeds the bootstrap size policy")
            digest.update(block)
            handle.write(block)
    if total != int(artifact["size"]) or digest.hexdigest() != artifact["sha256"]:
        raise SystemExit("release wheel failed SHA-256 verification")
    _verify_wheel_metadata(target, str(release["tag_name"]).removeprefix("v"))
    return target


def _verify_local_wheel(path: Path, version: str, expected_sha256: str) -> Path:
    target = path.expanduser().resolve()
    digest_text = expected_sha256.strip().casefold()
    if len(digest_text) != 64 or any(character not in "0123456789abcdef" for character in digest_text):
        raise SystemExit("local wheel SHA-256 is invalid")
    if not target.is_file() or target.suffix.casefold() != ".whl":
        raise SystemExit("local wheel does not exist or is not a wheel")
    if target.stat().st_size <= 0 or target.stat().st_size > MAX_WHEEL_BYTES:
        raise SystemExit("local wheel size is invalid")
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest_text:
        raise SystemExit("local wheel failed SHA-256 verification")
    _verify_wheel_metadata(target, version.removeprefix("v"))
    return target


def _verify_wheel_metadata(path: Path, version: str) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            metadata = [
                item for item in archive.namelist() if item.endswith(".dist-info/METADATA")
            ]
            contents = archive.read(metadata[0]) if len(metadata) == 1 else b""
    except (OSError, zipfile.BadZipFile) as exc:
        raise SystemExit("release wheel is not a valid wheel archive") from exc
    expected_version = f"Version: {version}\n".encode()
    if b"Name: persistmind\n" not in contents or expected_version not in contents:
        raise SystemExit("release wheel metadata is invalid")


def _install_wheel(python: Path, wheel: Path, *, reinstall: bool) -> None:
    command = [str(python), "-m", "pip", "install", "--disable-pip-version-check", "--upgrade"]
    if reinstall:
        command.append("--force-reinstall")
    subprocess.run([*command, str(wheel)], check=True)


def _write_launchers(environment: Path, python: Path) -> None:
    bin_dir = _user_bin()
    bin_dir.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        launcher = bin_dir / "persistmind.cmd"
        launcher.write_text(
            f'@echo off\r\n"{python}" -I -m persistmind %*\r\n',
            encoding="utf-8",
        )
        _ensure_windows_path(bin_dir)
    else:
        launcher = bin_dir / "persistmind"
        launcher.write_text(
            "#!/bin/sh\nexec "
            + shlex.quote(str(python.resolve()))
            + ' -I -m persistmind "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)
    print(f"persistmind-bootstrap: launcher {launcher}")


def _user_bin() -> Path:
    if os.name == "nt":
        return (
            Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
            / "persistmind"
            / "bin"
        )
    return Path.home() / ".local" / "bin"


def _ensure_windows_path(bin_dir: Path) -> None:
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
        current, _ = (
            winreg.QueryValueEx(key, "Path") if _registry_value_exists(key, "Path") else ("", 1)
        )
        entries = [item for item in str(current).split(";") if item]
        if str(bin_dir).lower() not in {item.lower() for item in entries}:
            winreg.SetValueEx(
                key, "Path", 0, winreg.REG_EXPAND_SZ, ";".join([*entries, str(bin_dir)])
            )


def _registry_value_exists(key: Any, name: str) -> bool:
    import winreg

    try:
        winreg.QueryValueEx(key, name)
        return True
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    main()
