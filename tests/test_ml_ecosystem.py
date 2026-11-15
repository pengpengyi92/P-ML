"""Offline evidence contracts; these do not benchmark third-party ML software."""
from copy import deepcopy
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "ml-repo" / "ecosystem"
SPEC = importlib.util.spec_from_file_location("ml_collector", ROOT / "scripts" / "collect_ml_ecosystem.py")
COLLECTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COLLECTOR)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")


class MLEcosystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads((DEST / "selection.json").read_text(encoding="utf-8"))
        cls.snapshot = json.loads((DEST / "snapshot.json").read_text(encoding="utf-8"))
        cls.rows = cls.snapshot["entries"]

    def test_declared_scope_and_selection(self):
        COLLECTOR.validate_selection(self.selection)
        self.assertFalse(self.snapshot["complete_ecosystem_inventory"])
        self.assertEqual(len(self.rows), 73)
        self.assertEqual(len(self.rows), len(self.selection["entries"]))
        self.assertEqual({r["requested_repository"] for r in self.rows}, {r["repository"] for r in self.selection["entries"]})

    def test_unique_public_primary_sources(self):
        names = set()
        for row in self.rows:
            self.assertFalse(row["private"])
            self.assertFalse(row["fork"])
            self.assertNotIn(row["repository"].casefold(), names)
            names.add(row["repository"].casefold())
            self.assertEqual(row["url"], "https://github.com/" + row["repository"])

    def test_learning_domains_and_engineering_are_separate_dimensions(self):
        covered = {category for row in self.rows for category in row["categories"]}
        self.assertEqual(covered, set(COLLECTOR.CATEGORIES))
        self.assertEqual(len(covered), 15)
        self.assertEqual(COLLECTOR.CATEGORIES["supervised"][1], "learning-paradigm")
        self.assertEqual(COLLECTOR.CATEGORIES["vision"][1], "application-domain")
        self.assertEqual(COLLECTOR.CATEGORIES["frameworks"][1], "engineering")
        self.assertGreater(sum(len(row["categories"]) for row in self.rows), len(self.rows))

    def test_source_pins_and_byte_integrity_receipts(self):
        count = 0
        for row in self.rows:
            self.assertRegex(row["head"], r"^[a-f0-9]{40}$")
            self.assertEqual({x["kind"] for x in row["sources"]}, {"readme", "license"})
            for source in row["sources"]:
                count += 1
                self.assertIn("/blob/" + row["head"] + "/", source["url"])
                self.assertRegex(source["blob_sha"], r"^[a-f0-9]{40}$")
                self.assertRegex(source["sha256"], r"^[a-f0-9]{64}$")
                self.assertGreater(source["bytes"], 0)
        self.assertEqual(count, 146)

    def test_timestamps_do_not_replace_old_observations(self):
        end = datetime.fromisoformat(self.snapshot["completed_at"])
        for row in self.rows:
            for key in ("metadata_observed_at", "sources_observed_at"):
                observed = datetime.fromisoformat(row[key])
                self.assertEqual(observed.utcoffset().total_seconds(), 28800)
                self.assertLessEqual(observed, end)
        self.assertIsInstance(self.snapshot["resume"], bool)
        if not self.snapshot["resume"]:
            self.assertTrue(all(datetime.fromisoformat(r["metadata_observed_at"]) >= datetime.fromisoformat(self.snapshot["started_at"]) for r in self.rows))

    def test_annotations_are_preserved_separately_from_observed_facts(self):
        annotations = {r["repository"]: r for r in self.selection["entries"]}
        for row in self.rows:
            selected = annotations[row["requested_repository"]]
            for key in ("categories", "use", "boundary", "reuse_policy"):
                self.assertEqual(row[key], selected[key])

    def test_redirects_are_not_duplicate_claims(self):
        names = {r["requested_repository"]: r["repository"] for r in self.rows}
        self.assertEqual(names["microsoft/LightGBM"], "lightgbm-org/LightGBM")
        self.assertEqual(names["huggingface/safetensors"], "safetensors/safetensors")
        self.assertEqual(names["pytorch/captum"], "meta-pytorch/captum")

    def test_archive_and_restricted_references_are_not_promoted(self):
        rows = {r["repository"]: r for r in self.rows}
        self.assertTrue(rows["facebookresearch/mae"]["archived"])
        self.assertTrue(rows["microsoft/Semi-supervised-learning"]["archived"])
        mae = rows["facebookresearch/mae"]
        self.assertEqual(mae["reuse_policy"], "restricted-noncommercial-reference")
        self.assertIn("CC BY-NC 4.0", mae["source_review_note"])
        page = (DEST / "self-semi-supervised.md").read_text(encoding="utf-8")
        self.assertIn("REFERENCE ONLY: NONCOMMERCIAL", page)
        self.assertIn("maintenance phase", rows["pytorch/audio"]["source_review_note"])

    def test_license_classifier_negative_controls(self):
        for signal in (None, "NOASSERTION", "CC-BY-NC-4.0", "BUSL-1.1", "LicenseRef-Proprietary"):
            self.assertEqual(COLLECTOR.license_class(signal), "needs-license-review")
        self.assertEqual(COLLECTOR.license_class("AGPL-3.0"), "reciprocal-signal-review-text")
        self.assertEqual(COLLECTOR.license_class("MIT"), "permissive-signal-review-text")
        for row in self.rows:
            self.assertEqual(row["license_class"], COLLECTOR.license_class(row["license_signal"]))

    def test_unknown_classifier_has_source_specific_notes(self):
        for row in self.rows:
            if row["license_signal"] == "NOASSERTION":
                self.assertTrue(row["source_review_note"])
        rows = {r["repository"]: r for r in self.rows}
        self.assertIn("Apache", rows["vwxyzjn/cleanrl"]["source_review_note"])
        self.assertIn("AePPL", rows["pymc-devs/pymc"]["source_review_note"])

    def test_generated_routes_contain_exact_source_links(self):
        observed = set()
        for category in COLLECTOR.CATEGORIES:
            text = (DEST / (category + ".md")).read_text(encoding="utf-8")
            self.assertIn("NOT_RUN", text)
            for row in self.rows:
                if category in row["categories"]:
                    self.assertIn(row["url"], text)
                    for source in row["sources"]:
                        self.assertIn(source["url"], text)
                        observed.add(source["url"])
        expected = {s["url"] for row in self.rows for s in row["sources"]}
        self.assertEqual(observed, expected)

    def test_all_catalog_links_are_local_safe_or_pinned_public(self):
        allowed = {s["url"] for row in self.rows for s in row["sources"]}
        for path in DEST.glob("*.md"):
            for href in LINK.findall(path.read_text(encoding="utf-8")):
                if href.startswith("https://github.com/") and "/blob/" in href:
                    self.assertIn(href, allowed)
                elif not re.match(r"[a-z]+:", href) and not href.startswith("#"):
                    target = (path.parent / unquote(href.split("#", 1)[0])).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.exists(), (path, href))

    def test_public_material_has_no_workstation_or_credentials(self):
        paths = list(DEST.glob("*.json")) + list(DEST.glob("*.md"))
        paths += list((ROOT / "report").glob("*.md")) + list((ROOT / "log").glob("*.md"))
        for path in paths:
            self.assertNotIn(b"\r", path.read_bytes(), path.name)
            text = path.read_text(encoding="utf-8")
            for pattern in (r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]", r"github_pat_[A-Za-z0-9_]{30,}", r"gh[pousr]_[A-Za-z0-9]{30,}", r"file://"):
                self.assertIsNone(re.search(pattern, text), path.name)

    def test_runtime_and_benefits_are_not_fabricated(self):
        for row in self.rows:
            self.assertEqual(row["runtime_evaluation"], "NOT_RUN")
            self.assertEqual(row["quality_gain"], "UNMEASURED")
        protocol = (DEST / "EXPERIMENT_PROTOCOL.md").read_text(encoding="utf-8")
        for phrase in ("PROPOSED / NOT_RUN", "final testing", "negative control", "universal score", "Baseline → Change → Measure → Result → Trade-off → Next Action"):
            self.assertIn(phrase, protocol)

    def test_duplicate_and_invalid_selection_rejected(self):
        duplicate = deepcopy(self.selection)
        duplicate["entries"].append(duplicate["entries"][0])
        with self.assertRaises(ValueError):
            COLLECTOR.validate_selection(duplicate)
        invalid = deepcopy(self.selection)
        invalid["entries"][0]["repository"] = "../../private"
        with self.assertRaises(ValueError):
            COLLECTOR.validate_selection(invalid)
        invalid["entries"][0]["repository"] = "owner/name"
        invalid["entries"][0]["categories"] = ["invalid"]
        with self.assertRaises(ValueError):
            COLLECTOR.validate_selection(invalid)

    def test_integrity_oracle_accepts_exact_blob(self):
        text = "fixture\n"
        content = text.encode()
        oid = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
        blob = {"oid": oid, "byteSize": len(content), "isBinary": False, "text": text}
        result = COLLECTOR.source_blob("owner/repo", "a" * 40, "README.md", blob, oid)
        self.assertEqual(result["sha256"], hashlib.sha256(content).hexdigest())

    def test_integrity_oracle_rejects_changed_binary_or_truncated_content(self):
        blob = {"oid": "a" * 40, "byteSize": 7, "isBinary": False, "text": "changed"}
        with self.assertRaises(ValueError):
            COLLECTOR.source_blob("owner/repo", "b" * 40, "README.md", blob, "a" * 40)
        blob["isBinary"] = True
        with self.assertRaises(ValueError):
            COLLECTOR.source_blob("owner/repo", "b" * 40, "README.md", blob, "a" * 40)

    def test_raw_output_cannot_enter_public_catalog_or_report(self):
        with patch.object(COLLECTOR.subprocess, "run") as run:
            for path in (DEST / "raw", ROOT / "report" / "raw"):
                with self.assertRaises(ValueError):
                    COLLECTOR.collect(path)
            run.assert_not_called()

    def test_private_repository_negative_control(self):
        private_response = {"data": {"r0": {"isPrivate": True}}}
        with TemporaryDirectory() as directory, patch.object(COLLECTOR, "ROOT", Path(directory)), patch.object(COLLECTOR, "query_github", return_value=private_response) as query:
            with self.assertRaises(ValueError):
                COLLECTOR.collect(Path(directory) / ".local" / "review")
            self.assertEqual(query.call_count, 1)

    def test_resume_preserves_original_cache_observation(self):
        query = "query{viewer{login}}"
        digest = hashlib.sha256(query.encode()).hexdigest()
        record = {"query_sha256": digest, "observed_at": "2026-11-14T01:02:03+08:00", "data": {"fixture": True}}
        with TemporaryDirectory() as directory:
            cache = Path(directory)
            (cache / (digest + ".json")).write_text(json.dumps(record), encoding="utf-8")
            with patch.object(COLLECTOR.subprocess, "run") as run:
                actual = COLLECTOR.query_github(query, cache, resume=True)
                self.assertEqual(actual, record)
                run.assert_not_called()

    def test_graphql_partial_error_is_not_success(self):
        result = subprocess.CompletedProcess([], 0, json.dumps({"data": {}, "errors": [{"message": "denied"}]}), "")
        with TemporaryDirectory() as directory, patch.object(COLLECTOR.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError):
                COLLECTOR.query_github("query{fixture}", Path(directory))

    def test_http_failure_is_bounded_and_not_missing_license(self):
        result = subprocess.CompletedProcess([], 1, "", "HTTP 403")
        with TemporaryDirectory() as directory, patch.object(COLLECTOR.subprocess, "run", return_value=result) as run, patch.object(COLLECTOR.time, "sleep"):
            with self.assertRaises(RuntimeError):
                COLLECTOR.query_github("query{fixture}", Path(directory))
            self.assertEqual(run.call_count, 2)


if __name__ == "__main__":
    unittest.main()
