"""Offline, rule-based Kaggle competition and workload triage."""

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


VERSION = "0.1.0"
HERE = Path(__file__).resolve().parent
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
MAX_TEXT = 32_000

SIGNALS = {
    "action": r"\b(?:actions?|polic(?:y|ies))\b|动作|策略",
    "agent": r"\bagents?\b|智能体",
    "environment": r"\b(?:game|simulator|simulation|environment|episodes?)\b|模拟器|仿真|环境|博弈",
    "classification": r"\b(?:classif\w+|predict whether|predict survival)\b|分类|预测类别",
    "regression": r"\b(?:regression|predict (?:sale |house sale )?prices|continuous target)\b|回归|预测房价",
    "forecasting": r"\b(?:forecast\w*|time series prediction|predict future)\b|时序预测|时间序列预测|预测未来",
    "clustering": r"\b(?:clustering|cluster (?:unlabell?ed|data|customers?)|customer segmentation)\b|聚类|无监督分群",
    "anomaly": r"\b(?:anomaly|outlier) detection\b|异常检测",
    "ranking": r"\b(?:learning to rank|ranked (?:results|products)|relevance labels|retriev\w+)\b|排序|检索",
    "segmentation": r"\b(?:image segmentation|semantic segmentation|pixel masks?)\b|图像分割|语义分割|像素掩码",
    "detection": r"\b(?:object detection|bounding boxes)\b|目标检测|边界框",
    "self_supervised": r"\b(?:self[- ]supervised|masked image modeling|masked language modeling)\b|自监督",
    "pretraining": r"\b(?:pre[- ]?train\w*|representations?)\b|预训练|表征学习",
    "unlabeled": r"\b(?:unlabell?ed (?:training\b|data\b)|no (?:training )?labels|unsupervised)\b|无标签|无监督",
    "labeled": r"\b(?:labell?ed(?:ness)?|ground truth|known targets?)\b|带标签|有标签|已标注",
    "tabular": r"\b(?:tabular|spreadsheet|structured rows|feature columns)\b|表格|结构化数据",
    "image": r"\b(?:images?|photos?|pixels?|x-rays?)\b|图像|图片",
    "text": r"\b(?:text|essays?|documents?|sentences?)\b|文本|作文|文档",
    "audio": r"\b(?:audio|speech|waveforms?)\b|音频|语音|鸟鸣",
}


@dataclass(frozen=True)
class Plan:
    method: str
    family: str
    cpu_cores: tuple[int, int]
    ram_gib: tuple[int, int]
    vram_gib: tuple[int, int]
    hours: tuple[float, float]


def cpu(method, ram=(2, 8), hours=(0.1, 1.0), *, family="classical-ml"):
    return Plan(method, family, (2, 4), ram, (0, 0), hours)


def gpu(method, vram=(8, 14), hours=(0.5, 4.0)):
    return Plan(method, "deep-learning", (2, 4), (8, 20), vram, hours)


