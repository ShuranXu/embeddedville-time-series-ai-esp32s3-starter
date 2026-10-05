import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_identity_and_no_public_solution_tree(self):
        contract = json.loads((ROOT / "course-version.json").read_text())
        self.assertEqual(contract["courseId"], "time-series-ai-esp32s3")
        self.assertFalse((ROOT / "solutions").exists())
        self.assertEqual(contract["starterTag"], "starter-v1.0.1")
        self.assertEqual(contract["evaluatorContract"], "2026.10-evaluator-v2")

    def test_original_artifacts_present(self):
        for path in ["data/baseline/bme280_sample.csv", "models/original/best_lstm.pt", "models/original/sensor_lstm.onnx", "outputs/original/01_channels.png", "outputs/original/training_curve.png", "outputs/original/05_predictions.png", "outputs/original/05_metrics.txt"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_uart_parser_rejects_claimed_pass_without_fault_case(self):
        with tempfile.TemporaryDirectory() as directory:
            uart = Path(directory) / "forged.log"
            uart.write_text('\n'.join([
                '{"event":"embedded_model_test","passed":true}',
                '{"event":"inference","output":[0,0,0],"expected":[0,0,0],"parity":true}',
                '{"event":"course_summary","unexpected_failures":0,"passed":true}',
            ]), encoding="utf-8")
            result = subprocess.run(["python3", str(ROOT / "scripts" / "parse-qemu-uart.py"), str(uart)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_submission_schema_v2_excludes_generated_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "submission.zip"
            subprocess.run(["python3", str(ROOT / "submission" / "build_submission.py"), "tsai-capstone-predictive-node", "--output", str(archive)], check=True)
            with zipfile.ZipFile(archive) as package:
                names = package.namelist()
                manifest = json.loads(package.read("submission-manifest.json"))
        self.assertEqual(manifest["schemaVersion"], 2)
        self.assertEqual(manifest["evaluatorContract"], "2026.10-evaluator-v2")
        self.assertFalse(any(name.endswith("qemu-uart.log") or name.endswith("parity.json") or name.endswith(".bin") for name in names))
        self.assertTrue(all("role" in entry for entry in manifest["files"]))

if __name__ == "__main__":
    unittest.main()
