"""Run the required BB84 stage, optional ML-KEM benchmark, and available analysis."""

import argparse
import logging
import os
from pathlib import Path

# The pipeline only writes image files; a non-interactive backend avoids Tk/Tcl failures
# on headless or partially installed Python environments. An explicit MPLBACKEND wins.
os.environ.setdefault("MPLBACKEND", "Agg")

from qkd_pqc.analysis.plotting import create_plots  # noqa: E402
from qkd_pqc.config import load_config  # noqa: E402
from qkd_pqc.pqc.mlkem_benchmark import MLKEMUnavailableError, run_mlkem_benchmark  # noqa: E402
from qkd_pqc.qkd.bb84_simulator import simulate_bb84, write_bb84_result  # noqa: E402
from qkd_pqc.qkd.experiment import run_qkd_experiment  # noqa: E402


def _fail(statuses: list[str]) -> int:
    print("\n".join(statuses))
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="also run the repeated BB84 sweep from 'qkd_sweep' and analyze only its CSV files",
    )
    args = parser.parse_args(argv)
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
        return _fail(statuses)

    # Analysis uses exactly the CSV files created by this invocation, never a raw-directory scan.
    qkd_paths: list[Path] = [qkd_path]
    if args.sweep:
        try:
            sweep_paths = run_qkd_experiment(config)
            statuses.append(f"BB84 sweep: completed ({len(sweep_paths)} run CSV files)")
        except (OSError, ValueError) as exc:
            logging.error("Requested BB84 sweep failed: %s", exc)
            statuses.append(f"BB84 sweep: failed ({exc})")
            return _fail(statuses)
        # The sweep already contains the baseline settings; plot the sweep cohort by itself.
        qkd_paths = list(sweep_paths)
    else:
        statuses.append("BB84 sweep: skipped (use --sweep to run it)")

    # run_mlkem_benchmark() performs the capability self-test once and raises when unavailable.
    pqc_path = None
    try:
        benchmark = run_mlkem_benchmark(config.pqc, config.output.raw_data_dir)
        pqc_path = benchmark.output_path
        statuses.append(f"ML-KEM-768: completed ({pqc_path})")
    except MLKEMUnavailableError:
        statuses.append("ML-KEM-768: skipped (verified implementation unavailable)")
    except (OSError, ValueError, RuntimeError) as exc:
        logging.error("Optional ML-KEM-768 stage failed: %s", exc)
        statuses.append(f"ML-KEM-768: failed ({exc})")
        return _fail(statuses)

    try:
        figures = create_plots(
            qkd_csv=qkd_paths,
            pqc_csv=pqc_path,
            figures_dir=config.output.figures_dir,
            processed_dir=config.output.processed_data_dir,
        )
        statuses.append(f"Analysis: completed ({len(figures)} figure(s))")
    except (OSError, ValueError) as exc:
        logging.error("Analysis stage failed: %s", exc)
        statuses.append(f"Analysis: failed ({exc})")
        return _fail(statuses)

    print("\n".join(statuses))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