# Task routes and model families are separate from how training signals are obtained.
ROUTES = {
    "classification": (cpu("Dummy majority then logistic regression on suitable features"),
                       None, "Stratify where valid; split by group or time when rows are dependent."),
    "tabular-classification": (cpu("Logistic regression with train-only preprocessing"),
                               cpu("CatBoost or LightGBM", (4, 16), (0.2, 3.0)),
                               "Stratify where valid; split by group or time when rows are dependent."),
    "regression": (cpu("Median target then ridge regression on suitable features"),
                   None, "Hold out unseen groups or later periods where applicable; use the official metric."),
    "tabular-regression": (cpu("Median target then ridge regression"),
                           cpu("CatBoost or LightGBM", (4, 16), (0.2, 3.0)),
                           "Fit transformations inside each fold; check the official target transformation."),
    "forecasting": (cpu("Seasonal naive forecast", family="reference"),
                    cpu("Lag features and gradient boosting", (6, 20), (0.3, 4.0)),
                    "Use rolling-origin validation; build each lag using only information available at prediction time."),
    "image-classification": (cpu("Logistic regression on downsampled images"),
                             gpu("Small CNN or transfer learning", (4, 10)),
                             "Split by source or subject where applicable; keep near duplicates in one split."),
    "image-segmentation": (cpu("Class prior or image thresholding on a small sample", family="reference"),
                           gpu("U-Net with resized inputs and a small batch", (8, 16), (1.0, 6.0)),
                           "Split by source image or subject; compute IoU/Dice only when relevant to the metric."),
    "object-detection": (cpu("Empty-box submission sanity check on a small sample", family="reference"),
                         gpu("Compact pretrained detector with a small batch", (8, 16), (1.0, 6.0)),
                         "Validate IoU and coordinate format on a held-out source/group split."),
    "text-classification": (cpu("Word/character TF-IDF and logistic regression", (4, 12)),
                            gpu("Compact encoder fine-tuning with capped sequence length"),
                            "Split by author, source or prompt where applicable; avoid duplicate leakage."),
    "audio-classification": (cpu("Spectral features and logistic regression", (4, 12)),
                             gpu("Mel-spectrogram CNN or compact audio encoder"),
                             "Split by recording/source rather than adjacent clips."),
    "multimodal-classification": (cpu("Separate per-modality baselines; compare against late fusion", (4, 12)),
                                  gpu("Compact encoders with frozen features or selective fine-tuning", (10, 18)),
                                  "Group paired examples together and report single-modality ablations."),
    "clustering": (cpu("Scaled features and mini-batch k-means"), cpu("Compare PCA + k-means and HDBSCAN", (4, 16)),
                   "Check cluster stability under resampling; use any supplied external metric separately."),
    "anomaly-detection": (cpu("Robust feature scores or Isolation Forest"), None,
                           "Confirm label availability and the false-positive budget before choosing a validation split."),
    "ranking": (cpu("Popularity or BM25 where query text is available", family="reference"),
                cpu("Learning-to-rank with labeled relevance", (6, 20), (0.3, 3.0)),
                "Hold out queries or time windows; evaluate against the official top-k metric."),
    "representation-learning": (cpu("PCA on suitable numeric features as a non-learning-objective reference"),
                                gpu("Small masked or contrastive encoder", (8, 16), (1.0, 6.0)),
                                "Keep downstream probes held out from pretraining and compare at a fixed feature budget."),
    "sequential-decision": (cpu("Rule-based agent; minimax for a suitable small board game", family="search-or-rules"),
                            cpu("Evaluate a small policy or self-play prototype only if RL adds value",
                                (4, 16), (0.5, 8.0), family="reinforcement-learning"),
                            "Freeze seeds and opponents; check action legality, timeouts and win rate."),
}

NOTEBOOKS = {
    "kaggle_cpu": {"cpu_cores": 4, "ram_gib": 24, "vram_gib": 0, "hours": 10},
    "kaggle_t4x2": {"cpu_cores": 4, "ram_gib": 24, "vram_gib": 14, "hours": 10},
}
PROFILE_SOURCES = ["https://www.kaggle.com/docs/notebooks", "https://www.kaggle.com/product-announcements/735239"]


def infer(description):
    # Explicitly excluded modalities should not turn a unimodal task into fusion.
    text = re.sub(r"\b(?:without|no) (?:any )?(?:images?|text|audio)\b|不含(?:图像|图片|文本|音频)", "", description.casefold())
    evidence = {key: match.group() for key, pattern in SIGNALS.items() if (match := re.search(pattern, text))}
    has = evidence.keys()
    modalities = [m for m in ("tabular", "image", "text", "audio") if m in has]
    predictive = {"classification", "regression", "segmentation", "detection"} & has
    task, learning = "unknown", "unknown"
    if {"agent", "action", "environment"} <= has:
        task, learning = "sequential-decision", "reinforcement-learning-optional"
    elif {"self_supervised", "pretraining"} <= has and not {"classification", "regression"} & has:
        task, learning = "representation-learning", "self-supervised"
    elif "clustering" in has and not {"classification", "detection", "regression", "forecasting"} & has:
        task, learning = "clustering", "unsupervised"
    elif "anomaly" in has:
        task = "anomaly-detection"
        if ("labeled" in has) != ("unlabeled" in has):
            learning = "supervised" if "labeled" in has else "unsupervised"
    elif "forecasting" in has:
        task, learning = "forecasting", "supervised"
    elif "segmentation" in has and "detection" not in has:
        task, learning = "image-segmentation", "supervised"
    elif "detection" in has and "segmentation" not in has:
        task, learning = "object-detection", "supervised"
    elif predictive in ({"classification"}, {"regression"}):
        classification = "classification" in has
        task = "classification" if classification else "regression"
        if classification and sum(m in has for m in ("image", "text", "audio")) > 1:
            task = "multimodal-classification"
        elif len(modalities) == 1 and (classification or modalities[0] == "tabular"):
            task = f"{modalities[0]}-{task}"
        learning = "supervised"
    elif "ranking" in has:
        task, learning = "ranking", "supervised" if "labeled" in has or "relevance labels" in text else "unknown"
    return task, learning, modalities, evidence


