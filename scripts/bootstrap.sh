#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root}"
case "$(uname -m)" in
  x86_64|aarch64|arm64) ;;
  *) echo "Unsupported course host architecture: $(uname -m)" >&2; exit 2 ;;
esac

sudo apt-get update
sudo apt-get install --yes --no-install-recommends curl git libglib2.0-0 libgcrypt20 libpixman-1-0 libslirp0 libusb-1.0-0 patch xz-utils
python -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt

idf_commit="fcae32885b0296b32044cb99ecbdc50d98dddb83"
if [[ ! -d .tooling/esp-idf/.git ]]; then
  git clone --filter=blob:none --no-checkout https://github.com/espressif/esp-idf.git .tooling/esp-idf
fi
git -C .tooling/esp-idf fetch --depth 1 origin "${idf_commit}"
git -C .tooling/esp-idf checkout --detach "${idf_commit}"
test "$(git -C .tooling/esp-idf rev-parse HEAD)" = "${idf_commit}"
.tooling/esp-idf/install.sh esp32s3
scripts/install-pinned-qemu.sh >/dev/null
echo "Run make ready after the container setup completes."

