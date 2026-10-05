idf_build_get_property(component_targets __COMPONENT_TARGETS)
if("___idf_espressif__esp-dl" IN_LIST component_targets)
  idf_component_get_property(espdl_dir espressif__esp-dl COMPONENT_DIR)
elseif("___idf_esp-dl" IN_LIST component_targets)
  idf_component_get_property(espdl_dir esp-dl COMPONENT_DIR)
else()
  message(FATAL_ERROR "ESP-DL component is required")
endif()

set(cmake_dir ${espdl_dir}/fbs_loader/cmake)
include(${cmake_dir}/utilities.cmake)
set(embed_files ${CMAKE_CURRENT_LIST_DIR}/../model/sensor_lstm_s3_w8a8.espdl)

idf_component_register(SRCS "app_main.cpp" INCLUDE_DIRS ".")
target_add_aligned_binary_data(${COMPONENT_LIB} ${embed_files} BINARY)

