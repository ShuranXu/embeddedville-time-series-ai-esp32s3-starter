#include <cstdio>

extern "C" void app_main(void) {
  // TODO(Lab 4): load the quantized .espdl artifact, assign the recorded 1x24x3
  // window, run ESP-DL inference, compare with the accepted ONNX output, and
  // emit the required JSONL evidence. Do not replace target inference with a
  // host-side or hard-coded prediction.
  std::printf("{\"event\":\"course_summary\",\"passed\":false,\"reason\":\"TODO\"}\n");
}

