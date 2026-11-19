"""Measure two small Kaggle workloads; use only labeled training CSVs."""

from time import perf_counter, process_time

START, CPU_START = perf_counter(), process_time()

import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import threading


SEED = 42
THREADS = 2
GIB = 1024 ** 3


def input_file(root):
    candidates = [(slug, parent / slug / "train.csv")
                  for slug in ("titanic", "digit-recognizer")
                  for parent in (root / "competitions", root)]
    matches = [(slug, path) for slug, path in candidates if path.is_file()]
    if len(matches) != 1:
        raise RuntimeError("Mount exactly one official competition source with train.csv")
    return matches[0]


def sha256(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def t4_snapshot():
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=index,name,memory.total,memory.used", "--format=csv,noheader,nounits"],
        capture_output=True, text=True, check=True, timeout=3,
    )
    return {int(index): (name.strip(), int(total), int(used))
            for index, name, total, used in csv.reader(io.StringIO(result.stdout))}


class GPUSampler:
    def __init__(self):
        self.initial = t4_snapshot()
        self.peaks = {idx: card[2] for idx, card in self.initial.items()}
        self.samples = 1
        self.stop = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self.run, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def run(self):
        while not self.stop.wait(0.2):
            try:
                for idx, (_, _, used) in t4_snapshot().items():
                    self.peaks[idx] = max(self.peaks[idx], used)
                self.samples += 1
            except (OSError, KeyError, ValueError, subprocess.SubprocessError) as exc:
                self.error = type(exc).__name__
                return

    def __exit__(self, *_):
        self.stop.set()
        self.thread.join()

    def result(self):
        return [{"index": idx, "name": name, "total_mib": capacity,
                 "initial_used_mib": initial, "sampled_peak_used_mib": self.peaks[idx]}
                for idx, (name, capacity, initial) in self.initial.items()]


def titanic(path):
    import pandas as pd
    import sklearn
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    source = pd.read_csv(path)
    if len(source) != 891 or "Survived" not in source:
        raise RuntimeError("Expected the official 891-row Titanic training file")
    numeric = ["Age", "SibSp", "Parch", "Fare"]
    categorical = ["Pclass", "Sex", "Embarked"]
    x_train, x_valid, y_train, y_valid = train_test_split(
        source[numeric + categorical], source["Survived"],
        test_size=0.2, random_state=SEED, stratify=source["Survived"],
    )
    preprocess = ColumnTransformer([
        ("numeric", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
        ("categorical", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                      OneHotEncoder(handle_unknown="ignore")), categorical),
    ])
    model = make_pipeline(preprocess, LogisticRegression(max_iter=500))
    start = perf_counter()
    model.fit(x_train, y_train)
    fit_seconds = perf_counter() - start
    return {"method": "logistic-regression", "source_rows": len(source), "train_rows": len(x_train),
            "validation_rows": len(x_valid), "validation_accuracy": float(model.score(x_valid, y_valid)),
            "fit_seconds": fit_seconds, "gpu": None, "versions": {"pandas": pd.__version__, "scikit-learn": sklearn.__version__}}


def digit_recognizer(path):
    with GPUSampler() as sampler:
        import numpy as np
        import pandas as pd
        import sklearn
        from sklearn.model_selection import train_test_split
        import torch
        from torch import nn
        from torch.utils.data import DataLoader, TensorDataset

        if not torch.cuda.is_available() or not all("T4" in card[0] for card in sampler.initial.values()) or not sampler.initial:
            raise RuntimeError("This pilot must run on a CUDA-visible T4, never on CPU or paid hardware")
        torch.set_num_threads(THREADS)
        torch.manual_seed(SEED)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        device = torch.device("cuda:0")

        source = pd.read_csv(path, dtype=np.uint8)
        if source.shape != (42000, 785) or "label" not in source:
            raise RuntimeError("Expected the official 42000-row Digit Recognizer training file")
        targets = source.pop("label").to_numpy()
        pixels = source.to_numpy()
        train_idx, valid_idx = train_test_split(np.arange(len(source)), train_size=12000, test_size=3000,
                                                random_state=SEED, stratify=targets)

        def batches(indices, shuffle):
            data = TensorDataset(torch.from_numpy(pixels[indices]).reshape(-1, 1, 28, 28),
                                 torch.from_numpy(targets[indices]).long())
            return DataLoader(data, batch_size=128, shuffle=shuffle, num_workers=0,
                              generator=torch.Generator().manual_seed(SEED))

        train, valid = batches(train_idx, True), batches(valid_idx, False)
        model = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                              nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                              nn.Flatten(), nn.Linear(32 * 7 * 7, 10)).to(device)
        # Model transfer initializes the device; its live allocations remain in the baseline.
        torch.cuda.reset_peak_memory_stats(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        loss_fn = nn.CrossEntropyLoss()
        torch.cuda.synchronize(device)
        start = perf_counter()
        for _ in range(3):
            for x, y in train:
                optimizer.zero_grad(set_to_none=True)
                loss_fn(model(x.to(device, dtype=torch.float32) / 255), y.to(device)).backward()
                optimizer.step()
        torch.cuda.synchronize(device)
        fit_seconds = perf_counter() - start
        model.eval()
        correct = 0
        with torch.inference_mode():
            for x, y in valid:
                prediction = model(x.to(device, dtype=torch.float32) / 255).argmax(dim=1)
                correct += int((prediction == y.to(device)).sum().item())
        torch.cuda.synchronize(device)
        allocated = torch.cuda.max_memory_allocated(device)
        reserved = torch.cuda.max_memory_reserved(device)
        visible_count = torch.cuda.device_count()
        cuda_name = torch.cuda.get_device_name(device)
    if sampler.error or sampler.samples < 2:
        raise RuntimeError(f"No usable GPU sampling: samples={sampler.samples}, error={sampler.error}")
    return {"method": "small-cnn", "source_rows": len(source), "train_rows": len(train_idx),
            "validation_rows": len(valid_idx), "validation_accuracy": correct / len(valid_idx),
            "fit_seconds": fit_seconds, "epochs": 3, "batch_size": 128,
            "gpu": {"training_device": "cuda:0", "cuda_device_name": cuda_name, "cuda_visible_count": visible_count,
                    "torch_peak_allocated_bytes": allocated, "torch_peak_reserved_bytes": reserved,
                    "samples": sampler.samples, "sample_interval_seconds": 0.2, "cards": sampler.result()},
            "versions": {"numpy": np.__version__, "pandas": pd.__version__, "scikit-learn": sklearn.__version__,
                         "torch": str(torch.__version__), "cuda": torch.version.cuda}}


def read_optional(path):
    try:
        return Path(path).read_text(encoding="ascii").strip()
    except OSError:
        return None


def main():
    for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[key] = str(THREADS)
    slug, path = input_file(Path("/kaggle/input"))
    input_hash = sha256(path)
    result = (titanic if slug == "titanic" else digit_recognizer)(path)
    result.update({"schema": 1, "competition": slug, "seed": SEED, "input_sha256": input_hash,
                   "input_bytes": path.stat().st_size, "script_sha256": sha256(Path(__file__)),
                   "python": platform.python_version(), "threads": THREADS,
                   "affinity_cpus": len(os.sched_getaffinity(0)), "cgroup_cpu_max": read_optional("/sys/fs/cgroup/cpu.max"),
                   "cgroup_memory_max": read_optional("/sys/fs/cgroup/memory.max"),
                   "wall_seconds": perf_counter() - START, "cpu_seconds": process_time() - CPU_START,
                   "process_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024})
    output = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    Path("/kaggle/working/pilot-metrics.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
