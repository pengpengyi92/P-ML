"""Read public GitHub sources and render a bounded, version-pinned ML catalog."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "ml-repo" / "ecosystem"
CATEGORIES = {
    "foundations": ("数值与数据底座", "engineering"),
    "frameworks": ("深度学习框架", "engineering"),
    "supervised": ("监督学习与表格模型", "learning-paradigm"),
    "unsupervised": ("无监督、聚类、降维与检索", "learning-paradigm"),
    "self-semi-supervised": ("自监督与半监督学习", "learning-paradigm"),
    "transformers-llm": ("Transformer、NLP 与 LLM 工具链", "application-and-tooling"),
    "vision": ("计算机视觉", "application-domain"),
    "audio": ("音频与语音", "application-domain"),
    "generative": ("生成与扩散模型", "model-family"),
    "reinforcement": ("强化学习与环境", "learning-paradigm"),
    "probabilistic": ("概率建模、贝叶斯与统计", "method-family"),
    "time-series": ("时间序列与在线学习", "application-domain"),
    "graph": ("图机器学习", "application-domain"),
    "evaluation": ("调参、评估、解释与实验管理", "engineering"),
    "deployment": ("模型交换、推理与服务", "engineering"),
}


def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def configure_catalog(directory):
    global DEST, CATEGORIES
    directory = directory.resolve()
    if not directory.is_relative_to((ROOT / "ml-repo").resolve()) or directory == (ROOT / "ml-repo").resolve():
        raise ValueError("Catalog must be a child of this project's ml-repo/")
    taxonomy = json.loads((directory / "taxonomy.json").read_text(encoding="utf-8"))
    if not isinstance(taxonomy, dict) or not taxonomy:
        raise ValueError("A nonempty taxonomy is required")
    for key, value in taxonomy.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", key) or not isinstance(value, list) or len(value) != 2 or not all(isinstance(x, str) and x.strip() for x in value):
            raise ValueError("Invalid taxonomy key/title/dimension")
    DEST = directory
    CATEGORIES = {key: tuple(value) for key, value in taxonomy.items()}


def validate_selection(data):
    seen = set()
    if data.get("complete_ecosystem_inventory") is not False:
        raise ValueError("This selection cannot claim global completeness")
    for row in data["entries"]:
        name = row["repository"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name):
            raise ValueError("Invalid repository identifier")
        if name.casefold() in seen:
            raise ValueError("Duplicate repository")
        seen.add(name.casefold())
        if not row["categories"] or not set(row["categories"]) <= CATEGORIES.keys():
            raise ValueError("Invalid categories")
        if not row["use"] or not row["boundary"]:
            raise ValueError("Missing actionable use/boundary")


def query_github(query, cache_dir, resume=False):
    cache = cache_dir / (hashlib.sha256(query.encode()).hexdigest() + ".json")
    if resume and cache.exists():
        record = json.loads(cache.read_text(encoding="utf-8"))
        if record["query_sha256"] != hashlib.sha256(query.encode()).hexdigest():
            raise ValueError("Cache key mismatch")
        return record
    for attempt in range(2):
        try:
            result = subprocess.run(
                ["gh", "api", "graphql", "--input", "-"],
                input=json.dumps({"query": query}), capture_output=True,
                text=True, encoding="utf-8", timeout=75,
            )
        except subprocess.TimeoutExpired:
            result = None
        if result is not None and result.returncode == 0:
            body = json.loads(result.stdout)
            if body.get("errors"):
                raise RuntimeError("GraphQL source lookup returned errors: " + json.dumps(body["errors"]))
            record = {"observed_at": now(), "query_sha256": hashlib.sha256(query.encode()).hexdigest(), "data": body["data"]}
            cache.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            return record
        if attempt == 0:
            time.sleep(1)
    raise RuntimeError("Public GitHub query failed; no absence or permission inferred")


def source_blob(repo, head, path, blob, expected_oid):
    if not blob or blob.get("isBinary") or blob.get("text") is None:
        raise ValueError("Missing/non-text source: " + repo + "/" + path)
    data = blob["text"].encode("utf-8")
    actual_oid = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if actual_oid != expected_oid or blob["oid"] != expected_oid or len(data) != blob["byteSize"]:
        raise ValueError("Source byte/Git blob integrity mismatch: " + repo + "/" + path)
    return {"path": path, "blob_sha": actual_oid, "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data), "url": f"https://github.com/{repo}/blob/{head}/{quote(path, safe='/')}"}


def license_class(signal):
    if signal in {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0"}:
        return "permissive-signal-review-text"
    if signal and signal.startswith(("AGPL-", "GPL-", "LGPL-", "MPL-", "EPL-")):
        return "reciprocal-signal-review-text"
    return "needs-license-review"


def collect(review_dir, resume=False):
    review_dir = review_dir.resolve()
    if not review_dir.is_relative_to((ROOT / ".local").resolve()):
        raise ValueError("Raw GitHub sources/cache must stay under this checkout's ignored .local/")
    selection = json.loads((DEST / "selection.json").read_text(encoding="utf-8"))
    validate_selection(selection)
    review_dir.mkdir(parents=True, exist_ok=True)
    cache = review_dir / "cache"
    cache.mkdir(exist_ok=True)
    entries = selection["entries"]
    snapshot = {"schema_version": 1, "title": selection["title"], "started_at": now(),
                "timezone": "Asia/Shanghai", "complete_ecosystem_inventory": False,
                "source_policy": "Public primary metadata and byte-verified pinned README/license only; no upstream code/data mirror or execution",
                "resume": resume, "entries": []}
    canonical = set()
    for offset in range(0, len(entries), 8):
        group = entries[offset:offset + 8]
        fields = []
        for i, row in enumerate(group):
            owner, name = row["repository"].split("/")
            fields.append(f'r{i}:repository(owner:{json.dumps(owner)},name:{json.dumps(name)})' +
                          '{nameWithOwner url isPrivate isArchived isFork description pushedAt licenseInfo{spdxId name}' +
                          'defaultBranchRef{name target{oid ... on Commit{tree{entries{name oid type}}}}}}')
        metadata = query_github("query{" + " ".join(fields) + "}", cache, resume)
        pending, source_fields = [], []
        for i, row in enumerate(group):
            info = metadata["data"][f"r{i}"]
            if not info or info["isPrivate"] or info["isFork"] or not info["defaultBranchRef"]:
                raise ValueError("Public primary nonempty repository required: " + row["repository"])
            repo = info["nameWithOwner"]
            if repo.casefold() in canonical:
                raise ValueError("Redirect introduced a canonical duplicate")
            canonical.add(repo.casefold())
            target = info["defaultBranchRef"]["target"]
            head, tree = target["oid"], target["tree"]["entries"]
            roots = {x["name"].casefold(): x for x in tree if x["type"] == "blob"}
            readme = next((roots[x] for x in ("readme.md", "readme.rst", "readme", "readme.markdown") if x in roots), None)
            license_file = next((roots[x] for x in ("license", "license.txt", "license.md", "licence", "licence.txt", "copying", "copying.txt", "license.rst") if x in roots), None)
            if not readme:
                raise ValueError("No root README; inspect explicitly: " + repo)
            specs = [("readme", readme)]
            if license_file:
                specs.append(("license", license_file))
            for index, path in enumerate(row.get("additional_root_sources", [])):
                if not isinstance(path, str) or "/" in path or "\\" in path or path.casefold() not in roots:
                    raise ValueError("Additional source must be an observed root file: " + str(path))
                specs.append((f"additional{index}", roots[path.casefold()]))
            pending.append((row, info, head, specs, license_file))
            owner, name = repo.split("/")
            expressions = []
            for label, source in specs:
                if source:
                    expressions.append(label + ':object(expression:' + json.dumps(head + ":" + source["name"]) + '){... on Blob{oid byteSize text isBinary}}')
            source_fields.append(f'r{i}:repository(owner:{json.dumps(owner)},name:{json.dumps(name)})' + "{" + " ".join(expressions) + "}")
        sources = query_github("query{" + " ".join(source_fields) + "}", cache, resume)
        for i, (row, info, head, specs, license_file) in enumerate(pending):
            repo = info["nameWithOwner"]
            record = sources["data"][f"r{i}"]
            pins = []
            for label, source in specs:
                if source:
                    pins.append({"kind": label, **source_blob(repo, head, source["name"], record[label], source["oid"])})
                    (review_dir / (repo.replace("/", "__") + "__" + label + ".txt")).write_text(record[label]["text"], encoding="utf-8")
            signal = (info["licenseInfo"] or {}).get("spdxId")
            snapshot["entries"].append({**row, "requested_repository": row["repository"], "repository": repo,
                "url": info["url"], "private": info["isPrivate"], "fork": info["isFork"],
                "archived": info["isArchived"], "description": info["description"],
                "default_branch": info["defaultBranchRef"]["name"], "head": head, "pushed_at": info["pushedAt"],
                "metadata_observed_at": metadata["observed_at"], "sources_observed_at": sources["observed_at"],
                "license_signal": signal, "license_class": license_class(signal) if license_file else "needs-license-review",
                "sources": pins, "runtime_evaluation": "NOT_RUN", "quality_gain": "UNMEASURED"})
            print(f"PINNED {repo} | {signal} | archived={info['isArchived']}", flush=True)
    snapshot["completed_at"] = now()
    (DEST / "snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"COLLECTED {len(snapshot['entries'])} public primary repositories", flush=True)


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render():
    data = json.loads((DEST / "snapshot.json").read_text(encoding="utf-8"))
    rows = data["entries"]
    for category, (title, dimension) in CATEGORIES.items():
        chosen = [row for row in rows if category in row["categories"]]
        lines = [f"# {title}", "", f"**Dimension:** `{dimension}`. **Selected:** {len(chosen)}; multi-label, not additive.",
                 f"**Snapshot completed:** `{data['completed_at']}`; each API observation keeps its own timestamp.",
                 "", "Public-source reading candidates; third-party runtime **NOT_RUN**, quality/cost gains **UNMEASURED**.",
                 "Code, data, weights, hosted products and dependencies have separate terms. No installation recommendation or official partnership is implied.",
                 "", "[总目录](README.md) · [实验与防泄漏协议](EXPERIMENT_PROTOCOL.md) · [来源快照](snapshot.json)", "",
                 "| Repository / current owner | 学什么、从哪里开始 | 许可识别与维护状态 | 使用边界 |", "| --- | --- | --- | --- |"]
        for row in chosen:
            readme = next(x for x in row["sources"] if x["kind"] == "readme")
            license_file = next((x for x in row["sources"] if x["kind"] == "license"), None)
            rights = f"[{row['license_signal'] or 'unclassified'}]({license_file['url']})" if license_file else "NO ROOT LICENSE: NEEDS_PERMISSION"
            if row["license_class"] != "permissive-signal-review-text":
                rights += " / " + row["license_class"]
            if row.get("source_review_note"):
                rights += " / " + cell(row["source_review_note"])
            if row["reuse_policy"] == "restricted-noncommercial-reference":
                rights += " / REFERENCE ONLY: NONCOMMERCIAL"
            if row["reuse_policy"] == "reference-only-license-clarification":
                rights += " / REFERENCE ONLY: CLARIFY LICENSE"
            for extra in row["sources"]:
                if extra["kind"].startswith("additional"):
                    rights += f" / [{extra['path']}]({extra['url']})"
            state = "ARCHIVED" if row["archived"] else "not archived (not a support promise)"
            use = cell(row["use"])
            if row.get("role"):
                use = f"`{cell(row['role'])}` · " + use
            lines.append(f"| [{row['repository']}]({row['url']}) | {use}；[固定 README]({readme['url']})；[版本树]({row['url']}/tree/{row['head']}) | {rights}; {state} | {cell(row['boundary'])} |")
        (DEST / (category + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    counts = {key: sum(key in row["categories"] for row in rows) for key in CATEGORIES}
    print(json.dumps({"unique": len(rows), "categories_nonadditive": counts,
                      "archived": [row["repository"] for row in rows if row["archived"]],
                      "license_review": [row["repository"] for row in rows if row["license_class"] == "needs-license-review"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--catalog-dir", type=Path, help="Additive catalog below ml-repo/, with its own taxonomy.json")
    parser.add_argument("--review-dir", type=Path, default=ROOT / ".local" / "ml-source-review")
    args = parser.parse_args()
    if not args.collect and not args.render:
        parser.error("Choose --collect and/or --render")
    if args.catalog_dir:
        configure_catalog(ROOT / args.catalog_dir)
    if args.collect:
        collect(args.review_dir, args.resume)
    if args.render:
        render()
