#!/usr/bin/env bash
# PersistMind release installer for macOS and Linux.
# For a fresh install, execute this only after following the staged verification guide.
set -euo pipefail

REPO="."
AGENTS=""
CHANNEL="stable"
VERSION=""
INIT_GIT=0
SKIP_INDEX=0
REINSTALL=0
BOOTSTRAP_PATH=""
BOOTSTRAP_URL=""
BOOTSTRAP_SHA256=""
MANIFEST_URL=""
MANIFEST_SIGNATURE_URL=""
LOCAL_WHEEL_PATH=""
LOCAL_WHEEL_SHA256=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2;;
    --agents) AGENTS="$2"; shift 2;;
    --channel) CHANNEL="$2"; shift 2;;
    --version) VERSION="$2"; shift 2;;
    --init-git) INIT_GIT=1; shift;;
    --skip-index) SKIP_INDEX=1; shift;;
    --reinstall) REINSTALL=1; shift;;
    --bootstrap-path) BOOTSTRAP_PATH="$2"; shift 2;;
    --bootstrap-url) BOOTSTRAP_URL="$2"; shift 2;;
    --bootstrap-sha256) BOOTSTRAP_SHA256="$2"; shift 2;;
    --manifest-url) MANIFEST_URL="$2"; shift 2;;
    --manifest-signature-url) MANIFEST_SIGNATURE_URL="$2"; shift 2;;
    --local-wheel-path) LOCAL_WHEEL_PATH="$2"; shift 2;;
    --local-wheel-sha256) LOCAL_WHEEL_SHA256="$2"; shift 2;;
    -h|--help)
      echo "usage: install-persistmind.sh [--repo PATH] [--agents LIST] [--channel stable|preview] [--version VERSION] [--bootstrap-path VERIFIED_FILE | --bootstrap-url RELEASE_URL --bootstrap-sha256 SHA256] --manifest-url RELEASE_URL --manifest-signature-url RELEASE_URL [--init-git] [--skip-index] [--reinstall]"
      exit 0;;
    *) echo "persistmind-install: unknown option '$1'" >&2; exit 2;;
  esac
done
[ "$CHANNEL" = "stable" ] || [ "$CHANNEL" = "preview" ] || { echo "persistmind-install: invalid channel" >&2; exit 2; }
if { [ -n "$LOCAL_WHEEL_PATH" ] && [ -z "$LOCAL_WHEEL_SHA256" ]; } || \
   { [ -z "$LOCAL_WHEEL_PATH" ] && [ -n "$LOCAL_WHEEL_SHA256" ]; }; then
  echo "persistmind-install: local wheel path and SHA-256 must be supplied together" >&2
  exit 2
fi
if [ -n "$LOCAL_WHEEL_PATH" ] && { [ -z "$BOOTSTRAP_PATH" ] || [ -z "$VERSION" ]; }; then
  echo "persistmind-install: local wheel testing requires --bootstrap-path and exact --version" >&2
  exit 2
fi

if [ -z "$AGENTS" ] && [ -r /dev/tty ]; then
  printf 'Coding agents to configure (codex, claude, cursor; comma-separated): ' > /dev/tty
  IFS= read -r AGENTS < /dev/tty
  [ -n "$AGENTS" ] || { echo "persistmind-install: no coding agents selected" >&2; exit 2; }
fi

compatible_python() {
  "$1" -c 'import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)' >/dev/null 2>&1
}

find_python() {
  for candidate in "${PERSISTMIND_PYTHON:-}" python3.13 python3.12 python3.11 python3; do
    [ -n "$candidate" ] || continue
    command -v "$candidate" >/dev/null 2>&1 || continue
    compatible_python "$candidate" && { command -v "$candidate"; return 0; }
  done
  return 1
}

install_python() {
  echo "persistmind-install: installing Python 3.11+"
  if command -v brew >/dev/null 2>&1; then
    brew install python@3.13
  elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3
  elif command -v zypper >/dev/null 2>&1; then
    sudo zypper --non-interactive install python3
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --needed --noconfirm python
  else
    echo "persistmind-install: no supported package manager was found; install Python 3.11+ and rerun." >&2
    return 1
  fi
}

install_managed_python() {
  command -v uv >/dev/null 2>&1 || {
    echo "persistmind-install: no trusted Python package source produced Python 3.11+." >&2
    echo "Install Python 3.11+ (or an already-verified uv), then rerun." >&2
    return 1
  }
  echo "persistmind-install: provisioning Python 3.13 with the existing uv executable"
  UV="$(command -v uv)"
  "$UV" python install 3.13
  "$UV" python find 3.13
}

