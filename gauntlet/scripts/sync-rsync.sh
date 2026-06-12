#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  sync-rsync.sh --source DIR --target USER@HOST:DIR [--ssh "ssh ..."]

Synchronize the local source-of-truth worktree to the remote run directory.
This helper intentionally does not delete .gauntlet run artifacts on the
business repository side. Project-specific sync changes should be captured in
run.yaml before changing this helper.
USAGE
}

SOURCE=""
TARGET=""
SSH_CMD="ssh"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      SOURCE="${2:-}"
      shift 2
      ;;
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --ssh)
      SSH_CMD="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "${SOURCE}" || -z "${TARGET}" ]]; then
  usage >&2
  exit 2
fi

rsync -az --delete \
  --exclude '.git/' \
  --exclude '.gauntlet/*/logs/' \
  --exclude 'node_modules/' \
  --exclude '.venv/' \
  -e "${SSH_CMD}" \
  "${SOURCE%/}/" \
  "${TARGET%/}/"
