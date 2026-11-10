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

    figures_dir = tmp_path / "figures"
    figures_dir.mkdir()
    stale_names = (
        "qber_vs_eve_probability.png",
        "qber_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_loss_rate.png",
        "mlkem_latency_cdf.png",
    )
    for name in stale_names:
        (figures_dir / name).write_bytes(b"stale output")

    figures = create_plots(
        qkd_csv=qkd_file,
        figures_dir=figures_dir,
        processed_dir=tmp_path / "processed",
    )

    assert figures == []
    assert not list(figures_dir.glob("*.png"))
    assert len(list((tmp_path / "processed").glob("*.csv"))) == 1


def test_plotting_creates_only_data_supported_figures(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    figures_dir = tmp_path / "figures"
    figures_dir.mkdir()
    stale_mlkem_figure = figures_dir / "mlkem_latency_cdf.png"
    stale_mlkem_figure.write_bytes(b"old benchmark")
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
        figures_dir=figures_dir,
        processed_dir=tmp_path / "processed",
    )

    assert {path.name for path in figures} == {
        "qber_vs_eve_probability.png",
        "qber_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_error_rate.png",
        "sifted_fraction_vs_channel_loss_rate.png",
    }
    assert all(path.is_file() for path in figures)
    assert not stale_mlkem_figure.exists()


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
        "simulation_elapsed_us",
        "simulation_signals_per_second",
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
        "simulation_elapsed_us": "1000",
        "simulation_signals_per_second": "100000",
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
        "simulation_elapsed_us",
        "simulation_signals_per_second",
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
            "simulation_elapsed_us": "1000",
            "simulation_signals_per_second": "100000",
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
            "simulation_elapsed_us": "2000",
            "simulation_signals_per_second": "50000",
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
    assert "Measured BB84 simulator: simulation_elapsed_us_mean" not in dimensions
    assert dimensions["Measured BB84 simulator: simulation_performance_scope"] == (
        "multiple_conditions_or_runtimes; consult raw CSV"
    )


def test_plotting_reports_bb84_simulator_performance_for_one_runtime(tmp_path):
    qkd_file = tmp_path / "qkd.csv"
    fields = (
        "seed",
        "n_signals",
        "channel_error_rate",
        "eve_probability",
        "channel_loss_rate",
        "qber_threshold",
        "simulator_version",
        "python_version",
        "platform",
        "qber",
        "sifted_fraction",
        "simulation_elapsed_us",
        "simulation_signals_per_second",
    )
    common = {
        "n_signals": "100",
        "channel_error_rate": "0",
        "eve_probability": "0",
        "channel_loss_rate": "0",
        "qber_threshold": "0.11",
        "simulator_version": "0.1.0",
        "python_version": "3.11.0",
        "platform": "test-platform",
        "qber": "0",
        "sifted_fraction": "0.5",
    }
    _write_rows(
        qkd_file,
        fields,
        [
            {
                **common,
                "seed": "1",
                "simulation_elapsed_us": "1000",
                "simulation_signals_per_second": "100000",
            },
            {
                **common,
                "seed": "2",
                "simulation_elapsed_us": "3000",
                "simulation_signals_per_second": "50000",
            },
        ],
    )

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
    assert dimensions["Measured BB84 simulator: simulation_elapsed_us_mean"] == (
        "2000.000000"
    )
    assert dimensions[
        "Measured BB84 simulator: simulation_signals_per_second_mean"
    ] == "75000.000000"


