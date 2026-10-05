"""Lab 3B evaluation scaffold derived from the original PC verifier."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    # TODO(Lab 3B): run every held-out window through ONNX Runtime, inverse
    # normalize, report MAE/RMSE/MAPE/R2, and compare against persistence.
    raise NotImplementedError("complete held-out evaluation")

if __name__ == "__main__":
    main()

