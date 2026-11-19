import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1] / "ml-project" / "kaggle-matcher"
CLI = ROOT / "matcher.py"
MATCH = runpy.run_path(str(CLI))["match_competition"]


class KaggleMatcherTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(CLI), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=10)

    def test_frozen_description_fixtures(self):
        cases = json.loads((ROOT / "eval_cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 24)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                result = MATCH(description=case["text"])
                self.assertEqual((result["task"], result["learning"]), (case["task"], case["learning"]))
                self.assertEqual(result["basis"], "description_rules")
                self.assertIsNone(result["metric"])

    def test_curated_profiles_and_provenance(self):
        expected = {"titanic": "tabular-classification", "digit-recognizer": "image-classification",
                    "house-prices-advanced-regression-techniques": "tabular-regression",
                    "store-sales-time-series-forecasting": "forecasting",
                    "llm-detect-ai-generated-text": "text-classification", "connectx": "sequential-decision"}
        for slug, task in expected.items():
            with self.subTest(competition=slug):
                result = MATCH(slug)
                self.assertEqual(result["task"], task)
                self.assertEqual(result["basis"], "curated_snapshot")
                self.assertEqual(result["competition"], slug)
                self.assertTrue(result["plans"]["baseline"]["method"])
                self.assertTrue(result["metric"])
                self.assertIn(f"/{slug}", result["source"])
                self.assertEqual(result["runtime_evidence"], "UNMEASURED")

    def test_url_variants_map_to_same_profile(self):
        self.assertEqual(MATCH("https://www.kaggle.com/competitions/Titanic/data?foo=bar#section"), MATCH("titanic"))
        self.assertEqual(MATCH("https://kaggle.com/c/titanic/"), MATCH("titanic"))

    def test_reject_malformed_or_wrong_site_urls(self):
        for url in ("http://www.kaggle.com/c/titanic", "https://kaggle.com.evil.org/c/titanic",
                    "https://kaggle.com@other.org/c/titanic", "https://foo@kaggle.com/c/titanic",
                    "https://kaggle.com/datasets/example/titanic", "https://kaggle.com/c/../titanic"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                MATCH(url, "tabular classification")

    def test_unknown_slug_asks_for_description(self):
        result = self.cli("https://www.kaggle.com/competitions/new-case")
        self.assertEqual(result.returncode, 2)
        self.assertIn("provide --description", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(MATCH("new-case", "tabular classification")["task"], "tabular-classification")

    def test_no_evidence_means_no_method_or_hardware_guess(self):
        report = MATCH(description="Kaggle contest. Cash reward.")
        self.assertEqual(report["task"], "unknown")
        self.assertEqual(report["plans"], {})
        self.assertIn("Clarify", report["checks"][0])

    def test_description_can_override_curated_route_but_not_rule_provenance(self):
        report = MATCH("titanic", "Object detection with bounding boxes for images.")
        self.assertEqual(report["basis"], "description_rules")
        self.assertEqual(report["task"], "object-detection")
        self.assertEqual(report["metric"], "categorization accuracy")
        self.assertIn("Pasted task differs", report["checks"][0])

    def test_supervised_dl_and_optional_rl_are_distinct(self):
        digit = MATCH("digit-recognizer")
        self.assertEqual(digit["learning"], "supervised")
        self.assertTrue(digit["deep_learning_route"])
        self.assertEqual(digit["plans"]["baseline"]["kaggle"]["profile"], "kaggle_cpu")
        self.assertEqual(digit["plans"]["next"]["kaggle"]["profile"], "kaggle_t4x2")
        self.assertEqual(digit["plans"]["next"]["family"], "deep-learning")
        connectx = MATCH("connectx")
        self.assertEqual(connectx["learning"], "reinforcement-learning-optional")
        self.assertFalse(connectx["deep_learning_route"])
        self.assertIn("minimax", connectx["plans"]["baseline"]["method"])
        self.assertEqual(connectx["plans"]["next"]["family"], "reinforcement-learning")
        self.assertIsNone(connectx["plans"]["baseline"]["submission_runtime"])

    def test_labeled_anomaly_plan_differs_from_unlabeled(self):
        labeled = MATCH(description="Anomaly detection with labeled examples.")
        unlabeled = MATCH(description="Anomaly detection with unlabeled data.")
        self.assertIn("logistic", labeled["plans"]["baseline"]["method"])
        self.assertIn("Isolation Forest", unlabeled["plans"]["baseline"]["method"])

    def test_cpu_baseline_and_exact_planning_budget(self):
        result = MATCH("titanic", overrides={"cpu_cores": 4, "ram_gib": 24, "hours": 10})
        baseline, next_plan = (result["plans"][name] for name in ("baseline", "next"))
        self.assertEqual(baseline["kaggle"]["fit"], "likely_for_pilot")
        self.assertEqual(baseline["resources"]["ram_gib"], {"range": [24, 24], "source": "user_input"})
        self.assertEqual(next_plan["resources"]["ram_gib"]["source"], "heuristic")

    def test_single_gpu_not_pooled_and_dl_flag_unchanged(self):
        report = MATCH("digit-recognizer", plan="next", overrides={"vram_gib": 20})
        candidate = report["plans"]["next"]["kaggle"]
        self.assertTrue(report["deep_learning_route"])
        self.assertEqual(candidate["profile"], "kaggle_t4x2")
        self.assertEqual(candidate["fit"], "above_planning_budget")
        self.assertEqual(candidate["limiting_fields"], ["vram_gib"])
        self.assertEqual(report["plans"]["baseline"]["kaggle"]["profile"], "kaggle_cpu")

    def test_fit_margins_and_multiple_resource_excesses(self):
        result = MATCH(description="Image segmentation with pixel masks.")
        self.assertEqual(result["plans"]["next"]["kaggle"]["fit"], "pilot_required")
        result = MATCH("titanic", overrides={"cpu_cores": 8, "ram_gib": 32, "hours": 11})
        self.assertEqual(result["plans"]["baseline"]["kaggle"]["limiting_fields"], ["cpu_cores", "ram_gib", "hours"])

    def test_submission_runtime_is_separate(self):
        historical = MATCH("llm-detect-ai-generated-text")
        self.assertEqual(historical["plans"]["next"]["submission_runtime"]["limit_hours"], 9)
        self.assertEqual(historical["submission_limit_source"], "curated_snapshot")
        for hours, expected in ((0.01, "above"), (0.5, "overlaps"), (1.0, "within")):
            result = MATCH("titanic", submission_hours=hours)
            self.assertEqual(result["plans"]["baseline"]["submission_runtime"]["estimate_relation"], expected)
            self.assertEqual(result["plans"]["baseline"]["kaggle"]["fit"], "likely_for_pilot")
            self.assertEqual(result["submission_limit_source"], "user_input")

    def test_invalid_overrides(self):
        for patch in ({"cpu_cores": 1.5}, {"ram_gib": 0}, {"vram_gib": -1}, {"hours": float("nan")},
                      {"hours": float("inf")}, {"unrecognized": 10}, {"cpu_cores": True}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                MATCH("titanic", overrides=patch)
        with self.assertRaisesRegex(ValueError, "no next workload"):
            MATCH(description="Binary classification", plan="next", overrides={"cpu_cores": 3})

    def test_cli_version_list_and_json(self):
        self.assertEqual(self.cli("--version").stdout.strip(), "0.1.0")
        result = self.cli("--list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 6)
        result = self.cli("titanic", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), MATCH("titanic"))
        self.assertIn("Actual resource use: UNMEASURED", self.cli("titanic").stdout)

    def test_cli_description_file_and_bad_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.txt"
            path.write_text("音频分类。", encoding="utf-8-sig")
            result = self.cli("--description-file", str(path), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["task"], "audio-classification")
            path.write_text("a" * 32_001, encoding="utf-8")
            self.assertEqual(self.cli("--description-file", str(path)).returncode, 2)
            path.write_bytes(b"\xff")
            self.assertEqual(self.cli("--description-file", str(path)).returncode, 2)
        for args in ((), ("--description", " "), ("titanic", "--hours", "inf"), ("--list", "titanic")):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
