#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
git clone --depth 1 --branch v5.5.1 https://github.com/espressif/esp-idf.git .tooling/esp-idf
.tooling/esp-idf/install.sh esp32s3
IDF_TOOLS_PATH="$HOME/.espressif" .venv/bin/python .tooling/esp-idf/tools/idf_tools.py install qemu-xtensa
echo "Run make ready after the container setup completes."

