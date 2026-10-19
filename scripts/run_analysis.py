"""Generate plots and comparison tables from existing experiment CSV files."""

import argparse
import logging

from qkd_pqc.analysis.plotting import create_plots
from qkd_pqc.config import load_config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    parser.add_argument(
        "--qkd-run-prefix",
        help="only analyze QKD CSV files whose run_id starts with this prefix",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        config = load_config(args.config)
        raw_dir = config.output.raw_data_dir
        qkd_files = sorted(raw_dir.glob("qkd_*.csv"))
        if args.qkd_run_prefix:
            qkd_files = [
                path for path in qkd_files
                if path.stem.startswith(args.qkd_run_prefix)
            ]
        pqc_files = sorted(raw_dir.glob("mlkem_*.csv"))
        if not qkd_files and not pqc_files:
            print(f"No experiment CSV files found in {raw_dir}; analysis skipped.")
            return 0
        figures = create_plots(
            qkd_csv=qkd_files or None,
            pqc_csv=pqc_files or None,
            figures_dir=config.output.figures_dir,
            processed_dir=config.output.processed_data_dir,
        )
    except (OSError, ValueError) as exc:
        logging.error("Analysis failed: %s", exc)
        return 1
    if figures:
        for path in figures:
            print(f"Figure saved: {path}")
    else:
        print("No figures were created; see warnings for unavailable/invalid measurements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
