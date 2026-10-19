"""Run one reproducible simplified BB84 simulation."""

import argparse
import logging

from qkd_pqc.config import load_config
from qkd_pqc.qkd.bb84_simulator import simulate_bb84, write_bb84_result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="YAML configuration path (relative to project root)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        config = load_config(args.config)
        result = simulate_bb84(config.qkd, seed=config.project.random_seed)
        output = write_bb84_result(result, config.output.raw_data_dir)
    except (OSError, ValueError) as exc:
        logging.error("BB84 stage failed: %s", exc)
        return 1
    print(f"BB84 run saved: {output}")
    print(
        f"received_signals={result.received_signals}, lost_signals={result.lost_signals}, "
        f"loss_fraction={result.loss_fraction:.6f}, sifted_bits={result.sifted_bits}, "
        f"error_bits={result.error_bits}, qber={result.qber}, "
        f"sifted_fraction={result.sifted_fraction:.6f}, "
        f"status={result.illustrative_status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
