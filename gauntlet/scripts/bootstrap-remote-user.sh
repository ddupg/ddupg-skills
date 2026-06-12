#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bootstrap-remote-user.sh --user USER --workdir USER_HOME [--install-base-packages]

Run as root on the Linux host. The script creates the isolated Gauntlet user,
ensures its home/work directory is USER_HOME, and optionally installs the base
package whitelist used by Gauntlet prompt runs.
USAGE
}

USER_NAME=""
WORKDIR=""
INSTALL_BASE_PACKAGES="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user)
      USER_NAME="${2:-}"
      shift 2
      ;;
    --workdir)
      WORKDIR="${2:-}"
      shift 2
      ;;
    --install-base-packages)
      INSTALL_BASE_PACKAGES="1"
      shift
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

if [[ "${EUID}" -ne 0 ]]; then
  echo "bootstrap-remote-user.sh must run as root" >&2
  exit 1
fi

if [[ -z "${USER_NAME}" || -z "${WORKDIR}" ]]; then
  usage >&2
  exit 2
fi

if [[ "${WORKDIR}" != /* ]]; then
  echo "workdir must be an absolute user home path" >&2
  exit 2
fi

install_base_packages() {
  if command -v apt-get >/dev/null 2>&1; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      git rsync curl tar ca-certificates build-essential python3 python3-venv
  elif command -v dnf >/dev/null 2>&1; then
    dnf install -y git rsync curl tar ca-certificates gcc gcc-c++ make python3
  elif command -v yum >/dev/null 2>&1; then
    yum install -y git rsync curl tar ca-certificates gcc gcc-c++ make python3
  else
    echo "no supported package manager found; install base packages manually" >&2
    return 1
  fi
}

if [[ "${INSTALL_BASE_PACKAGES}" == "1" ]]; then
  install_base_packages
fi

if id "${USER_NAME}" >/dev/null 2>&1; then
  USER_HOME="$(getent passwd "${USER_NAME}" | cut -d: -f6)"
  if [[ "${USER_HOME}" != "${WORKDIR}" ]]; then
    echo "existing user home mismatch: ${USER_NAME} has ${USER_HOME}, expected ${WORKDIR}" >&2
    exit 1
  fi
else
  WORKDIR_PARENT="${WORKDIR%/*}"
  if [[ -z "${WORKDIR_PARENT}" ]]; then
    WORKDIR_PARENT="/"
  fi
  mkdir -p "${WORKDIR_PARENT}"
  useradd --create-home --home-dir "${WORKDIR}" --shell /bin/bash "${USER_NAME}"
fi

mkdir -p "${WORKDIR}"
chown -R "${USER_NAME}:${USER_NAME}" "${WORKDIR}"
chmod 0750 "${WORKDIR}"

printf 'user=%s\nworkdir=%s\n' "${USER_NAME}" "${WORKDIR}"
