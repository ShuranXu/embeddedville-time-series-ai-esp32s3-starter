"""Lab 3B scaffold derived from the original ONNX export script."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPSET = 18

def main() -> None:
    # TODO(Lab 3B): load your accepted checkpoint, export fixed input shape
    # 1x24x3 at opset 18, inline all weights, and prove PyTorch/ONNX parity.
    raise NotImplementedError("complete the opset 18 export and parity report")

if __name__ == "__main__":
    main()

