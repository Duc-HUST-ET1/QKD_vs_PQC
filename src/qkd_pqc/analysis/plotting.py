"""Validation and plotting for actual BB84 and ML-KEM CSV results."""

import csv
import logging
import math
from pathlib import Path
import statistics
from typing import Mapping, Sequence

from qkd_pqc.common.csv_utils import write_csv_exclusive
from qkd_pqc.common.metadata import create_run_id
from qkd_pqc.paths import resolve_project_path
from qkd_pqc.system.tradeoff_analysis import analyze_tradeoffs

logger = logging.getLogger(__name__)

QKD_REQUIRED_COLUMNS = {
    "qber",
    "eve_probability",
    "channel_error_rate",
    "sifted_fraction",
}
PQC_REQUIRED_COLUMNS = {"algorithm", "operation", "latency_us"}
SUMMARY_FIELDS = ("dimension", "qkd", "pqc", "evidence_type")
PQC_OPERATIONS = {"key_generation", "encapsulation", "decapsulation"}


def _read_csv_files(
    paths: Sequence[str | Path],
    required_columns: set[str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path_value in paths:
        path = Path(path_value)
        if not path.is_file():
            raise FileNotFoundError(f"Required experiment CSV does not exist: {path}")
        with path.open("r", newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            actual = set(reader.fieldnames or ())
            missing = required_columns - actual
            if missing:
                raise ValueError(
                    f"{path} is missing required column(s): {', '.join(sorted(missing))}"
                )
            rows.extend(reader)
    return rows


def _unique_qkd_runs(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    """Do not treat repeated exports of the same deterministic seeded run as replicates."""
    unique_rows: list[Mapping[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    identity_columns = (
        "seed",
        "n_signals",
        "channel_error_rate",
        "eve_probability",
        "qber_threshold",
        "channel_loss_rate",
        "simulator_version",
    )
    for row in rows:
        identity_values = tuple(row.get(column, "") for column in identity_columns)
        if not identity_values[0]:
            unique_rows.append(row)
            continue
        if identity_values in seen:
            logger.warning(
                "Ignoring duplicate seeded BB84 run (seed=%s, settings=%s).",
                identity_values[0],
                identity_values[1:-1],
            )
            continue
        seen.add(identity_values)
        unique_rows.append(row)
    return unique_rows


def _number(row: Mapping[str, str], column: str, row_number: int) -> float | None:
    value = row.get(column, "")
    if value is None or not value.strip():
        return None
    try:
        result = float(value)
    except ValueError:
        logger.warning("Skipping row %d: '%s' is not numeric.", row_number, column)
        return None
    if not math.isfinite(result):
        logger.warning("Skipping row %d: '%s' is not finite.", row_number, column)
        return None
    return result


def _valid_pair(
    row: Mapping[str, str],
    x_column: str,
    y_column: str,
    row_number: int,
) -> tuple[float, float] | None:
    x_value = _number(row, x_column, row_number)
    y_value = _number(row, y_column, row_number)
    if x_value is None or y_value is None:
        return None
    if not 0.0 <= x_value <= 1.0 or not 0.0 <= y_value <= 1.0:
        logger.warning(
            "Skipping row %d: expected '%s' and '%s' to be in [0, 1].",
            row_number,
            x_column,
            y_column,
        )
        return None
    return x_value, y_value


def _save_summary_plot(
    rows: Sequence[Mapping[str, str]],
    x_column: str,
    y_column: str,
    required_zero_columns: Sequence[str],
    x_label: str,
    y_label: str,
    title: str,
    path: Path,
) -> bool:
    groups: dict[float, list[float]] = {}
    for index, row in enumerate(rows, start=2):
        controls_are_zero = True
        for column in required_zero_columns:
            raw_value = row.get(column, "0")
            value = _number(row, column, index) if raw_value else 0.0
            if value is None or value != 0.0:
                controls_are_zero = False
                break
        if not controls_are_zero:
            continue
        pair = _valid_pair(row, x_column, y_column, index)
        if pair is not None:
            x_value, y_value = pair
            groups.setdefault(x_value, []).append(y_value)

    if not groups:
        logger.warning("No valid measurements available for %s; figure not created.", title)
        return False
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots()
    x_values = sorted(groups)
    means = [statistics.fmean(groups[value]) for value in x_values]
    deviations = [
        statistics.stdev(groups[value]) if len(groups[value]) > 1 else 0.0
        for value in x_values
    ]
    group_sizes = {len(groups[value]) for value in x_values}
    sample_label = (
        f"n={next(iter(group_sizes))} runs/setting"
        if len(group_sizes) == 1
        else "n varies by setting"
    )
    axis.errorbar(x_values, means, yerr=deviations, fmt="o-", capsize=3)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_title(f"{title} (mean ± 1 SD; {sample_label})")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)
    return True


def _qkd_metrics(rows: Sequence[Mapping[str, str]]) -> dict[str, str]:
    qbers: list[float] = []
    fractions: list[float] = []
    loss_fractions: list[float] = []
    settings: set[tuple[str, ...]] = set()
    for index, row in enumerate(rows, start=2):
        settings.add(
            (
                row.get("n_signals", ""),
                row.get("channel_error_rate", ""),
                row.get("eve_probability", ""),
                row.get("channel_loss_rate", "") or "0",
                row.get("qber_threshold", ""),
                row.get("simulator_version", ""),
            )
        )
        qber = _number(row, "qber", index)
        fraction = _number(row, "sifted_fraction", index)
        if qber is not None and 0.0 <= qber <= 1.0:
            qbers.append(qber)
        if fraction is not None and 0.0 <= fraction <= 1.0:
            fractions.append(fraction)
        loss_fraction = _number(row, "loss_fraction", index)
        if loss_fraction is not None and 0.0 <= loss_fraction <= 1.0:
            loss_fractions.append(loss_fraction)
    metrics: dict[str, str] = {"valid_run_rows": str(len(rows))}
    if len(settings) > 1:
        logger.info(
            "QKD CSVs contain multiple configurations; omitting cross-setting metric averages."
        )
        metrics["measurement_scope"] = "multiple_settings; consult per-setting plots"
        metrics["setting_count"] = str(len(settings))
        return metrics
    if qbers:
        metrics["mean_qber"] = f"{statistics.fmean(qbers):.8f}"
    if fractions:
        metrics["mean_sifted_fraction"] = f"{statistics.fmean(fractions):.8f}"
    if loss_fractions:
        metrics["mean_loss_fraction"] = f"{statistics.fmean(loss_fractions):.8f}"
    return metrics


def _pqc_metrics(rows: Sequence[Mapping[str, str]]) -> dict[str, str]:
    grouped: dict[str, list[float]] = {operation: [] for operation in PQC_OPERATIONS}
    for index, row in enumerate(rows, start=2):
        operation = row.get("operation", "")
        latency = _number(row, "latency_us", index)
        if operation not in grouped:
            logger.warning("Skipping row %d: unknown ML-KEM operation '%s'.", index, operation)
            continue
        if latency is not None and latency >= 0:
            grouped[operation].append(latency)
    metrics: dict[str, str] = {}
    for operation, values in grouped.items():
        if values:
            ordered = sorted(values)
            metrics[f"{operation}_median_latency_us"] = f"{statistics.median(values):.6f}"
            metrics[f"{operation}_p95_latency_us"] = (
                f"{ordered[math.ceil(0.95 * len(ordered)) - 1]:.6f}"
            )
    return metrics


def _write_comparison_table(
    qkd_metrics: Mapping[str, str] | None,
    pqc_metrics: Mapping[str, str] | None,
    processed_dir: Path,
) -> Path:
    items = analyze_tradeoffs(qkd_metrics=qkd_metrics, pqc_metrics=pqc_metrics)
    run_id, _ = create_run_id("comparison")
    path = processed_dir / f"{run_id}.csv"
    rows = [
        {
            "dimension": item.dimension,
            "qkd": item.qkd,
            "pqc": item.pqc,
            "evidence_type": item.evidence_type,
        }
        for item in items
    ]
    return write_csv_exclusive(path, SUMMARY_FIELDS, rows)


def create_plots(
    qkd_csv: str | Path | Sequence[str | Path] | None = None,
    pqc_csv: str | Path | Sequence[str | Path] | None = None,
    figures_dir: str | Path | None = None,
    processed_dir: str | Path | None = None,
) -> list[Path]:
    """Create plots and a comparison table only from validated, actual input CSV files."""
    qkd_paths = ([qkd_csv] if isinstance(qkd_csv, (str, Path))
                 else list(qkd_csv or []))
    pqc_paths = ([pqc_csv] if isinstance(pqc_csv, (str, Path))
                 else list(pqc_csv or []))
    if not qkd_paths and not pqc_paths:
        logger.info("No experiment CSV files supplied; analysis skipped.")
        return []

    qkd_rows = (
        _unique_qkd_runs(_read_csv_files(qkd_paths, QKD_REQUIRED_COLUMNS))
        if qkd_paths else []
    )
    pqc_rows = _read_csv_files(pqc_paths, PQC_REQUIRED_COLUMNS) if pqc_paths else []
    figures_path = Path(figures_dir) if figures_dir else resolve_project_path("figures")
    processed_path = (
        Path(processed_dir) if processed_dir
        else resolve_project_path("data/processed")
    )
    figures_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    if qkd_rows:
        series = (
            (
                "eve_probability", "qber", ("channel_error_rate", "channel_loss_rate"),
                "Eve intercept probability", "Mean QBER",
                "QBER vs Eve probability (noise=0, loss=0)",
                "qber_vs_eve_probability.png",
            ),
            (
                "channel_error_rate", "qber", ("eve_probability", "channel_loss_rate"),
                "Channel bit-flip probability", "Mean QBER",
                "QBER vs channel noise (Eve=0, loss=0)",
                "qber_vs_channel_error_rate.png",
            ),
            (
                "channel_error_rate", "sifted_fraction", ("eve_probability", "channel_loss_rate"),
                "Channel bit-flip probability", "Mean sifted fraction",
                "Sifted fraction vs channel noise (Eve=0, loss=0)",
                "sifted_fraction_vs_channel_error_rate.png",
            ),
            (
                "channel_loss_rate", "sifted_fraction", ("eve_probability", "channel_error_rate"),
                "Channel loss probability", "Mean sifted fraction",
                "Sifted fraction vs channel loss (Eve=0, noise=0)",
                "sifted_fraction_vs_channel_loss_rate.png",
            ),
        )
        for x_column, y_column, controls, x_label, y_label, title, filename in series:
            path = figures_path / filename
            if _save_summary_plot(
                qkd_rows, x_column, y_column, controls, x_label, y_label, title, path
            ):
                created.append(path)

    if pqc_rows:
        grouped: dict[str, list[float]] = {operation: [] for operation in PQC_OPERATIONS}
        for index, row in enumerate(pqc_rows, start=2):
            if row.get("algorithm") != "ML-KEM-768":
                raise ValueError(
                    f"Row {index} has unsupported algorithm {row.get('algorithm')!r}; "
                    "only ML-KEM-768 results may be analyzed."
                )
            operation = row.get("operation", "")
            latency = _number(row, "latency_us", index)
            if operation not in grouped:
                logger.warning("Skipping row %d: unknown ML-KEM operation '%s'.", index, operation)
                continue
            if latency is not None and latency >= 0:
                grouped[operation].append(latency)
            elif latency is not None:
                logger.warning("Skipping row %d: latency_us must be non-negative.", index)

        if any(grouped.values()):
            import matplotlib.pyplot as plt

            figure, axis = plt.subplots()
            for operation, values in grouped.items():
                if values:
                    ordered = sorted(values)
                    cumulative = [(index + 1) / len(ordered)
                                 for index in range(len(ordered))]
                    axis.step(ordered, cumulative, where="post", label=operation)
            axis.set_xlabel("Operation latency (microseconds)")
            axis.set_ylabel("Cumulative fraction")
            axis.set_title("ML-KEM-768 operation latency distributions")
            axis.set_ylim(0.0, 1.0)
            axis.grid(True, alpha=0.3)
            axis.legend()
            figure.tight_layout()
            path = figures_path / "mlkem_latency_cdf.png"
            figure.savefig(path, dpi=150)
            plt.close(figure)
            created.append(path)
        else:
            logger.warning("No valid ML-KEM latency samples; latency figure not created.")

    comparison_path = _write_comparison_table(
        _qkd_metrics(qkd_rows) if qkd_rows else None,
        _pqc_metrics(pqc_rows) if pqc_rows else None,
        processed_path,
    )
    logger.info("Comparison table saved: %s", comparison_path)
    logger.info("Created %d figure(s).", len(created))
    return created
