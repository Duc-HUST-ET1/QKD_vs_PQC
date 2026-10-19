import csv

from qkd_pqc.config import (
    ExperimentConfig,
    OutputConfig,
    PQCConfig,
    ProjectConfig,
    QKDConfig,
    QKDSweepConfig,
)
from qkd_pqc.qkd.experiment import run_qkd_experiment


def test_experiment_runner_writes_reproducible_sweep_runs(tmp_path):
    config = ExperimentConfig(
        project=ProjectConfig(name="test", random_seed=123),
        qkd=QKDConfig(100, 0.01, 0.0, 0.11),
        pqc=PQCConfig("ML-KEM-768", 0, 1),
        output=OutputConfig(tmp_path / "raw", tmp_path / "processed", tmp_path / "figures"),
        qkd_sweep=QKDSweepConfig(
            repetitions=2,
            eve_probabilities=(0.0, 1.0),
            channel_error_rates=(0.0, 0.1),
            channel_loss_rates=(0.0, 1.0),
        ),
    )

    paths = run_qkd_experiment(config)
    rows = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as stream:
            rows.extend(csv.DictReader(stream))

    assert len(paths) == 8
    assert len(rows) == 8
    assert len({row["seed"] for row in rows}) == 8
    assert {float(row["eve_probability"]) for row in rows} == {0.0, 1.0}
    assert {float(row["channel_error_rate"]) for row in rows} == {0.0, 0.1}
    assert {float(row["channel_loss_rate"]) for row in rows} == {0.0, 1.0}
