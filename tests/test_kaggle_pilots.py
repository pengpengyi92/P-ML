import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


PILOTS = Path(__file__).resolve().parents[1] / "ml-project" / "kaggle-matcher" / "pilots"
COMPARE = runpy.run_path(str(PILOTS / "compare.py"))["compare"]


class KagglePilotEvidenceTests(unittest.TestCase):
    def receipt(self, name):
        return json.loads((PILOTS / "evidence" / f"{name}.json").read_text(encoding="utf-8"))

    def test_recorded_pilots_match_expected_fit_not_range(self):
        cpu, gpu = (COMPARE(self.receipt(name)) for name in ("titanic", "digit-recognizer"))
        for result in (cpu, gpu):
            self.assertEqual(result["estimated_fit"], "likely_for_pilot")
            self.assertTrue(result["fits_observed_budgets"])
            self.assertEqual(result["cpu_configuration"], {"compute_threads": 2, "available_cores": 4, "within_budget": True})
            self.assertEqual(result["measurements"]["hours"]["range_relation"], "below")
            self.assertEqual(result["measurements"]["ram_gib"]["range_relation"], "below")
        self.assertEqual(cpu["measurements"]["vram_gib"]["observed"], 0)
        self.assertEqual(gpu["measurements"]["vram_gib"]["range_relation"], "below")

    def test_comparison_fails_closed_on_bad_provenance_or_missing_gpu(self):
        cpu = self.receipt("titanic")
        cpu["script_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "different pilot.py"):
            COMPARE(cpu)
        gpu = self.receipt("digit-recognizer")
        gpu["gpu"] = None
        with self.assertRaisesRegex(ValueError, "missing T4"):
            COMPARE(gpu)

    def test_above_budget_is_separate_from_profile_estimate(self):
        counterfactual = self.receipt("titanic")
        counterfactual["process_peak_rss_bytes"] = 25 * 1024 ** 3
        result = COMPARE(counterfactual)
        self.assertEqual(result["estimated_fit"], "likely_for_pilot")
        self.assertFalse(result["fits_observed_budgets"])

    def test_prepare_is_private_offline_and_copies_exact_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "packages"
            env = dict(os.environ, PYTHONUTF8="1")
            run = subprocess.run([sys.executable, "-B", str(PILOTS / "prepare.py"), "--owner", "example",
                                  "--suffix", "fix1", "--out", str(path)], env=env, capture_output=True,
                                 encoding="utf-8", text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            for case, slug in (("cpu", "titanic"), ("gpu", "digit-recognizer")):
                folder = path / case
                metadata = json.loads((folder / "kernel-metadata.json").read_text(encoding="utf-8"))
                self.assertEqual(metadata["competition_sources"], [slug])
                self.assertTrue(metadata["is_private"])
                self.assertFalse(metadata["enable_internet"])
                self.assertEqual(metadata["enable_gpu"], case == "gpu")
                self.assertFalse(metadata["enable_tpu"])
                self.assertEqual((folder / metadata["code_file"]).read_bytes(), (PILOTS / "pilot.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
