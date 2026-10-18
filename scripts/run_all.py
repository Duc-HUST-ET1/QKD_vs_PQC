"""Run the required BB84 stage, optional ML-KEM benchmark, and available analysis."""

import argparse
import logging

from qkd_pqc.analysis.plotting import create_plots
from qkd_pqc.config import load_config
from qkd_pqc.pqc.mlkem_benchmark import (
    MLKEMUnavailableError,
    detect_mlkem_implementation,
    run_mlkem_benchmark,
)
from qkd_pqc.qkd.bb84_simulator import simulate_bb84, write_bb84_result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        config = load_config(args.config)
    except (OSError, ValueError) as exc:
        logging.error("Configuration failed: %s", exc)
        return 1

    statuses: list[str] = []
    try:
        qkd_result = simulate_bb84(config.qkd, seed=config.project.random_seed)
        qkd_path = write_bb84_result(qkd_result, config.output.raw_data_dir)
        statuses.append(f"BB84: completed ({qkd_path})")
    except (OSError, ValueError) as exc:
        logging.error("Required BB84 stage failed: %s", exc)
        statuses.append(f"BB84: failed ({exc})")
        print("\n".join(statuses))
        return 1

    pqc_path = None
    if detect_mlkem_implementation() is None:
        statuses.append("ML-KEM-768: skipped (verified implementation unavailable)")
    else:
        try:
            benchmark = run_mlkem_benchmark(config.pqc, config.output.raw_data_dir)
            pqc_path = benchmark.output_path
            statuses.append(f"ML-KEM-768: completed ({pqc_path})")
        except MLKEMUnavailableError as exc:
            statuses.append(f"ML-KEM-768: skipped ({exc})")
        except (OSError, ValueError, RuntimeError) as exc:
            logging.error("Optional ML-KEM-768 stage failed: %s", exc)
            statuses.append(f"ML-KEM-768: failed ({exc})")
            print("\n".join(statuses))
            return 1

    try:
        figures = create_plots(
            qkd_csv=qkd_path,
            pqc_csv=pqc_path,
            figures_dir=config.output.figures_dir,
            processed_dir=config.output.processed_data_dir,
        )
        statuses.append(f"Analysis: completed ({len(figures)} figure(s))")
    except (OSError, ValueError) as exc:
        logging.error("Analysis stage failed: %s", exc)
        statuses.append(f"Analysis: failed ({exc})")
        print("\n".join(statuses))
        return 1

    print("\n".join(statuses))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
