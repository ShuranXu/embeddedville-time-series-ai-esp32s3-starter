PYTHON ?= .venv/bin/python

.PHONY: ready explore preprocess train export firmware qemu evidence package test
ready:
	$(PYTHON) scripts/readiness.py
explore:
	$(PYTHON) src/01_explore_data.py --input data/baseline/bme280_sample.csv --output-dir outputs/release
preprocess:
	$(PYTHON) src/02_preprocessing.py --input data/baseline/bme280_sample.csv
train:
	$(PYTHON) src/03_train_lstm.py
export:
	$(PYTHON) src/04_export_onnx.py && $(PYTHON) src/05_evaluate_onnx.py && $(PYTHON) src/06_quantize_espdl.py
firmware:
	bash scripts/build-firmware.sh
qemu:
	bash scripts/run-qemu.sh
evidence:
	$(PYTHON) scripts/collect_evidence.py
package:
	$(PYTHON) submission/build_submission.py tsai-capstone-predictive-node --output submission/out/capstone.zip
test:
	$(PYTHON) -m unittest discover -s tests -v

