"""Additive catalog contracts; no CV model, GPU or RL policy execution."""
from copy import deepcopy
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "ml-repo" / "cv-dl-rl"
SPEC = importlib.util.spec_from_file_location("cv_dl_rl_collector", ROOT / "scripts" / "collect_ml_ecosystem.py")
COLLECTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COLLECTOR)
COLLECTOR.configure_catalog(DEST)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")


class FocusCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads((DEST / "selection.json").read_text(encoding="utf-8"))
        cls.snapshot = json.loads((DEST / "snapshot.json").read_text(encoding="utf-8"))
        cls.rows = cls.snapshot["entries"]
        cls.by_name = {r["repository"]: r for r in cls.rows}
        cls.original = json.loads((ROOT / "ml-repo/ecosystem/snapshot.json").read_text(encoding="utf-8"))["entries"]

    def test_declared_scope_and_three_routes(self):
        COLLECTOR.validate_selection(self.selection)
        self.assertFalse(self.snapshot["complete_ecosystem_inventory"])
        self.assertEqual(len(self.rows), 43)
        self.assertEqual(len(COLLECTOR.CATEGORIES), 3)
        counts = {k: sum(k in r["categories"] for r in self.rows) for k in COLLECTOR.CATEGORIES}
        self.assertEqual(counts, {"computer-vision": 16, "deep-learning": 11, "reinforcement-learning": 16})

    def test_no_overlap_or_fork_in_combined_116(self):
        names = [r["repository"].casefold() for r in self.rows + self.original]
        self.assertEqual(len(names), 116)
        self.assertEqual(len(names), len(set(names)))
        for row in self.rows:
            self.assertFalse(row["private"])
            self.assertFalse(row["fork"])
        self.assertNotIn("corl-team/CORL", self.by_name)
        self.assertIn("tinkoff-ai/CORL", self.by_name)

    def test_roles_distinguish_simulators_environment_and_algorithm(self):
        for row in self.rows:
            self.assertTrue(row["role"])
            self.assertTrue(row["use"])
            self.assertTrue(row["boundary"])
        self.assertEqual(self.by_name["google-deepmind/mujoco"]["role"], "simulator")
        self.assertEqual(self.by_name["Farama-Foundation/PettingZoo"]["role"], "environment-api")
        self.assertEqual(self.by_name["takuseno/d3rlpy"]["role"], "algorithm-toolkit")
        self.assertEqual(self.by_name["karpathy/micrograd"]["role"], "educational")

    def test_annotations_and_canonical_redirects(self):
        chosen = {r["repository"]: r for r in self.selection["entries"]}
        for row in self.rows:
            selected = chosen[row["requested_repository"]]
            for key in ("categories", "role", "use", "boundary", "reuse_policy"):
                self.assertEqual(row[key], selected[key])
        self.assertEqual(self.by_name["deepspeedai/DeepSpeed"]["requested_repository"], "microsoft/DeepSpeed")
        self.assertEqual(self.by_name["meta-pytorch/torchtune"]["requested_repository"], "pytorch/torchtune")

    def test_89_pinned_byte_verified_source_receipts(self):
        sources = []
        for row in self.rows:
            self.assertRegex(row["head"], r"^[a-f0-9]{40}$")
            self.assertTrue({"readme", "license"} <= {x["kind"] for x in row["sources"]})
            for source in row["sources"]:
                sources.append(source["url"])
                self.assertIn("/blob/" + row["head"] + "/", source["url"])
                self.assertRegex(source["blob_sha"], r"^[a-f0-9]{40}$")
                self.assertRegex(source["sha256"], r"^[a-f0-9]{64}$")
                self.assertGreater(source["bytes"], 0)
        self.assertEqual(len(sources), 89)
        self.assertEqual(len(set(sources)), 89)

    def test_per_query_timestamps_are_not_regeneration_times(self):
        completed = datetime.fromisoformat(self.snapshot["completed_at"])
        for row in self.rows:
            for key in ("metadata_observed_at", "sources_observed_at"):
                observed = datetime.fromisoformat(row[key])
                self.assertEqual(observed.utcoffset().total_seconds(), 28800)
                self.assertLessEqual(observed, completed)

    def test_license_classifier_is_not_permission(self):
        exceptions = [r for r in self.rows if r["license_signal"] == "NOASSERTION"]
        self.assertEqual(len(exceptions), 9)
        for row in exceptions:
            self.assertTrue(row["source_review_note"])
            self.assertEqual(row["license_class"], "needs-license-review")
        yolo = self.by_name["ultralytics/ultralytics"]
        self.assertEqual(yolo["license_class"], "reciprocal-signal-review-text")
        self.assertIn("非商业", yolo["source_review_note"])
        mini = self.by_name["Farama-Foundation/Minigrid"]
        self.assertIn("@@", mini["source_review_note"])
        self.assertEqual(mini["reuse_policy"], "reference-only-license-clarification")

    def test_extra_license_files_are_captured_and_linked(self):
        book = self.by_name["d2l-ai/d2l-en"]
        self.assertTrue({"LICENSE-SAMPLECODE", "LICENSE-SUMMARY"} <= {s["path"] for s in book["sources"]})
        self.assertIn("modified MIT", book["source_review_note"])
        self.assertIn("CC BY-SA", book["source_review_note"])
        sam = self.by_name["facebookresearch/sam2"]
        self.assertIn("LICENSE_cctorch", {s["path"] for s in sam["sources"]})

    def test_archive_and_maintenance_do_not_imply_live_support(self):
        self.assertEqual({r["repository"] for r in self.rows if r["archived"]}, {"tinkoff-ai/CORL", "facebookresearch/mbrl-lib"})
        self.assertIn("deprecated", self.by_name["karpathy/nanoGPT"]["source_review_note"])
        self.assertIn("karpathy/nanochat", self.by_name)
        self.assertIn("brax/training", self.by_name["google/brax"]["source_review_note"])
        self.assertIn("Minari", self.by_name["Farama-Foundation/D4RL"]["source_review_note"])

    def test_generated_routes_cover_all_sources_and_roles(self):
        seen = set()
        for key in COLLECTOR.CATEGORIES:
            text = (DEST / (key + ".md")).read_text(encoding="utf-8")
            self.assertIn("NOT_RUN", text)
            for row in self.rows:
                if key in row["categories"]:
                    self.assertIn("`" + row["role"] + "`", text)
                    for source in row["sources"]:
                        self.assertIn(source["url"], text)
                        seen.add(source["url"])
        self.assertEqual(len(seen), 89)

    def test_links_privacy_and_lf_output(self):
        allowed = {s["url"] for row in self.rows for s in row["sources"]}
        for path in list(DEST.glob("*.md")) + list(DEST.glob("*.json")):
            self.assertNotIn(b"\r", path.read_bytes())
            text = path.read_text(encoding="utf-8")
            for pattern in (r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]", r"github_pat_[A-Za-z0-9_]{30,}", r"gh[pousr]_[A-Za-z0-9]{30,}", r"file://"):
                self.assertIsNone(re.search(pattern, text), path.name)
            if path.suffix != ".md":
                continue
            for href in LINK.findall(text):
                if href.startswith("https://github.com/") and "/blob/" in href:
                    self.assertIn(href, allowed)
                elif not re.match(r"[a-z]+:", href) and not href.startswith("#"):
                    target = (path.parent / unquote(href.split("#", 1)[0])).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.exists(), (path, href))

    def test_configured_destination_cannot_escape_catalog(self):
        original = COLLECTOR.DEST
        for directory in (ROOT / "ml-repo", ROOT / "report", ROOT.parent / "other-project"):
            with self.assertRaises(ValueError):
                COLLECTOR.configure_catalog(directory)
        self.assertEqual(COLLECTOR.DEST, original)

    def test_invalid_taxonomy_is_rejected_without_mutating_globals(self):
        previous = COLLECTOR.CATEGORIES.copy()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            dest = root / "ml-repo" / "fixture"
            dest.mkdir(parents=True)
            (dest / "taxonomy.json").write_text(json.dumps({"../escape": ["title", "dimension"]}), encoding="utf-8")
            with patch.object(COLLECTOR, "ROOT", root), self.assertRaises(ValueError):
                COLLECTOR.configure_catalog(dest)
        self.assertEqual(COLLECTOR.CATEGORIES, previous)

    def test_extra_source_cannot_escape_root_tree(self):
        selection = deepcopy(self.selection)
        selection["entries"] = [selection["entries"][0]]
        selection["entries"][0]["additional_root_sources"] = ["../LICENSE"]
        info = {"nameWithOwner": "opencv/opencv", "isPrivate": False, "isFork": False,
                "defaultBranchRef": {"target": {"oid": "a" * 40, "tree": {"entries": [
                    {"name": "README.md", "oid": "b" * 40, "type": "blob"},
                    {"name": "LICENSE", "oid": "c" * 40, "type": "blob"}]}}}}
        with TemporaryDirectory() as directory, patch.object(COLLECTOR, "ROOT", Path(directory)), patch.object(COLLECTOR.json, "loads", return_value=selection), patch.object(COLLECTOR, "query_github", return_value={"data": {"r0": info}}) as query:
            with self.assertRaises(ValueError):
                COLLECTOR.collect(Path(directory) / ".local" / "review")
            self.assertEqual(query.call_count, 1)

    def test_unrun_experiments_have_fixed_protocols_not_claims(self):
        for row in self.rows:
            self.assertEqual(row["runtime_evaluation"], "NOT_RUN")
            self.assertEqual(row["quality_gain"], "UNMEASURED")
        text = (DEST / "EXPERIMENT_PROTOCOL.md").read_text(encoding="utf-8")
        for item in ("PROPOSED / NOT_RUN", "finite differences", "checkpoint", "interactions", "negative", "real-world", "Baseline → Change → Measure → Result → Trade-off → Next Action"):
            self.assertIn(item.casefold(), text.casefold())


if __name__ == "__main__":
    unittest.main()