def test_plotting_does_not_combine_mlkem_runs_from_different_environments(
    tmp_path, monkeypatch
):
    from matplotlib.axes import Axes

    labels = []
    original_step = Axes.step

    def record_label(axis, *args, **kwargs):
        labels.append(kwargs.get("label"))
        return original_step(axis, *args, **kwargs)

    monkeypatch.setattr(Axes, "step", record_label)
    fields = (
        "algorithm",
        "operation",
        "latency_us",
        "implementation",
        "implementation_version",
        "python_version",
        "platform",
        "warmup_iterations",
        "measured_iterations",
    )
    first = tmp_path / "mlkem-first.csv"
    second = tmp_path / "mlkem-second.csv"
    common = {
        "algorithm": "ML-KEM-768",
        "operation": "key_generation",
        "warmup_iterations": "50",
        "measured_iterations": "1000",
    }
    _write_rows(
        first,
        fields,
        [{
            **common,
            "latency_us": "40",
            "implementation": "pqcrypto",
            "implementation_version": "1.0.0",
            "python_version": "3.11.3",
            "platform": "Windows-A",
        }],
    )
    _write_rows(
        second,
        fields,
        [{
            **common,
            "latency_us": "400",
            "implementation": "pqcrypto",
            "implementation_version": "1.0.0",
            "python_version": "3.12.0",
            "platform": "Linux-B",
        }],
    )

    figures = create_plots(
        pqc_csv=[first, second],
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    assert [path.name for path in figures] == ["mlkem_latency_cdf.png"]
    with next((tmp_path / "processed").glob("comparison_*.csv")).open(
        newline="", encoding="utf-8"
    ) as stream:
        dimensions = {
            row["dimension"]: row["pqc"] for row in csv.DictReader(stream)
        }
    assert dimensions["Measured ML-KEM-768: measurement_scope"] == (
        "multiple_implementations_or_runtimes; consult per-group CDF and raw CSV"
    )
    assert dimensions["Measured ML-KEM-768: measurement_group_count"] == "2"
    assert "Measured ML-KEM-768: key_generation_median_latency_us" not in dimensions
    assert len(labels) == 2
    assert any("Python 3.11.3" in label for label in labels)
    assert any("Python 3.12.0" in label for label in labels)


def test_plotting_records_mlkem_provenance_for_one_environment(tmp_path):
    pqc_file = tmp_path / "mlkem.csv"
    fields = (
        "algorithm",
        "operation",
        "latency_us",
        "implementation",
        "implementation_version",
        "python_version",
        "platform",
        "warmup_iterations",
        "measured_iterations",
    )
    _write_rows(
        pqc_file,
        fields,
        [{
            "algorithm": "ML-KEM-768",
            "operation": "key_generation",
            "latency_us": "40",
            "implementation": "pqcrypto",
            "implementation_version": "1.0.0",
            "python_version": "3.11.3",
            "platform": "Windows-A",
            "warmup_iterations": "50",
            "measured_iterations": "1000",
        }],
    )

    create_plots(
        pqc_csv=pqc_file,
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    with next((tmp_path / "processed").glob("comparison_*.csv")).open(
        newline="", encoding="utf-8"
    ) as stream:
        dimensions = {
            row["dimension"]: row["pqc"] for row in csv.DictReader(stream)
        }
    assert dimensions["Measured ML-KEM-768: key_generation_median_latency_us"] == (
        "40.000000"
    )
    assert dimensions["Measured ML-KEM-768: provenance_implementation_version"] == (
        "1.0.0"
    )
    assert dimensions["Measured ML-KEM-768: provenance_platform"] == "Windows-A"


def test_plotting_keeps_legacy_mlkem_files_separate_without_provenance(tmp_path):
    first = tmp_path / "legacy-first.csv"
    second = tmp_path / "legacy-second.csv"
    fields = ("algorithm", "operation", "latency_us")
    _write_rows(
        first,
        fields,
        [{"algorithm": "ML-KEM-768", "operation": "key_generation", "latency_us": "40"}],
    )
    _write_rows(
        second,
        fields,
        [{"algorithm": "ML-KEM-768", "operation": "key_generation", "latency_us": "400"}],
    )

    create_plots(
        pqc_csv=[first, second],
        figures_dir=tmp_path / "figures",
        processed_dir=tmp_path / "processed",
    )

    with next((tmp_path / "processed").glob("comparison_*.csv")).open(
        newline="", encoding="utf-8"
    ) as stream:
        dimensions = {
            row["dimension"]: row["pqc"] for row in csv.DictReader(stream)
        }
    assert dimensions["Measured ML-KEM-768: measurement_group_count"] == "2"
    assert "Measured ML-KEM-768: key_generation_median_latency_us" not in dimensions