def competition_slug(ref):
    value = ref.strip().lower()
    if re.fullmatch(SLUG, value):
        return value
    parsed = urlsplit(value)
    match = re.fullmatch(rf"/(?:competitions|c)/({SLUG})(?:/[^\s]*)?", parsed.path)
    if parsed.scheme != "https" or parsed.netloc not in {"www.kaggle.com", "kaggle.com"} or not match:
        raise ValueError("expected a Kaggle competition slug or https://www.kaggle.com/competitions/<slug>")
    return match[1]


def estimate(plan, overrides, submission_hours):
    ranges = {name: getattr(plan, name) for name in NOTEBOOKS["kaggle_cpu"]}
    ranges.update({key: (value, value) for key, value in overrides.items()})
    profile = "kaggle_t4x2" if ranges["vram_gib"][1] > 0 else "kaggle_cpu"
    budget = NOTEBOOKS[profile]
    exceeds = [key for key, (low, _) in ranges.items() if low > budget[key]]
    near = [key for key, (_, high) in ranges.items() if high > budget[key]]
    fit = "above_planning_budget" if exceeds else "pilot_required" if near else "likely_for_pilot"
    return {
        "method": plan.method, "family": plan.family,
        "resources": {key: {"range": list(limits), "source": "user_input" if key in overrides else "heuristic"}
                      for key, limits in ranges.items()},
        "kaggle": {"profile": profile, "fit": fit, "planning_budget": budget.copy(),
                   "limiting_fields": exceeds or near},
        "submission_runtime": None if submission_hours is None else {
            "limit_hours": submission_hours,
            "estimate_relation": ("above" if ranges["hours"][0] > submission_hours else
                                  "overlaps" if ranges["hours"][1] > submission_hours else "within"),
        },
    }


def finite_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def match_competition(ref=None, description=None, *, overrides=None, plan="baseline", submission_hours=None):
    """Return a JSON-compatible result without reading data or calling Kaggle."""
    overrides = dict(overrides or {})
    if plan not in {"baseline", "next"}:
        raise ValueError("plan must be baseline or next")
    for field, value in overrides.items():
        if (field not in NOTEBOOKS["kaggle_cpu"] or not finite_number(value) or
                value < 0 or (value == 0 and field != "vram_gib") or
                (field == "cpu_cores" and int(value) != value)):
            raise ValueError(f"invalid resource override: {field}")
    if submission_hours is not None and (not finite_number(submission_hours) or submission_hours <= 0):
        raise ValueError("submission hours must be a finite positive number")
    if description is not None and (not description.strip() or len(description) > MAX_TEXT):
        raise ValueError(f"description must contain 1 to {MAX_TEXT} characters")
    slug = competition_slug(ref) if ref else None
    entry = json.loads((HERE / "catalog.json").read_text(encoding="utf-8")).get(slug) if slug else None
    if not entry and not description:
        raise ValueError("no offline profile for this competition; provide --description or --description-file"
                         if slug else "provide a competition slug, URL, or task description")

    if entry and not description:
        task, learning, modalities = entry["task"], entry["learning"], entry["modalities"]
        basis, evidence = "curated_snapshot", {"task_summary": entry["summary"]}
    else:
        task, learning, modalities, evidence = infer(description)
        basis = "description_rules"

    limit = submission_hours if submission_hours is not None else (entry or {}).get("submission_hours")
    plans = {}
    validation = None
    if task in ROUTES:
        baseline, next_plan, validation = ROUTES[task]
        if task == "anomaly-detection" and learning == "supervised":
            baseline = cpu("Class-weighted logistic regression on labeled anomalies")
            next_plan = cpu("Gradient boosting with precision/recall threshold selection", (4, 16))
        if task == "ranking" and learning == "unknown":
            next_plan = None
        plans = {name: estimate(route, overrides if plan == name else {}, limit)
                 for name, route in (("baseline", baseline), ("next", next_plan)) if route}
    if overrides and plan not in plans:
        raise ValueError(f"no {plan} workload is available for resource overrides")
    checks = ["Run a small pilot; measure peak RAM, per-device VRAM, disk and wall time before scaling.",
              "Check current account quota, accelerator availability, dataset/model permissions, internet and submission rules.",
              "T4x2 VRAM is per device, not one pooled allocation. Use explicit sharding if needed."]
    if task == "unknown" or learning == "unknown":
        checks.insert(0, "Clarify the target, training labels, evaluation metric or agent environment before committing to a method.")
    if entry and description and task != entry["task"]:
        checks.insert(0, "Pasted task differs from the curated task. Official metric and rule notes still refer to the curated competition.")
    return {
        "version": VERSION, "competition": slug, "basis": basis,
        "task": task, "learning": learning, "modalities": modalities, "evidence": evidence,
        "deep_learning_route": any(route["family"] == "deep-learning" for route in plans.values()),
        "metric": (entry or {}).get("metric"), "validation": validation, "plans": plans,
        "source": (entry or {}).get("source"), "submission_rules_note": (entry or {}).get("rules_note"),
        "submission_limit_source": ("user_input" if submission_hours is not None else "curated_snapshot")
        if limit is not None else None,
        "profile_sources": PROFILE_SOURCES.copy(), "checks": checks, "runtime_evidence": "UNMEASURED",
    }


