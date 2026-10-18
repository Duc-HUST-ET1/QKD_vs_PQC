"""Run the optional verified ML-KEM-768 benchmark."""

import argparse
import logging

from qkd_pqc.config import load_config
from qkd_pqc.pqc.mlkem_benchmark import MLKEMUnavailableError, run_mlkem_benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        config = load_config(args.config)
        results = run_mlkem_benchmark(config.pqc, config.output.raw_data_dir)
    except MLKEMUnavailableError as exc:
        logging.error("%s", exc)
        return 2
    except (OSError, ValueError, RuntimeError) as exc:
        logging.error("ML-KEM-768 benchmark failed: %s", exc)
        return 1
    print(
        f"ML-KEM-768 benchmark saved: {results.output_path} "
        f"({results.measured_iterations} samples per operation)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
