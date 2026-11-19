"""Prepare two private, offline Kaggle script packages without pushing them."""

import argparse
import json
from pathlib import Path
import re
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--suffix", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9_-]{1,40}", args.owner) or not re.fullmatch(r"[a-z0-9-]{1,12}", args.suffix):
        parser.error("invalid Kaggle account or run suffix")
    args.out.mkdir(parents=True, exist_ok=False)
    for kind, competition, gpu, title in (
        ("cpu", "titanic", False, "PML Titanic CPU Pilot"),
        ("gpu", "digit-recognizer", True, "PML Digit Recognizer GPU Pilot"),
    ):
        folder = args.out / kind
        folder.mkdir()
        kernel = f"{args.owner}/{title.lower().replace(' ', '-')}-{args.suffix}"
        meta = {"id": kernel, "title": f"{title} {args.suffix}", "code_file": "pilot.py",
                "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": gpu,
                "enable_tpu": False, "enable_internet": False, "dataset_sources": [],
                "competition_sources": [competition], "kernel_sources": [], "model_sources": []}
        (folder / "kernel-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        shutil.copyfile(Path(__file__).with_name("pilot.py"), folder / "pilot.py")
        print(kernel)


if __name__ == "__main__":
    main()
