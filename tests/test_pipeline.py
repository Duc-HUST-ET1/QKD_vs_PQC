"""Integration tests for scripts/run_all.py and the shipped default configuration."""

import csv
from dataclasses import replace
import importlib.util

import pytest
import yaml

from qkd_pqc.config import OutputConfig, load_config
from qkd_pqc.paths import PROJECT_ROOT
from qkd_pqc.pqc.mlkem_benchmark import MLKEMUnavailableError


def _load_run_all():
    spec = importlib.util.spec_from_file_location("run_all", PROJECT_ROOT / "scripts" / "run_all.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def small_config(tmp_path):
    """A fast configuration whose outputs are redirected into tmp_path."""
    raw = {
        "project": {"name": "pipeline-test", "random_seed": 7},
        "qkd": {
            "n_signals": 200,
            "channel_error_rate": 0.01,
            "eve_probability": 0.0,
            "qber_threshold": 0.11,
            "channel_loss_rate": 0.0,
        },
        "qkd_sweep": {
            "repetitions": 2,
            "eve_probabilities": [0.0, 1.0],
            "channel_error_rates": [0.0, 0.1],
            "channel_loss_rates": [0.0, 0.5],
        },
        "pqc": {"algorithm": "ML-KEM-768", "warmup_iterations": 0, "measured_iterations": 3},
        "output": {
            "raw_data_dir": "data/raw",
            "processed_data_dir": "data/processed",
            "figures_dir": "figures",
        },
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.safe_dump(raw), encoding="utf-8")
    config = load_config(config_file)
    # Output paths must be relative in YAML; tests redirect the validated result instead.
    return replace(
        config,
        output=OutputConfig(
            raw_data_dir=tmp_path / "raw",
            processed_data_dir=tmp_path / "processed",
            figures_dir=tmp_path / "figures",
        ),
    )


@pytest.fixture
def run_all(monkeypatch, small_config):
    module = _load_run_all()
    monkeypatch.setattr(module, "load_config", lambda path=None: small_config)
    return module


def _mlkem_unavailable(*_args, **_kwargs):
    raise MLKEMUnavailableError("not installed in this test")


def _measured_valid_rows(processed_dir) -> int:
    tables = sorted(processed_dir.glob("comparison_*.csv"))
    assert len(tables) == 1
    with tables[0].open(encoding="utf-8", newline="") as stream:
        rows = {row["dimension"]: row for row in csv.DictReader(stream)}
    return int(rows["Measured QKD: valid_run_rows"]["qkd"])


def test_pipeline_completes_bb84_and_skips_missing_mlkem_honestly(run_all, monkeypatch,
                                                                  small_config, capsys):
    monkeypatch.setattr(run_all, "run_mlkem_benchmark", _mlkem_unavailable)

    assert run_all.main([]) == 0

    output = capsys.readouterr().out
    assert "BB84: completed" in output
    assert "BB84 sweep: skipped" in output
    assert "ML-KEM-768: skipped (verified implementation unavailable)" in output
    assert "Analysis: completed" in output
    assert len(list(small_config.output.raw_data_dir.glob("qkd_*.csv"))) == 1
    assert not list(small_config.output.raw_data_dir.glob("mlkem_*.csv"))


def test_pipeline_analyzes_only_csv_created_by_current_run(run_all, monkeypatch, small_config):
    monkeypatch.setattr(run_all, "run_mlkem_benchmark", _mlkem_unavailable)
    assert run_all.main([]) == 0
    first_run = sorted(small_config.output.raw_data_dir.glob("qkd_*.csv"))
    for table in small_config.output.processed_data_dir.glob("comparison_*.csv"):
        table.unlink()

    assert run_all.main([]) == 0

    # Two raw CSVs now exist, but the second analysis must only count its own run.
    assert len(list(small_config.output.raw_data_dir.glob("qkd_*.csv"))) == 2
    assert _measured_valid_rows(small_config.output.processed_data_dir) == 1
    assert first_run[0].exists()


def test_pipeline_never_overwrites_existing_raw_csv(run_all, monkeypatch, small_config):
    monkeypatch.setattr(run_all, "run_mlkem_benchmark", _mlkem_unavailable)
    assert run_all.main([]) == 0
    [existing] = small_config.output.raw_data_dir.glob("qkd_*.csv")
    original = existing.read_bytes()

    assert run_all.main([]) == 0

    assert existing.read_bytes() == original
    assert len(list(small_config.output.raw_data_dir.glob("qkd_*.csv"))) == 2


def test_pipeline_sweep_analyzes_exactly_the_sweep_cohort(run_all, monkeypatch, small_config,
                                                          capsys):
    monkeypatch.setattr(run_all, "run_mlkem_benchmark", _mlkem_unavailable)

    assert run_all.main(["--sweep"]) == 0

    # Baseline (0, 0, 0) is shared, so 2 Eve + 1 noise + 1 loss settings remain unique: 4 x 2 reps.
    expected_sweep_runs = 4 * small_config.qkd_sweep.repetitions
    assert f"BB84 sweep: completed ({expected_sweep_runs} run CSV files)" in capsys.readouterr().out
    assert len(list(small_config.output.raw_data_dir.glob("qkd_*.csv"))) == expected_sweep_runs + 1
    assert _measured_valid_rows(small_config.output.processed_data_dir) == expected_sweep_runs


def test_pipeline_reports_optional_mlkem_failure(run_all, monkeypatch, capsys):
    def broken_benchmark(*_args, **_kwargs):
        raise RuntimeError("shared secret mismatch")

    monkeypatch.setattr(run_all, "run_mlkem_benchmark", broken_benchmark)

    assert run_all.main([]) == 1
    assert "ML-KEM-768: failed (shared secret mismatch)" in capsys.readouterr().out


def test_pipeline_rejects_invalid_configuration(tmp_path):
    module = _load_run_all()
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("project: {name: x, random_seed: -1}\n", encoding="utf-8")

    assert module.main(["--config", str(invalid)]) == 1


def test_shipped_config_matches_documented_defaults():
    config = load_config()

    assert config.project.random_seed == 42
    assert config.qkd.n_signals == 100_000
    assert config.qkd.channel_error_rate == 0.01
    assert config.qkd.eve_probability == 0.0
    assert config.qkd.channel_loss_rate == 0.0
    assert config.qkd.qber_threshold == 0.11
    assert config.pqc.algorithm == "ML-KEM-768"
    assert (config.pqc.warmup_iterations, config.pqc.measured_iterations) == (50, 1000)
    for path in (config.output.raw_data_dir, config.output.processed_data_dir,
                 config.output.figures_dir):
        assert path.is_relative_to(PROJECT_ROOT)