PYTHON="$(find_python || true)"
if [ -z "$PYTHON" ]; then
  install_python || true
  PYTHON="$(find_python || true)"
fi
if [ -z "$PYTHON" ]; then
  PYTHON="$(install_managed_python | tail -n 1)"
  compatible_python "$PYTHON" || PYTHON=""
fi
[ -n "$PYTHON" ] || { echo "persistmind-install: Python 3.11+ could not be located after installation." >&2; exit 1; }

REPO="$(cd "$REPO" && pwd)"
if [ -n "$BOOTSTRAP_PATH" ]; then
  [ -n "$VERSION" ] || {
    echo "persistmind-install: --bootstrap-path requires the exact --version that was verified." >&2
    exit 2
  }
  [ -f "$BOOTSTRAP_PATH" ] || {
    echo "persistmind-install: verified bootstrap not found: $BOOTSTRAP_PATH" >&2
    exit 2
  }
  BOOTSTRAP_PATH="$(cd "$(dirname "$BOOTSTRAP_PATH")" && pwd)/$(basename "$BOOTSTRAP_PATH")"
else
  [ -n "$BOOTSTRAP_URL" ] && [ -n "$BOOTSTRAP_SHA256" ] || {
    echo "persistmind-install: provide --bootstrap-path, or the GitHub release --bootstrap-url and --bootstrap-sha256" >&2
    exit 2
  }
  case "$BOOTSTRAP_URL" in
    https://github.com/*|https://drive.google.com/*|https://drive.usercontent.google.com/*|https://docs.googleusercontent.com/*) ;;
    *) echo "persistmind-install: bootstrap URL must be hosted on GitHub Releases or Google Drive" >&2; exit 2;;
  esac
  case "$BOOTSTRAP_SHA256" in
    *[!0-9a-fA-F]*|'') echo "persistmind-install: bootstrap SHA-256 is invalid" >&2; exit 2;;
  esac
  [ "${#BOOTSTRAP_SHA256}" -eq 64 ] || { echo "persistmind-install: bootstrap SHA-256 is invalid" >&2; exit 2; }
  BOOTSTRAP_PATH="$(mktemp "${TMPDIR:-/tmp}/persistmind-bootstrap.XXXXXX.py")"
  trap 'rm -f "$BOOTSTRAP_PATH"' EXIT
  curl --fail --location --proto '=https' --max-redirs 8 "$BOOTSTRAP_URL" --output "$BOOTSTRAP_PATH"
  ACTUAL_BOOTSTRAP_SHA256="$($PYTHON -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$BOOTSTRAP_PATH")"
  [ "$ACTUAL_BOOTSTRAP_SHA256" = "$(printf '%s' "$BOOTSTRAP_SHA256" | tr 'A-F' 'a-f')" ] || {
    echo "persistmind-install: bootstrap download failed SHA-256 verification" >&2
    exit 1
  }
fi

if [ -z "$LOCAL_WHEEL_PATH" ] && { [ -z "$MANIFEST_URL" ] || [ -z "$MANIFEST_SIGNATURE_URL" ]; }; then
  echo "persistmind-install: release installation requires --manifest-url and --manifest-signature-url" >&2
  exit 2
fi

ARGS=(-I "$BOOTSTRAP_PATH" --repo "$REPO" --channel "$CHANNEL")
[ -z "$AGENTS" ] || ARGS+=(--agents "$AGENTS")
[ -z "$VERSION" ] || ARGS+=(--version "$VERSION")
[ -z "$MANIFEST_URL" ] || ARGS+=(--manifest-url "$MANIFEST_URL")
[ -z "$MANIFEST_SIGNATURE_URL" ] || ARGS+=(--manifest-signature-url "$MANIFEST_SIGNATURE_URL")
if [ -n "$LOCAL_WHEEL_PATH" ]; then
  LOCAL_WHEEL_PATH="$(cd "$(dirname "$LOCAL_WHEEL_PATH")" && pwd)/$(basename "$LOCAL_WHEEL_PATH")"
  ARGS+=(--local-wheel "$LOCAL_WHEEL_PATH" --local-wheel-sha256 "$LOCAL_WHEEL_SHA256")
fi
[ "$INIT_GIT" -eq 0 ] || ARGS+=(--init-git)
[ "$SKIP_INDEX" -eq 0 ] || ARGS+=(--skip-index)
[ "$REINSTALL" -eq 0 ] || ARGS+=(--reinstall)
"$PYTHON" "${ARGS[@]}"

echo "persistmind-install: complete. Ensure $HOME/.local/bin is on PATH, then use: persistmind update"
