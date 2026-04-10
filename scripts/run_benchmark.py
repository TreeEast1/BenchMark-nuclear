#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nusafety.config import load_config
from nusafety.data import load_cases
from nusafety.runner import EvaluationRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the NuSafety multi-turn benchmark scaffold.")
    parser.add_argument("--config", type=Path, required=True, help="YAML configuration file.")
    parser.add_argument("--cases", type=Path, required=True, help="JSONL scenario cases.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for transcripts and scores.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    cases = load_cases(args.cases)
    runner = EvaluationRunner(config=config, output_dir=args.output_dir)
    summary = runner.run(cases)
    print(f"Completed {summary['scenario_count']} scenario(s). Mean NSC: {summary['mean_nsc']:.2f}")


if __name__ == "__main__":
    main()
