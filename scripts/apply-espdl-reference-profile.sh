#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
component="${1:-${root}/firmware/managed_components/espressif__esp-dl}"
patch_file="${root}/toolchain/patches/esp-dl-3.3.13-reference-kernels.patch"
expected_checksums="809b78d63fdd4179eb80e4f42400033b1e3252f24c547a53c2895e6493b666d9"
expected_cmake="05b3c504a6eefcb8f9f937e1c511810e4ada59d423e9d19d3e486cf8630194b7"
expected_finalize="cadec00fe7508fbbd88a889fb6b57707adeae649a51867c2cc4510cd51d362fc"
expected_kconfig="40e9bd827488a3f0bcac19bc0cc3760642337e815e6aa121b94eb1dca6e13c0d"
expected_header="0ac77e393b5fb3df26bb3a1ddeed9fe30ae3f0f0a95b80c95219c30761a0b96a"

for path in CHECKSUMS.json CMakeLists.txt cmake/compile_finalize.cmake Kconfig dl/dl_define_private.hpp; do test -f "${component}/${path}"; done
test "$(sha256sum "${component}/CHECKSUMS.json" | cut -d ' ' -f 1)" = "${expected_checksums}"
if grep -q 'config ESP_DL_REFERENCE_KERNELS' "${component}/Kconfig"; then exit 0; fi
test "$(sha256sum "${component}/Kconfig" | cut -d ' ' -f 1)" = "${expected_kconfig}"
test "$(sha256sum "${component}/CMakeLists.txt" | cut -d ' ' -f 1)" = "${expected_cmake}"
test "$(sha256sum "${component}/cmake/compile_finalize.cmake" | cut -d ' ' -f 1)" = "${expected_finalize}"
test "$(sha256sum "${component}/dl/dl_define_private.hpp" | cut -d ' ' -f 1)" = "${expected_header}"
patch --batch --forward --directory "${component}" --strip 1 < "${patch_file}"
