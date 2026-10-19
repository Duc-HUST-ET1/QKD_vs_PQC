"""Reproducible multi-run BB84 sweeps for QKD analysis."""

from dataclasses import replace
import logging
from pathlib import Path

from qkd_pqc.config import ExperimentConfig
from qkd_pqc.qkd.bb84_simulator import simulate_bb84, write_bb84_result

logger = logging.getLogger(__name__)


def run_qkd_experiment(config: ExperimentConfig) -> list[Path]:
    """Run independent Eve, channel-noise, and channel-loss sweeps."""
    sweep = config.qkd_sweep
    scenarios: tuple[tuple[str, tuple[float, ...]], ...] = (
        ("eve_probability", sweep.eve_probabilities),
        ("channel_error_rate", sweep.channel_error_rates),
        ("channel_loss_rate", sweep.channel_loss_rates),
    )
    output_paths: list[Path] = []
    seen_settings: set[tuple[float, float, float]] = set()
    seed_offset = 0

    for parameter, values in scenarios:
        for value in values:
            settings = {
                "eve_probability": 0.0,
                "channel_error_rate": 0.0,
                "channel_loss_rate": 0.0,
            }
            settings[parameter] = value
            setting_key = (
                settings["eve_probability"],
                settings["channel_error_rate"],
                settings["channel_loss_rate"],
            )
            if setting_key in seen_settings:
                seed_offset += sweep.repetitions
                continue
            seen_settings.add(setting_key)

            run_config = replace(config.qkd, **settings)
            for repetition in range(sweep.repetitions):
                seed = config.project.random_seed + seed_offset + repetition
                result = simulate_bb84(run_config, seed=seed)
                output_paths.append(
                    write_bb84_result(result, config.output.raw_data_dir)
                )
            logger.info(
                "Completed %s=%s with %d repetitions.",
                parameter,
                value,
                sweep.repetitions,
            )
            seed_offset += sweep.repetitions

    return output_paths
