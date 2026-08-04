#!/usr/bin/env python3
"""Verified first-install bootstrap for PersistMind release wheels.

This file intentionally uses only the standard library. It verifies Ed25519
release metadata before installing a hash-locked wheelhouse offline.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import re
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPOSITORY = "abhilashsblai/persistmind-release"  # legacy v2/v3 manifest identity
SOURCE_REPOSITORY = "abhilashsblai/PersistMind"
RELEASE_DRIVE_FOLDER_ID = "1aOOJ7fEE9Bv8yS-jzFVvTuBwlx0q7Nz9"
API_ROOT = "https://api.github.com"
MANIFEST_NAME = "persistmind-update-manifest.v2.json"
SIGNATURE_NAME = f"{MANIFEST_NAME}.sig"
MANIFEST_V3_NAME = "persistmind-update-manifest.v3.json"
SIGNATURE_V3_NAME = f"{MANIFEST_V3_NAME}.sig"
MANIFEST_V4_NAME = "persistmind-update-manifest.v4.json"
SIGNATURE_V4_NAME = f"{MANIFEST_V4_NAME}.sig"
MANIFEST_SCHEMAS = {
    "persistmind.update_manifest.v2",
    "persistmind.update_manifest.v3",
    "persistmind.update_manifest.v4",
}
TRUSTED_MANIFEST_NAME = "trusted-release-manifest.v4.json"
TRUSTED_MANIFEST_SIGNATURE_NAME = f"{TRUSTED_MANIFEST_NAME}.sig"
MANIFEST_SELF_VERIFICATION_ID = "signed-manifest:self:ed25519:v4"
DRIVE_HOSTS = {"drive.google.com", "drive.usercontent.google.com", "docs.googleusercontent.com"}
GITHUB_RELEASE_HOSTS = {"github.com", "objects.githubusercontent.com"}
ROOT_KEYS = (
    "2zTxhUn/x3MO0ju5mXYuEmbJfAGWj6BE9nWkgBb43do=",
    "kuh85P8eq5Qp1S4kIUJ2LoUfxZX+TbEstEaKgJtlV4A=",
)
MAX_METADATA_BYTES = 1_000_000
MAX_WHEEL_BYTES = 250_000_000
MAX_BUNDLE_BYTES = 1_000_000_000
PRODUCT_ID = "c8ee8be4-1cc8-4e78-972f-c73f8615f2f7"

_ED25519_Q = 2**255 - 19
_ED25519_L = 2**252 + 27742317777372353535851937790883648493
_ED25519_D = (-121665 * pow(121666, _ED25519_Q - 2, _ED25519_Q)) % _ED25519_Q
_ED25519_I = pow(2, (_ED25519_Q - 1) // 4, _ED25519_Q)


def _verify_ed25519(public_key: bytes, signature: bytes, message: bytes) -> bool:
    if len(public_key) != 32 or len(signature) != 64:
        return False
    try:
        public = _decode_ed25519_point(public_key)
        encoded_r = signature[:32]
        point_r = _decode_ed25519_point(encoded_r)
    except ValueError:
        return False
    scalar_s = int.from_bytes(signature[32:], "little")
    if scalar_s >= _ED25519_L:
        return False
    challenge = (
        int.from_bytes(hashlib.sha512(encoded_r + public_key + message).digest(), "little")
        % _ED25519_L
    )
    base = _decode_ed25519_point(
        bytes.fromhex("5866666666666666666666666666666666666666666666666666666666666666")
    )
    return _ed25519_scalar(base, scalar_s) == _ed25519_add(
        point_r, _ed25519_scalar(public, challenge)
    )


def _decode_ed25519_point(encoded: bytes) -> tuple[int, int]:
    value = int.from_bytes(encoded, "little")
    sign = value >> 255
    y = value & ((1 << 255) - 1)
    if y >= _ED25519_Q:
        raise ValueError("non-canonical Ed25519 point")
    y2 = y * y % _ED25519_Q
    x2 = (y2 - 1) * pow(_ED25519_D * y2 + 1, _ED25519_Q - 2, _ED25519_Q)
    x = pow(x2, (_ED25519_Q + 3) // 8, _ED25519_Q)
    if (x * x - x2) % _ED25519_Q:
        x = x * _ED25519_I % _ED25519_Q
    if (x * x - x2) % _ED25519_Q:
        raise ValueError("invalid Ed25519 point")
    if (x & 1) != sign:
        x = _ED25519_Q - x
    if (-x * x + y2 - 1 - _ED25519_D * x * x * y2) % _ED25519_Q:
        raise ValueError("point is not on Ed25519 curve")
    return x, y


def _ed25519_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = left
    x2, y2 = right
    product = _ED25519_D * x1 * x2 * y1 * y2 % _ED25519_Q
    x3 = (x1 * y2 + x2 * y1) * pow(1 + product, _ED25519_Q - 2, _ED25519_Q)
    y3 = (y1 * y2 + x1 * x2) * pow(1 - product, _ED25519_Q - 2, _ED25519_Q)
    return x3 % _ED25519_Q, y3 % _ED25519_Q


def _ed25519_scalar(point: tuple[int, int], scalar: int) -> tuple[int, int]:
    result = (0, 1)
    addend = point
    while scalar:
        if scalar & 1:
            result = _ed25519_add(result, addend)
        addend = _ed25519_add(addend, addend)
        scalar >>= 1
    return result


def _python_supported(specifier: str) -> bool:
    version = sys.version_info[:2]
    clauses = [item.strip() for item in specifier.split(",") if item.strip()]
    for clause in clauses:
        match = re.fullmatch(r"(>=|<=|>|<|==)(\d+)\.(\d+)", clause)
        if not match:
            return False
        expected = (int(match.group(2)), int(match.group(3)))
        operator = match.group(1)
        if operator == ">=" and not version >= expected:
            return False
        if operator == "<=" and not version <= expected:
            return False
        if operator == ">" and not version > expected:
            return False
        if operator == "<" and not version < expected:
            return False
        if operator == "==" and not version == expected:
            return False
    return bool(clauses)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install PersistMind from a signed GitHub release manifest"
    )
    parser.add_argument("--repo", default=".", help="project repository to configure")
    parser.add_argument(
        "--agents", help="comma-separated agent list; omit for an interactive prompt"
    )
    parser.add_argument("--channel", choices=("stable", "preview"), default="stable")
    parser.add_argument("--version", help="install an exact release version")
    parser.add_argument(
        "--manifest-url",
        default=os.environ.get("PERSISTMIND_RELEASE_MANIFEST_URL"),
        help="GitHub release URL for the signed release manifest",
    )
    parser.add_argument(
        "--manifest-signature-url",
        default=os.environ.get("PERSISTMIND_RELEASE_MANIFEST_SIGNATURE_URL"),
        help="GitHub release URL for the detached manifest signature",
    )
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
    if not (3, 11) <= sys.version_info[:2] < (3, 14):
        raise SystemExit("PersistMind requires Python 3.11 through 3.13")
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        raise SystemExit(f"project repository does not exist: {repo}")
    environment = _environment_root()
    python = _venv_python(environment)
    if not args.internal:
        _prepare_environment(environment, python)
        command = [str(python), str(Path(__file__).resolve()), *sys.argv[1:], "--internal"]
        raise SystemExit(subprocess.call(command))
    activation: tuple[bytes, bytes] | None = None
    if args.local_wheel:
        wheel = _verify_local_wheel(
            Path(args.local_wheel), str(args.version), str(args.local_wheel_sha256)
        )
        _verify_local_wheelhouse(wheel)
        _install_wheel(python, wheel, wheelhouse=wheel.parent, reinstall=args.reinstall)
        _remove_trusted_release_activation(environment)
        installed_version = str(args.version).removeprefix("v")
    else:
        if not args.manifest_url or not args.manifest_signature_url:
            raise SystemExit(
                "release metadata is not configured; pass --manifest-url and "
                "--manifest-signature-url"
            )
        manifest_bytes = _release_metadata_bytes(args.manifest_url, MAX_METADATA_BYTES)
        signature = _release_metadata_bytes(args.manifest_signature_url, 16_384)
        release: dict[str, Any] = {}
        manifest = _verify_manifest(release, manifest_bytes, signature, args.channel, args.version)
        _verify_promoted_release_identity(manifest)
        release = {
            "tag_name": manifest["release_tag"],
            "prerelease": manifest["channel"] == "preview",
            "assets": [],
        }
        wheel = _download_bundle(release, manifest)
        try:
            _install_wheel(python, wheel, wheelhouse=wheel.parent, reinstall=args.reinstall)
        finally:
            shutil.rmtree(wheel.parent, ignore_errors=True)
        activation = (manifest_bytes, signature)
        installed_version = str(manifest["version"])
    if activation is not None:
        _write_trusted_release_activation(environment, *activation)
    _write_launchers(environment, python)
    command = _project_install_command(python, repo, args)
    result = subprocess.call(command)
    if result:
        raise SystemExit(result)
    print(f"persistmind-bootstrap: installed PersistMind {installed_version}")
    print("persistmind-bootstrap: future updates: persistmind update")


def _project_install_command(python: Path, repo: Path, args: argparse.Namespace) -> list[str]:
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


def _verify_promoted_release_identity(manifest: dict[str, Any]) -> dict[str, Any]:
    identity = manifest.get("release_identity")
    if (
        manifest.get("schema_version") != "persistmind.update_manifest.v4"
        or manifest.get("promotion_status") != "promoted"
        or not isinstance(identity, dict)
    ):
        raise SystemExit("release manifest does not contain a promoted v4 identity")
    supplied_hash = identity.get("identity_hash")
    canonical = {key: value for key, value in identity.items() if key != "identity_hash"}
    expected_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if supplied_hash != expected_hash:
        raise SystemExit("promoted release identity hash is invalid")
    maturity = str(identity.get("maturity") or "")
    expected_maturity = "production" if manifest.get("channel") == "stable" else "public_beta"
    if (
        maturity != expected_maturity
        or bool(identity.get("production")) != (maturity == "production")
        or bool(identity.get("public_beta")) != (maturity == "public_beta")
        or identity.get("officially_signed") is not True
        or identity.get("signing_status") != "signed-trusted-update"
        or identity.get("runtime_profile") != "windows-stable"
        or identity.get("profile_locked") is not True
    ):
        raise SystemExit("promoted release identity maturity or signing posture is invalid")
    if (
        identity.get("version") != manifest.get("version")
        or identity.get("source_commit") != manifest.get("commit_sha")
        or set(identity.get("qualified_os") or []) != {"Windows 11"}
        or set(identity.get("qualified_python") or []) != {"3.11", "3.12", "3.13"}
    ):
        raise SystemExit("promoted release identity qualification does not match the manifest")
    promotion = identity.get("promotion")
    evidence = (
        promotion.get("supported_agent_evidence_ids") if isinstance(promotion, dict) else None
    )
    if (
        not isinstance(evidence, list)
        or {str(item).split(":", 1)[0] for item in evidence} != {"codex", "gemini"}
        or promotion.get("signed_manifest_verification_id") != MANIFEST_SELF_VERIFICATION_ID
        or not str(promotion.get("independent_approval_id") or "").strip()
    ):
        raise SystemExit("promoted release identity lacks Codex/Gemini or approval evidence")
    wheels = [
        item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
        and item.get("role") == "root"
        and str(item.get("filename") or "").endswith(".whl")
    ]
    if len(wheels) != 1 or wheels[0].get("sha256") != identity.get("artifact_hashes", {}).get(
        "wheel_sha256"
    ):
        raise SystemExit("promoted release identity does not bind the manifest wheel")
    forbidden = ("internal windows preview", "non-critical", "manual human review")
    if any(
        marker in str(item).casefold()
        for item in identity.get("known_limitations") or []
        for marker in forbidden
    ):
        raise SystemExit("promoted release identity retained an internal-preview restriction")
    return identity


def _write_trusted_release_activation(root: Path, document: bytes, signature: bytes) -> None:
    destination = root / "share" / "persistmind"
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in (
        (TRUSTED_MANIFEST_NAME, document),
        (TRUSTED_MANIFEST_SIGNATURE_NAME, signature),
    ):
        target = destination / name
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_bytes(content)
        os.replace(temporary, target)


def _remove_trusted_release_activation(root: Path) -> None:
    destination = root / "share" / "persistmind"
    for name in (TRUSTED_MANIFEST_NAME, TRUSTED_MANIFEST_SIGNATURE_NAME):
        (destination / name).unlink(missing_ok=True)


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
    try:
        signature = base64.b64decode(encoded_signature.strip(), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SystemExit("release manifest signature is not valid base64") from exc
    for encoded_key in ROOT_KEYS:
        try:
            public_key = base64.b64decode(encoded_key, validate=True)
        except (binascii.Error, ValueError):
            continue
        if _verify_ed25519(public_key, signature, document):
            break
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
        "dependency_lock",
        "sbom",
    }
    if not isinstance(value, dict) or not required.issubset(value):
        raise SystemExit("release manifest is incomplete")
    expected_repository = REPOSITORY
    if (
        value["schema_version"] not in MANIFEST_SCHEMAS
        or value["repository"] != expected_repository
        or value.get("product_id") != PRODUCT_ID
    ):
        raise SystemExit("release manifest identity is invalid")
    if (release.get("tag_name") and value["release_tag"] != release.get("tag_name")) or value[
        "release_tag"
    ] != f"v{value['version']}":
        raise SystemExit("release tag and manifest version disagree")
    version = str(value["version"])
    prerelease = bool(re.search(r"[A-Za-z]", version))
    if exact and version != exact.removeprefix("v"):
        raise SystemExit("the release manifest version differs from the requested version")
    if not exact and channel == "stable" and prerelease:
        raise SystemExit("stable channel returned a prerelease")
    if value["channel"] != ("preview" if prerelease else "stable"):
        raise SystemExit("release channel and version disagree")
    if release and bool(release.get("prerelease")) != prerelease:
        raise SystemExit("release-channel prerelease state and manifest version disagree")
    if not _python_supported(str(value["requires_python"])):
        raise SystemExit("this PersistMind release does not support the installed Python")
    if value["schema_version"] == "persistmind.update_manifest.v3":
        _verify_v3_manifest(value)
    if value["schema_version"] == "persistmind.update_manifest.v4":
        _verify_v4_manifest(value)
    return value


def _verify_v3_manifest(value: dict[str, Any]) -> None:
    required = {
        "commit_sha",
        "release_repository_commit",
        "build_identity",
        "expires_at",
        "revoked",
        "project_state_protocol",
    }
    if not required.issubset(value) or value.get("revoked") is not False:
        raise SystemExit("release manifest v3 trust metadata is incomplete or revoked")
    for key in ("commit_sha", "release_repository_commit"):
        digest = str(value.get(key, ""))
        if not re.fullmatch(r"[0-9a-f]{40}", digest):
            raise SystemExit(f"release manifest v3 {key} is invalid")
    if (
        not str(value.get("build_identity", "")).strip()
        or int(value.get("project_state_protocol", 0)) != 2
    ):
        raise SystemExit("release manifest v3 build or protocol identity is invalid")
    try:
        expires_at = datetime.fromisoformat(str(value["expires_at"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit("release manifest v3 expiry is invalid") from exc
    if expires_at.tzinfo is None or expires_at <= datetime.now(timezone.utc):
        raise SystemExit("release manifest v3 has expired")
    bindings = [value.get("dependency_lock"), value.get("sbom"), *value.get("artifacts", [])]
    file_ids: list[str] = []
    for binding in bindings:
        if not isinstance(binding, dict):
            raise SystemExit("release manifest v3 artifact binding is invalid")
        transport = binding.get("transport")
        if not isinstance(transport, dict) or transport.get("kind") != "google_drive":
            raise SystemExit("release manifest v3 requires Google Drive artifact transport")
        file_id = str(transport.get("file_id", ""))
        if not re.fullmatch(r"[A-Za-z0-9_-]{10,200}", file_id):
            raise SystemExit("release manifest v3 Drive file identity is invalid")
        file_ids.append(file_id)
    if len(file_ids) != len(set(file_ids)):
        raise SystemExit("release manifest v3 Drive file identities must be unique")


def _verify_v4_manifest(value: dict[str, Any]) -> None:
    required = {
        "commit_sha",
        "build_identity",
        "expires_at",
        "revoked",
        "project_state_protocol",
        "artifact_transport",
        "release_repository",
    }
    if not required.issubset(value) or value.get("revoked") is not False:
        raise SystemExit("release manifest v4 trust metadata is incomplete or revoked")
    if not re.fullmatch(r"[0-9a-f]{40}", str(value.get("commit_sha", ""))):
        raise SystemExit("release manifest v4 source commit is invalid")
    if (
        value.get("artifact_transport") != "github_release_asset"
        or value.get("release_repository") != REPOSITORY
    ):
        raise SystemExit("release manifest v4 GitHub release identity is invalid")
    if (
        not str(value.get("build_identity", "")).strip()
        or int(value.get("project_state_protocol", 0)) != 2
    ):
        raise SystemExit("release manifest v4 build or protocol identity is invalid")
    try:
        expires_at = datetime.fromisoformat(str(value["expires_at"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit("release manifest v4 expiry is invalid") from exc
    if expires_at.tzinfo is None or expires_at <= datetime.now(timezone.utc):
        raise SystemExit("release manifest v4 has expired")
    bindings = [value.get("dependency_lock"), value.get("sbom"), *value.get("artifacts", [])]
    asset_names: list[str] = []
    for binding in bindings:
        if not isinstance(binding, dict):
            raise SystemExit("release manifest v4 artifact binding is invalid")
        transport = binding.get("transport")
        if not isinstance(transport, dict) or transport.get("kind") != "github_release_asset":
            raise SystemExit("release manifest v4 requires GitHub release asset transport")
        if (
            transport.get("repository") != REPOSITORY
            or transport.get("release_tag") != value.get("release_tag")
            or transport.get("asset_name") != binding.get("filename")
        ):
            raise SystemExit("release manifest v4 GitHub asset identity is invalid")
        asset_names.append(str(transport["asset_name"]))
    if len(asset_names) != len(set(asset_names)):
        raise SystemExit("release manifest v4 GitHub asset identities must be unique")


def _release_metadata_bytes(url: str, maximum: int) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme == "https" and parsed.hostname in DRIVE_HOSTS:
        return _drive_metadata_bytes(url, maximum)
    if parsed.scheme == "https" and parsed.hostname == "github.com":
        return _github_metadata_bytes(url, maximum)
    raise SystemExit("release metadata must be hosted on GitHub Releases or Google Drive")


def _drive_metadata_bytes(url: str, maximum: int) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in DRIVE_HOSTS:
        raise SystemExit("release metadata must be hosted on Google Drive")

    class DriveMetadataRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
            redirect = urllib.parse.urlparse(newurl)
            if redirect.scheme != "https" or redirect.hostname not in DRIVE_HOSTS:
                raise SystemExit("release metadata redirect escaped the Drive host policy")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    request = urllib.request.Request(url, headers={"User-Agent": "persistmind-bootstrap/4"})
    with urllib.request.build_opener(DriveMetadataRedirect()).open(request, timeout=60) as response:
        final = urllib.parse.urlparse(response.geturl())
        if final.scheme != "https" or final.hostname not in DRIVE_HOSTS:
            raise SystemExit("release metadata response escaped the Drive host policy")
        value = response.read(maximum + 1)
    if len(value) > maximum:
        raise SystemExit("release metadata exceeds the bootstrap size policy")
    return value


def _github_metadata_bytes(url: str, maximum: int) -> bytes:
    parsed = urllib.parse.urlparse(url)
    expected_prefix = f"/{REPOSITORY}/releases/download/"
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or not parsed.path.startswith(expected_prefix)
    ):
        raise SystemExit("release metadata must be hosted on the PersistMind GitHub release repo")

    class GitHubMetadataRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
            redirect = urllib.parse.urlparse(newurl)
            if redirect.scheme != "https" or redirect.hostname not in GITHUB_RELEASE_HOSTS:
                raise SystemExit("release metadata redirect escaped the GitHub host policy")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    request = urllib.request.Request(url, headers={"User-Agent": "persistmind-bootstrap/4"})
    with urllib.request.build_opener(GitHubMetadataRedirect()).open(
        request, timeout=60
    ) as response:
        final = urllib.parse.urlparse(response.geturl())
        if final.scheme != "https" or final.hostname not in GITHUB_RELEASE_HOSTS:
            raise SystemExit("release metadata response escaped the GitHub host policy")
        value = response.read(maximum + 1)
    if len(value) > maximum:
        raise SystemExit("release metadata exceeds the bootstrap size policy")
    return value


def _wheel_artifact(manifest: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        item
        for item in manifest["artifacts"]
        if str(item.get("filename", "")).endswith(".whl") and item.get("role") == "root"
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


def _download_bundle(release: dict[str, Any], manifest: dict[str, Any]) -> Path:
    directory = Path(tempfile.mkdtemp(prefix="persistmind-bootstrap-"))
    try:
        wheel_artifacts = [
            item
            for item in manifest["artifacts"]
            if isinstance(item, dict) and str(item.get("filename", "")).endswith(".whl")
        ]
        if sum(int(item.get("size", 0)) for item in wheel_artifacts) > MAX_BUNDLE_BYTES:
            raise SystemExit("release wheelhouse exceeds the bootstrap size policy")
        root = _wheel_artifact(manifest)
        for artifact in wheel_artifacts:
            _download_signed_asset(release, artifact, directory)
        for key in ("dependency_lock", "sbom"):
            binding = manifest.get(key)
            if not isinstance(binding, dict):
                raise SystemExit(f"release {key} binding is invalid")
            _download_signed_asset(release, binding, directory)
        wheel = directory / str(root["filename"])
        _verify_wheel_metadata(wheel, str(release["tag_name"]).removeprefix("v"))
        _verify_local_wheelhouse(wheel)
        return wheel
    except BaseException:
        shutil.rmtree(directory, ignore_errors=True)
        raise


def _download_signed_asset(
    release: dict[str, Any], artifact: dict[str, Any], directory: Path
) -> Path:
    name = str(artifact.get("filename", ""))
    size = int(artifact.get("size", 0))
    digest_text = str(artifact.get("sha256", ""))
    if (
        Path(name).name != name
        or size <= 0
        or size > MAX_WHEEL_BYTES
        or not re.fullmatch(r"[0-9a-f]{64}", digest_text)
    ):
        raise SystemExit("release artifact binding is invalid")
    if isinstance(artifact.get("transport"), dict):
        transport = artifact["transport"]
        if transport.get("kind") == "google_drive":
            return _download_drive_asset(artifact, directory)
        if transport.get("kind") == "github_release_asset":
            return _download_github_release_asset(artifact, directory)
        raise SystemExit("release artifact transport is invalid")
    asset = _assets(release).get(name)
    if not asset or int(asset.get("size", -1)) != size:
        raise SystemExit("release asset does not match its signed manifest")
    target = directory / name
    digest = hashlib.sha256()
    request = urllib.request.Request(str(asset["browser_download_url"]), headers=_headers())
    with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as handle:
        total = 0
        while block := response.read(1024 * 1024):
            total += len(block)
            if total > size:
                raise SystemExit("release artifact exceeds its signed size")
            digest.update(block)
            handle.write(block)
    if total != size or digest.hexdigest() != digest_text:
        raise SystemExit("release artifact failed SHA-256 verification")
    return target


def _download_drive_asset(artifact: dict[str, Any], directory: Path) -> Path:
    name = str(artifact["filename"])
    size = int(artifact["size"])
    expected_digest = str(artifact["sha256"])
    transport = artifact.get("transport")
    if not isinstance(transport, dict) or transport.get("kind") != "google_drive":
        raise SystemExit("release artifact transport is invalid")
    file_id = str(transport.get("file_id", ""))
    url = str(transport.get("url", ""))
    allowed = {str(item).casefold() for item in transport.get("allowed_redirect_hosts", [])}
    parsed = urllib.parse.urlparse(url)
    if (
        not re.fullmatch(r"[A-Za-z0-9_-]{10,200}", file_id)
        or parsed.scheme != "https"
        or parsed.hostname not in DRIVE_HOSTS
        or file_id not in urllib.parse.unquote(url)
        or not allowed
        or not allowed.issubset(DRIVE_HOSTS)
    ):
        raise SystemExit("release Drive artifact origin or identity is invalid")

    class SignedDriveRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
            redirect = urllib.parse.urlparse(newurl)
            if redirect.scheme != "https" or redirect.hostname not in allowed:
                raise SystemExit("release Drive redirect escaped the signed host policy")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    target = directory / name
    temporary = target.with_suffix(target.suffix + ".part")
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers=_headers())
    opener = urllib.request.build_opener(SignedDriveRedirect())
    try:
        with opener.open(request, timeout=120) as response, temporary.open("wb") as handle:
            final = urllib.parse.urlparse(response.geturl())
            if final.scheme != "https" or final.hostname not in allowed:
                raise SystemExit("release Drive response escaped the signed host policy")
            expected_media = str(artifact.get("media_type", "application/octet-stream"))
            if str(response.headers.get_content_type()).casefold() != expected_media.casefold():
                raise SystemExit("release Drive artifact media type is invalid")
            total = 0
            while block := response.read(min(1024 * 1024, size + 1 - total)):
                total += len(block)
                if total > size:
                    raise SystemExit("release Drive artifact exceeds its signed size")
                digest.update(block)
                handle.write(block)
        if total != size or digest.hexdigest() != expected_digest:
            raise SystemExit("release Drive artifact failed SHA-256 verification")
        os.replace(temporary, target)
        return target
    finally:
        temporary.unlink(missing_ok=True)


def _download_github_release_asset(artifact: dict[str, Any], directory: Path) -> Path:
    name = str(artifact["filename"])
    size = int(artifact["size"])
    expected_digest = str(artifact["sha256"])
    transport = artifact.get("transport")
    if not isinstance(transport, dict) or transport.get("kind") != "github_release_asset":
        raise SystemExit("release artifact transport is invalid")
    repository = str(transport.get("repository", ""))
    release_tag = str(transport.get("release_tag", ""))
    asset_name = str(transport.get("asset_name", ""))
    url = str(transport.get("url", ""))
    parsed = urllib.parse.urlparse(url)
    if (
        repository != REPOSITORY
        or asset_name != name
        or not re.fullmatch(r"v[0-9A-Za-z_.-]+", release_tag)
        or parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or urllib.parse.unquote(parsed.path)
        != f"/{repository}/releases/download/{release_tag}/{asset_name}"
    ):
        raise SystemExit("release GitHub artifact origin or identity is invalid")

    class SignedGitHubRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
            redirect = urllib.parse.urlparse(newurl)
            if redirect.scheme != "https" or redirect.hostname not in GITHUB_RELEASE_HOSTS:
                raise SystemExit("release GitHub redirect escaped the signed host policy")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    target = directory / name
    temporary = target.with_suffix(target.suffix + ".part")
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers=_headers())
    opener = urllib.request.build_opener(SignedGitHubRedirect())
    try:
        with opener.open(request, timeout=120) as response, temporary.open("wb") as handle:
            final = urllib.parse.urlparse(response.geturl())
            if final.scheme != "https" or final.hostname not in GITHUB_RELEASE_HOSTS:
                raise SystemExit("release GitHub response escaped the signed host policy")
            total = 0
            while block := response.read(min(1024 * 1024, size + 1 - total)):
                total += len(block)
                if total > size:
                    raise SystemExit("release GitHub artifact exceeds its signed size")
                digest.update(block)
                handle.write(block)
        if total != size or digest.hexdigest() != expected_digest:
            raise SystemExit("release GitHub artifact failed SHA-256 verification")
        os.replace(temporary, target)
        return target
    finally:
        temporary.unlink(missing_ok=True)


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
    if len(digest_text) != 64 or any(
        character not in "0123456789abcdef" for character in digest_text
    ):
        raise SystemExit("local wheel SHA-256 is invalid")
    if not target.is_file() or target.suffix.casefold() != ".whl":
        raise SystemExit("local wheel does not exist or is not a wheel")
    if target.stat().st_size <= 0 or target.stat().st_size > MAX_WHEEL_BYTES:
        raise SystemExit("local wheel size is invalid")
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest_text:
        raise SystemExit("local wheel failed SHA-256 verification")
    _verify_wheel_metadata(target, version.removeprefix("v"))
    return target


def _verify_local_wheelhouse(root_wheel: Path) -> dict[str, Any]:
    lock_path = root_wheel.parent / "dependency-lock.v1.json"
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit("verified dependency lock is required for offline installation") from exc
    entries = lock.get("wheels") if isinstance(lock, dict) else None
    if (
        lock.get("schema_version") != "persistmind.dependency_lock.v1"
        or lock.get("root_wheel") != root_wheel.name
        or not isinstance(entries, list)
        or not entries
    ):
        raise SystemExit("dependency lock identity is invalid")
    expected = {str(item.get("filename")) for item in entries if isinstance(item, dict)}
    actual = {path.name for path in root_wheel.parent.glob("*.whl")}
    if expected != actual:
        raise SystemExit("offline wheelhouse differs from dependency lock")
    for item in entries:
        path = root_wheel.parent / str(item["filename"])
        if (
            Path(str(item["filename"])).name != str(item["filename"])
            or path.stat().st_size != int(item.get("size", 0))
            or hashlib.sha256(path.read_bytes()).hexdigest() != item.get("sha256")
        ):
            raise SystemExit("offline wheelhouse artifact failed verification")
    return lock


def _verify_wheel_metadata(path: Path, version: str) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            metadata = [item for item in archive.namelist() if item.endswith(".dist-info/METADATA")]
            contents = archive.read(metadata[0]) if len(metadata) == 1 else b""
    except (OSError, zipfile.BadZipFile) as exc:
        raise SystemExit("release wheel is not a valid wheel archive") from exc
    expected_version = f"Version: {version}\n".encode()
    if b"Name: persistmind\n" not in contents or expected_version not in contents:
        raise SystemExit("release wheel metadata is invalid")


def _install_wheel(python: Path, wheel: Path, *, wheelhouse: Path, reinstall: bool) -> None:
    command = [
        str(python),
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-index",
        "--find-links",
        str(wheelhouse),
        "--upgrade",
    ]
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
            "#!/bin/sh\nexec " + shlex.quote(str(python.resolve())) + ' -I -m persistmind "$@"\n',
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
