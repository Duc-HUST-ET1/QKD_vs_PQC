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
        ("qber", "eve_probability", "channel_error_rate", "sifted_fraction"),
        [{
            "qber": "0.08",
            "eve_probability": "0.2",
            "channel_error_rate": "0.01",
            "sifted_fraction": "0.5",
        }],
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
    }
    assert all(path.is_file() for path in figures)
