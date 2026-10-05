import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_identity_and_no_public_solution_tree(self):
        contract = json.loads((ROOT / "course-version.json").read_text())
        self.assertEqual(contract["courseId"], "time-series-ai-esp32s3")
        self.assertFalse((ROOT / "solutions").exists())

    def test_original_artifacts_present(self):
        for path in ["data/baseline/bme280_sample.csv", "models/original/best_lstm.pt", "models/original/sensor_lstm.onnx", "outputs/original/01_channels.png", "outputs/original/training_curve.png", "outputs/original/05_predictions.png", "outputs/original/05_metrics.txt"]:
            self.assertTrue((ROOT / path).is_file(), path)

if __name__ == "__main__":
    unittest.main()
