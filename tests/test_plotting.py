import csv

import pytest

from qkd_pqc.analysis.plotting import create_plots


def _write_rows(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_plotting_rejects_missing_required_columns(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    _write_rows(qkd_file, ("qber",), [{"qber": "0.1"}])

    with pytest.raises(ValueError, match="missing required column"):
        create_plots(qkd_csv=qkd_file, figures_dir=tmp_path / "figures")


def test_plotting_skips_invalid_measurement_rows(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    _write_rows(
        qkd_file,
        ("qber", "eve_probability", "channel_error_rate", "sifted_fraction"),
        [{
            "qber": "",
            "eve_probability": "invalid",
            "channel_error_rate": "1.2",
            "sifted_fraction": "1.2",
        }],
    )

    figures = create_plots(
        qkd_csv=qkd_file,
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    assert figures == []
    assert not list((tmp_path / "figures").glob("*.png"))
    assert len(list((tmp_path / "processed").glob("*.csv"))) == 1


def test_plotting_creates_only_data_supported_figures(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    _write_rows(
        qkd_file,
        (
            "qber",
            "eve_probability",
            "channel_error_rate",
            "channel_loss_rate",
            "sifted_fraction",
        ),
        [
            {
                "qber": "0.08",
                "eve_probability": "0.2",
                "channel_error_rate": "0.0",
                "channel_loss_rate": "0.0",
                "sifted_fraction": "0.5",
            },
            {
                "qber": "0.01",
                "eve_probability": "0.0",
                "channel_error_rate": "0.01",
                "channel_loss_rate": "0.0",
                "sifted_fraction": "0.5",
            },
            {
                "qber": "0.0",
                "eve_probability": "0.0",
                "channel_error_rate": "0.0",
                "channel_loss_rate": "0.2",
                "sifted_fraction": "0.4",
            },
        ],
    )

    figures = create_plots(
        qkd_csv=qkd_file,
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    assert {path.name for path in figures} == {
        "qber_vs_eve_probability.png",
        "qber_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_loss_rate.png",
    }
    assert all(path.is_file() for path in figures)


def test_plotting_does_not_count_duplicate_seeded_runs_as_repetitions(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    fields = (
        "run_id",
        "seed",
        "n_signals",
        "channel_error_rate",
        "eve_probability",
        "qber_threshold",
        "channel_loss_rate",
        "simulator_version",
        "qber",
        "sifted_fraction",
    )
    row = {
        "seed": "42",
        "n_signals": "100",
        "channel_error_rate": "0",
        "eve_probability": "0",
        "qber_threshold": "0.11",
        "channel_loss_rate": "0",
        "simulator_version": "0.1.0",
        "qber": "0",
        "sifted_fraction": "0.5",
    }
    _write_rows(
        qkd_file,
        fields,
        [{**row, "run_id": "first"}, {**row, "run_id": "duplicate"}],
    )

    create_plots(
        qkd_csv=qkd_file,
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    with next((tmp_path / "processed").glob("*.csv")).open(
        newline="", encoding="utf-8"
    ) as stream:
        measured_rows = list(csv.DictReader(stream))
    assert {
        row["qkd"] for row in measured_rows
        if row["dimension"] == "Measured QKD: valid_run_rows"
    } == {"1"}


def test_plotting_omits_averages_across_mixed_qkd_settings(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    fields = (
        "run_id",
        "seed",
        "n_signals",
        "channel_error_rate",
        "eve_probability",
        "qber_threshold",
        "channel_loss_rate",
        "simulator_version",
        "qber",
        "sifted_fraction",
    )
    rows = [
        {
            "run_id": "baseline",
            "seed": "1",
            "n_signals": "100",
            "channel_error_rate": "0",
            "eve_probability": "0",
            "qber_threshold": "0.11",
            "channel_loss_rate": "0",
            "simulator_version": "0.1.0",
            "qber": "0",
            "sifted_fraction": "0.5",
        },
        {
            "run_id": "eve",
            "seed": "2",
            "n_signals": "100",
            "channel_error_rate": "0",
            "eve_probability": "0.5",
            "qber_threshold": "0.11",
            "channel_loss_rate": "0",
            "simulator_version": "0.1.0",
            "qber": "0.12",
            "sifted_fraction": "0.5",
        },
    ]
    _write_rows(qkd_file, fields, rows)

    create_plots(
        qkd_csv=qkd_file,
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    with next((tmp_path / "processed").glob("*.csv")).open(
        newline="", encoding="utf-8"
    ) as stream:
        dimensions = {
            row["dimension"]: row["qkd"] for row in csv.DictReader(stream)
        }
    assert "Measured QKD: mean_qber" not in dimensions
    assert dimensions["Measured QKD: measurement_scope"] == (
        "multiple_settings; consult per-setting plots"
    )
    assert dimensions["Measured QKD: setting_count"] == "2"