def render(report):
    lines = [f"Kaggle Matcher v{report['version']} | {report['competition'] or 'task description'}",
             f"Task: {report['task']} | Learning: {report['learning']} | Evidence: {report['basis']}",
             f"Inputs: {', '.join(report['modalities']) or 'unknown'} | Deep-learning option: "
             f"{'yes' if report['deep_learning_route'] else 'not proposed'}"]
    if report["evidence"]:
        lines.append("Signals: " + "; ".join(f"{k}={v}" for k, v in report["evidence"].items()))
    if report["metric"]:
        lines.append(f"Competition metric: {report['metric']}")
    for name, plan in report["plans"].items():
        profile = plan["kaggle"]
        fields = ", ".join(f"{k}={v['range'][0]:g}-{v['range'][1]:g} ({v['source']})"
                           for k, v in plan["resources"].items())
        lines += [f"{name.title()}: {plan['method']} [{plan['family']}]", f"  {fields}",
                  f"  {profile['profile']}: {profile['fit']} (limits: {', '.join(profile['limiting_fields']) or 'none flagged'})"]
        if rule := plan["submission_runtime"]:
            lines.append(f"  If run during submission: estimate {rule['estimate_relation']} "
                         f"{rule['limit_hours']:g}h limit ({report['submission_limit_source']}).")
    for field, label in (("validation", "Validation"), ("submission_rules_note", "Rules snapshot"), ("source", "Official source")):
        if report[field]:
            lines.append(f"{label}: {report[field]}")
    lines.append(f"Actual resource use: {report['runtime_evidence']}")
    return "\n".join(lines + [f"- {check}" for check in report["checks"]])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("competition", nargs="?", help="Kaggle competition slug or URL")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--description", help="Competition task description (English or Chinese)")
    group.add_argument("--description-file", type=Path, help="Read a UTF-8 task description")
    parser.add_argument("--plan", choices=("baseline", "next"), default="baseline", help="Plan to apply overrides to")
    for field in NOTEBOOKS["kaggle_cpu"]:
        parser.add_argument("--" + field.replace("_", "-"), type=float, help=f"Override the selected plan's {field}")
    parser.add_argument("--submission-hours", type=float, help="Separate official submission runtime limit")
    parser.add_argument("--json", action="store_true", help="Emit structured output")
    parser.add_argument("--list", action="store_true", help="List offline competition profiles")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    overrides = {field: getattr(args, field) for field in NOTEBOOKS["kaggle_cpu"] if getattr(args, field) is not None}
    try:
        if args.list:
            if args.competition or args.description is not None or args.description_file or overrides or args.submission_hours is not None:
                parser.error("--list cannot be combined with a match request")
            profiles = json.loads((HERE / "catalog.json").read_text(encoding="utf-8"))
            print(json.dumps(sorted(profiles), indent=2) if args.json else "\n".join(sorted(profiles)))
            return 0
        description = args.description
        if args.description_file:
            with args.description_file.open(encoding="utf-8-sig") as handle:
                description = handle.read(MAX_TEXT + 1)
        report = match_competition(args.competition, description, overrides=overrides, plan=args.plan,
                                   submission_hours=args.submission_hours)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    # JSON escapes unicode by default; human output remains safe on legacy terminals.
    output = json.dumps(report, indent=2) if args.json else render(report)
    encoding = sys.stdout.encoding or "utf-8"
    print(output.encode(encoding, errors="backslashreplace").decode(encoding))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
