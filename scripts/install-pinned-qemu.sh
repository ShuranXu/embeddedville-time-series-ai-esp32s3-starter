#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
lock="${root}/toolchain/qemu.lock.json"
install_root="${QEMU_INSTALL_ROOT:-${root}/.tooling/qemu}"

case "$(uname -m)" in
  x86_64) asset_key="x86_64-linux-gnu" ;;
  aarch64|arm64) asset_key="aarch64-linux-gnu" ;;
  *) echo "Unsupported QEMU host architecture: $(uname -m)" >&2; exit 2 ;;
esac

mapfile -t values < <(python3 - "${lock}" "${asset_key}" <<'PY'
import json, sys
value = json.load(open(sys.argv[1], encoding="utf-8"))
asset = value["assets"][sys.argv[2]]
print(value["release"])
print(value["versionOutput"])
print(asset["name"])
print(asset["sha256"])
PY
)
release="${values[0]}"
version_output="${values[1]}"
asset_name="${values[2]}"
expected_sha="${values[3]}"
destination="${install_root}/${release}/${asset_key}"
qemu_bin="${destination}/bin/qemu-system-xtensa"

if [[ ! -x "${qemu_bin}" ]]; then
  mkdir -p "${install_root}/archives" "${destination}"
  archive="${install_root}/archives/${asset_name}"
  if [[ ! -f "${archive}" ]] || [[ "$(sha256sum "${archive}" | cut -d ' ' -f 1)" != "${expected_sha}" ]]; then
    partial="${archive}.partial"
    curl --fail --location --retry 3 --output "${partial}" "https://github.com/espressif/qemu/releases/download/${release}/${asset_name}"
    actual_sha="$(sha256sum "${partial}" | cut -d ' ' -f 1)"
    if [[ "${actual_sha}" != "${expected_sha}" ]]; then
      rm -f -- "${partial}"
      echo "QEMU checksum mismatch: expected ${expected_sha}, got ${actual_sha}" >&2
      exit 1
    fi
    mv -- "${partial}" "${archive}"
  fi
  staging="$(mktemp -d "${install_root}/extract.XXXXXX")"
  trap 'rm -rf -- "${staging}"' EXIT
  tar -xJf "${archive}" -C "${staging}"
  found="$(find "${staging}" -type f -path '*/bin/qemu-system-xtensa' -print -quit)"
  [[ -n "${found}" ]] || { echo "Verified QEMU archive lacks qemu-system-xtensa" >&2; exit 1; }
  cp -a "$(dirname "$(dirname "${found}")")/." "${destination}/"
fi

if ldd "${qemu_bin}" 2>&1 | grep -q 'not found'; then
  ldd "${qemu_bin}" >&2 || true
  echo "Pinned QEMU runtime libraries are missing; rerun scripts/bootstrap.sh." >&2
  exit 2
fi
actual_version="$("${qemu_bin}" --version | sed -n '1p')"
[[ "${actual_version}" == *"${version_output}"* ]] || { echo "Unexpected QEMU version: ${actual_version}" >&2; exit 1; }
printf '%s\n' "${qemu_bin}"
