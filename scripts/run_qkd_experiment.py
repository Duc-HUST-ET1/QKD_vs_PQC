"""Run repeated BB84 sweeps for Eve, channel noise, and channel loss."""

import argparse
import logging
import os

from qkd_pqc.config import load_config
from qkd_pqc.qkd.experiment import run_qkd_experiment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        config = load_config(args.config)
        outputs = run_qkd_experiment(config)
    except (OSError, ValueError) as exc:
        logging.error("BB84 experiment failed: %s", exc)
        return 1
    print(f"BB84 experiment saved {len(outputs)} run CSV files.")
    if outputs:
        run_prefix = os.path.commonprefix([path.stem for path in outputs])
        print(f"Run-ID prefix for analysis: {run_prefix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
