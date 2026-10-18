"""YAML configuration loading and validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from qkd_pqc.paths import PROJECT_ROOT, resolve_project_path


class ConfigurationError(ValueError):
    """Raised when the experiment configuration is missing or invalid."""


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    random_seed: int


@dataclass(frozen=True)
class QKDConfig:
    n_signals: int
    channel_error_rate: float
    eve_probability: float
    qber_threshold: float


@dataclass(frozen=True)
class PQCConfig:
    algorithm: str
    warmup_iterations: int
    measured_iterations: int


@dataclass(frozen=True)
class OutputConfig:
    raw_data_dir: Path
    processed_data_dir: Path
    figures_dir: Path


@dataclass(frozen=True)
class ExperimentConfig:
    project: ProjectConfig
    qkd: QKDConfig
    pqc: PQCConfig
    output: OutputConfig


def _mapping(value: Any, section: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"Configuration section '{section}' must be a mapping.")
    return value


def _positive_integer(value: Any, name: str, *, allow_zero: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError(f"'{name}' must be an integer.")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        qualifier = "non-negative" if allow_zero else "positive"
        raise ConfigurationError(f"'{name}' must be {qualifier}.")
    return value


def _probability(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigurationError(f"'{name}' must be a number between 0 and 1.")
    result = float(value)
    if not 0.0 <= result <= 1.0:
        raise ConfigurationError(f"'{name}' must be between 0 and 1 inclusive.")
    return result


def _relative_output_path(value: Any, name: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"'{name}' must be a non-empty relative path.")
    path = Path(value)
    if path.is_absolute():
        raise ConfigurationError(f"'{name}' must be relative to the project root.")
    return resolve_project_path(path)


def _from_mapping(raw: Any) -> ExperimentConfig:
    root = _mapping(raw, "root")
    project = _mapping(root.get("project"), "project")
    qkd = _mapping(root.get("qkd"), "qkd")
    pqc = _mapping(root.get("pqc"), "pqc")
    output = _mapping(root.get("output"), "output")

    name = project.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ConfigurationError("'project.name' must be a non-empty string.")

    algorithm = pqc.get("algorithm")
    if algorithm != "ML-KEM-768":
        raise ConfigurationError("'pqc.algorithm' must be exactly 'ML-KEM-768'.")

    return ExperimentConfig(
        project=ProjectConfig(
            name=name.strip(),
            random_seed=_positive_integer(project.get("random_seed"), "project.random_seed",
                                          allow_zero=True),
        ),
        qkd=QKDConfig(
            n_signals=_positive_integer(qkd.get("n_signals"), "qkd.n_signals"),
            channel_error_rate=_probability(qkd.get("channel_error_rate"),
                                             "qkd.channel_error_rate"),
            eve_probability=_probability(qkd.get("eve_probability"), "qkd.eve_probability"),
            qber_threshold=_probability(qkd.get("qber_threshold"), "qkd.qber_threshold"),
        ),
        pqc=PQCConfig(
            algorithm=algorithm,
            warmup_iterations=_positive_integer(pqc.get("warmup_iterations"),
                                                "pqc.warmup_iterations", allow_zero=True),
            measured_iterations=_positive_integer(pqc.get("measured_iterations"),
                                                  "pqc.measured_iterations"),
        ),
        output=OutputConfig(
            raw_data_dir=_relative_output_path(output.get("raw_data_dir"),
                                               "output.raw_data_dir"),
            processed_data_dir=_relative_output_path(output.get("processed_data_dir"),
                                                     "output.processed_data_dir"),
            figures_dir=_relative_output_path(output.get("figures_dir"),
                                              "output.figures_dir"),
        ),
    )


def load_config(path: str | Path | None = None) -> ExperimentConfig:
    """Load and validate YAML settings; relative config paths use the project root."""
    config_path = (PROJECT_ROOT / "configs" / "experiment_config.yaml"
                   if path is None else resolve_project_path(path))
    if not config_path.is_file():
        raise ConfigurationError(f"Configuration file does not exist: {config_path}")
    try:
        with config_path.open("r", encoding="utf-8") as stream:
            raw = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Invalid YAML in {config_path}: {exc}") from exc
    return _from_mapping(raw)
