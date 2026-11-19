"""Verify the saved pilot receipts and compare to matcher v0.1.0 planning ranges."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import runpy


HERE = Path(__file__).resolve().parent
GIB = 1024 ** 3
CPU_V1_SHA256 = "c02016085f34ca0ae52af01061447caef218f7d8cef2146a6b4edf6010f7eae1"
CONTRACTS = {
    "titanic": ("baseline", "logistic-regression", 891, 712, 179, 61194),
    "digit-recognizer": ("next", "small-cnn", 42000, 12000, 3000, 76775041),
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def positive(value):
    return type(value) in (int, float) and value > 0 and math.isfinite(value)


def compare(receipt):
    slug = receipt["competition"]
    check(slug in CONTRACTS and receipt["schema"] == 1, "unexpected pilot receipt")
    stage, method, source_rows, train_rows, valid_rows, input_bytes = CONTRACTS[slug]
    check((receipt["method"], receipt["source_rows"], receipt["train_rows"], receipt["validation_rows"],
           receipt["input_bytes"], receipt["seed"], receipt["threads"]) ==
          (method, source_rows, train_rows, valid_rows, input_bytes, 42, 2), "fixed pilot configuration changed")
    check(bool(re.fullmatch(r"[0-9a-f]{64}", receipt["input_sha256"])), "missing input fingerprint")
    # CPU ran before the GPU-only counter initialization fix.
    expected_scripts = {hashlib.sha256((HERE / "pilot.py").read_bytes()).hexdigest()}
    if slug == "titanic":
        expected_scripts.add(CPU_V1_SHA256)
    check(receipt["script_sha256"] in expected_scripts,
          "receipt was produced by a different pilot.py")
    check(positive(receipt["fit_seconds"]) and positive(receipt["wall_seconds"]) and
          receipt["fit_seconds"] <= receipt["wall_seconds"] <= 300 and positive(receipt["process_peak_rss_bytes"]),
          "invalid timing or memory evidence")
    check(0 <= receipt["validation_accuracy"] <= 1, "invalid held-out accuracy")
    gpu = receipt["gpu"]
    vram_gib = 0.0
    if stage == "next":
        check(gpu and receipt["epochs"] == 3 and receipt["batch_size"] == 128 and
              gpu["training_device"] == "cuda:0" and "T4" in gpu["cuda_device_name"] and gpu["samples"] >= 2,
              "missing T4 CNN execution evidence")
        check(0 < gpu["torch_peak_allocated_bytes"] <= gpu["torch_peak_reserved_bytes"], "invalid allocator peaks")
        cards = gpu["cards"]
        check(len(cards) == gpu["cuda_visible_count"] == 2 and {c["index"] for c in cards} == {0, 1},
              "T4x2 profile was not verified")
        check(all("T4" in card["name"] and 0 <= card["initial_used_mib"] <= card["sampled_peak_used_mib"] <= card["total_mib"]
                  for card in cards), "invalid per-card peaks")
        vram_gib = max(max(card["sampled_peak_used_mib"] for card in cards) / 1024,
                       gpu["torch_peak_reserved_bytes"] / GIB)
    else:
        check(gpu is None, "CPU plan unexpectedly used an accelerator")

    match = runpy.run_path(str(HERE.parent / "matcher.py"))["match_competition"](slug)
    check(match["version"] == "0.1.0", "update the comparison for a new matcher version")
    plan = match["plans"][stage]
    quota = receipt["cgroup_cpu_max"]
    check(isinstance(quota, str) and bool(re.fullmatch(r"[1-9]\d* [1-9]\d*", quota)), "missing CPU quota evidence")
    period_quota, period = map(int, quota.split())
    effective_cores = min(receipt["affinity_cpus"], period_quota / period)
    threads = receipt["threads"]
    cpu_fit = threads <= min(effective_cores, plan["kaggle"]["planning_budget"]["cpu_cores"])
    observations = {"hours": receipt["wall_seconds"] / 3600,
                    "ram_gib": receipt["process_peak_rss_bytes"] / GIB, "vram_gib": vram_gib}
    comparisons = {}
    for key, value in observations.items():
        low, high = plan["resources"][key]["range"]
        budget = plan["kaggle"]["planning_budget"][key]
        comparisons[key] = {"observed": value, "planning_range": [low, high], "planning_budget": budget,
                            "range_relation": "below" if value < low else "above" if value > high else "inside",
                            "within_budget": value <= budget}
    return {"competition": slug, "plan": stage, "matcher_version": match["version"],
            "estimated_fit": plan["kaggle"]["fit"], "measurements": comparisons,
            "cpu_configuration": {"compute_threads": threads, "available_cores": effective_cores, "within_budget": cpu_fit},
            "fits_observed_budgets": cpu_fit and all(value["within_budget"] for value in comparisons.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path, default=HERE / "evidence" / "titanic.json")
    parser.add_argument("--gpu", type=Path, default=HERE / "evidence" / "digit-recognizer.json")
    args = parser.parse_args()
    try:
        result = [compare(json.loads(path.read_text(encoding="utf-8"))) for path in (args.cpu, args.gpu)]
        check([record["competition"] for record in result] == list(CONTRACTS), "expected one CPU and one GPU receipt")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if all(record["fits_observed_budgets"] for record in result) else 1


if __name__ == "__main__":
    raise SystemExit(main())
