import yaml
import pytest

from qkd_pqc.config import ConfigurationError, load_config


def _valid_config():
    return {
        "project": {"name": "test", "random_seed": 1},
        "qkd": {
            "n_signals": 10,
            "channel_error_rate": 0.01,
            "eve_probability": 0.0,
            "qber_threshold": 0.11,
        },
        "qkd_sweep": {
            "repetitions": 2,
            "eve_probabilities": [0.0, 1.0],
            "channel_error_rates": [0.0, 0.1],
            "channel_loss_rates": [0.0, 1.0],
        },
        "pqc": {
            "algorithm": "ML-KEM-768",
            "warmup_iterations": 0,
            "measured_iterations": 1,
        },
        "output": {
            "raw_data_dir": "data/raw",
            "processed_data_dir": "data/processed",
            "figures_dir": "figures",
        },
    }


@pytest.mark.parametrize(
    ("section", "key", "value", "error_match"),
    [
        ("qkd", "channel_error_rate", 1.1, "channel_error_rate"),
        ("qkd", "channel_loss_rate", -0.1, "channel_loss_rate"),
        ("qkd", "channel_error_rate", float("nan"), "channel_error_rate"),
        ("qkd", "n_signals", 0, "n_signals"),
        ("qkd_sweep", "repetitions", 0, "repetitions"),
        ("qkd_sweep", "eve_probabilities", [], "non-empty"),
        ("pqc", "measured_iterations", 0, "measured_iterations"),
        ("pqc", "algorithm", "Kyber768", "ML-KEM-768"),
    ],
)
def test_invalid_configuration_values_are_rejected(
    tmp_path, section, key, value, error_match
):
    config = _valid_config()
    config[section][key] = value
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    with pytest.raises(ConfigurationError, match=error_match):
        load_config(config_path)


def test_default_configuration_loads():
    config = load_config()

    assert config.project.random_seed == 42
    assert config.qkd.n_signals == 100000
    assert config.qkd.channel_loss_rate == 0.0
    assert config.qkd_sweep.repetitions == 10
    assert config.pqc.algorithm == "ML-KEM-768"
    assert config.pqc.measured_iterations > 0
