"""Compare description routing against a fixed task-only keyword baseline."""

import json

from matcher import HERE, match_competition


KEYWORDS = (
    ("classification", "classification"), ("regression", "regression"),
    ("forecast", "forecasting"), ("cluster", "clustering"),
    ("anomaly", "anomaly-detection"), ("reward", "sequential-decision"),
    ("image", "image-classification"), ("text", "text-classification"),
    ("retrieve", "ranking"),
)


def baseline(description):
    lower = description.casefold()
    return next((task for keyword, task in KEYWORDS if keyword in lower), "unknown")


def evaluate():
    cases = json.loads((HERE / "eval_cases.json").read_text(encoding="utf-8"))
    baseline_misses, matcher_misses, learning_misses = [], [], []
    for case in cases:
        observed = match_competition(description=case["text"])
        if baseline(case["text"]) != case["task"]:
            baseline_misses.append(case["id"])
        if observed["task"] != case["task"]:
            matcher_misses.append(case["id"])
        if observed["learning"] != case["learning"]:
            learning_misses.append(case["id"])
    return {
        "cases": len(cases), "baseline_task_correct": len(cases) - len(baseline_misses),
        "matcher_task_correct": len(cases) - len(matcher_misses),
        "matcher_learning_correct": len(cases) - len(learning_misses),
        "baseline_task_misses": baseline_misses, "matcher_task_misses": matcher_misses,
        "matcher_learning_misses": learning_misses,
    }


if __name__ == "__main__":
    result = evaluate()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["matcher_task_misses"] or result["matcher_learning_misses"]))
