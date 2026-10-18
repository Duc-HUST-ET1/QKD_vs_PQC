"""Capability detection and benchmarking for a real ML-KEM-768 implementation."""

from dataclasses import dataclass
import importlib
from importlib.metadata import PackageNotFoundError, version
import logging
import math
from pathlib import Path
import time

from qkd_pqc.common.csv_utils import write_csv_exclusive
from qkd_pqc.common.metadata import create_run_id, runtime_metadata
from qkd_pqc.config import PQCConfig

logger = logging.getLogger(__name__)

MLKEM_CSV_FIELDS = (
    "run_id",
    "timestamp_utc",
    "algorithm",
    "operation",
    "iteration",
    "latency_us",
    "median_latency_us",
    "p95_latency_us",
    "public_key_bytes",
    "secret_key_bytes",
    "ciphertext_bytes",
    "shared_secret_bytes",
    "warmup_iterations",
    "measured_iterations",
    "implementation",
    "implementation_version",
    "platform",
    "python_version",
)
OPERATIONS = ("key_generation", "encapsulation", "decapsulation")
IMPLEMENTATION_NAME = "pqcrypto (pqcrypto.kem.ml_kem_768)"


class MLKEMUnavailableError(RuntimeError):
    """Raised when the supported ML-KEM-768 implementation is unavailable."""


@dataclass(frozen=True)
class MLKEMImplementation:
    """Validated function handles for the exact ML-KEM-768 API used by this project."""

    module: object
    implementation: str
    implementation_version: str


@dataclass(frozen=True)
class BenchmarkSample:
    """One timed operation sample, in microseconds."""

    operation: str
    iteration: int
    latency_us: float
    median_latency_us: float
    p95_latency_us: float
    public_key_bytes: int | None
    secret_key_bytes: int | None
    ciphertext_bytes: int | None
    shared_secret_bytes: int | None


@dataclass(frozen=True)
class BenchmarkResults:
    """Raw operation samples and their unique CSV output path."""

    run_id: str
    timestamp_utc: str
    samples: tuple[BenchmarkSample, ...]
    output_path: Path
    warmup_iterations: int
    measured_iterations: int
    implementation: str
    implementation_version: str


def detect_mlkem_implementation() -> MLKEMImplementation | None:
    """Probe and verify the pqcrypto ML-KEM-768 API; never substitute an algorithm."""
    try:
        module = importlib.import_module("pqcrypto.kem.ml_kem_768")
    except (ImportError, ModuleNotFoundError) as exc:
        logger.warning(
            "ML-KEM-768 unavailable: install the optional dependency with "
            "`python -m pip install -e \".[mlkem]\". Details: %s",
            exc,
        )
        return None

    required = ("generate_keypair", "encrypt", "decrypt")
    missing = [name for name in required if not callable(getattr(module, name, None))]
    if missing:
        logger.warning("ML-KEM-768 API is incompatible; missing callable(s): %s", ", ".join(missing))
        return None

    try:
        implementation_version = version("pqcrypto")
    except PackageNotFoundError:
        logger.warning("The ML-KEM-768 module is importable but its pqcrypto version is unknown.")
        return None

    try:
        public_key, secret_key = module.generate_keypair()
        ciphertext, encapsulated_secret = module.encrypt(public_key)
        decapsulated_secret = module.decrypt(secret_key, ciphertext)
    except (TypeError, ValueError, RuntimeError) as exc:
        logger.warning("ML-KEM-768 capability self-test failed: %s", exc)
        return None
    if not isinstance(encapsulated_secret, bytes) or encapsulated_secret != decapsulated_secret:
        logger.warning("ML-KEM-768 capability self-test failed shared-secret verification.")
        return None
    if not all(isinstance(value, bytes) for value in (public_key, secret_key, ciphertext)):
        logger.warning("ML-KEM-768 API returned unexpected non-byte key or ciphertext values.")
        return None

    return MLKEMImplementation(
        module=module,
        implementation=IMPLEMENTATION_NAME,
        implementation_version=implementation_version,
    )


def _percentile_95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def _verify_shared_secret(encapsulated: bytes, decapsulated: bytes) -> None:
    if encapsulated != decapsulated:
        raise RuntimeError("ML-KEM-768 decapsulation did not reproduce the encapsulated secret.")


def run_mlkem_benchmark(config: PQCConfig, output_dir: str | Path) -> BenchmarkResults:
    """Benchmark verified ML-KEM-768 operations and save per-trial CSV data."""
    if config.algorithm != "ML-KEM-768":
        raise ValueError("Only the standardized ML-KEM-768 algorithm is supported.")
    if (
        isinstance(config.warmup_iterations, bool)
        or not isinstance(config.warmup_iterations, int)
        or isinstance(config.measured_iterations, bool)
        or not isinstance(config.measured_iterations, int)
    ):
        raise ValueError("Iteration counts must be integers.")
    if config.warmup_iterations < 0 or config.measured_iterations < 1:
        raise ValueError("Warm-up count must be non-negative and measured count must be positive.")

    implementation = detect_mlkem_implementation()
    if implementation is None:
        raise MLKEMUnavailableError(
            "No verified pqcrypto ML-KEM-768 implementation is available. Install the optional "
            "dependency with `python -m pip install -e \".[mlkem]\"`; no substitute was used."
        )

    module = implementation.module
    for _ in range(config.warmup_iterations):
        public_key, secret_key = module.generate_keypair()
        ciphertext, shared_secret = module.encrypt(public_key)
        _verify_shared_secret(shared_secret, module.decrypt(secret_key, ciphertext))

    samples_by_operation: dict[str, list[tuple[float, dict[str, int | None]]]] = {
        operation: [] for operation in OPERATIONS
    }
    for _ in range(config.measured_iterations):
        start = time.perf_counter_ns()
        public_key, secret_key = module.generate_keypair()
        keygen_latency = (time.perf_counter_ns() - start) / 1_000.0
        samples_by_operation["key_generation"].append(
            (keygen_latency, {
                "public_key_bytes": len(public_key),
                "secret_key_bytes": len(secret_key),
                "ciphertext_bytes": None,
                "shared_secret_bytes": None,
            })
        )

        start = time.perf_counter_ns()
        ciphertext, shared_secret = module.encrypt(public_key)
        encapsulation_latency = (time.perf_counter_ns() - start) / 1_000.0
        samples_by_operation["encapsulation"].append(
            (encapsulation_latency, {
                "public_key_bytes": len(public_key),
                "secret_key_bytes": None,
                "ciphertext_bytes": len(ciphertext),
                "shared_secret_bytes": len(shared_secret),
            })
        )

        start = time.perf_counter_ns()
        decapsulated_secret = module.decrypt(secret_key, ciphertext)
        decapsulation_latency = (time.perf_counter_ns() - start) / 1_000.0
        _verify_shared_secret(shared_secret, decapsulated_secret)
        samples_by_operation["decapsulation"].append(
            (decapsulation_latency, {
                "public_key_bytes": None,
                "secret_key_bytes": len(secret_key),
                "ciphertext_bytes": len(ciphertext),
                "shared_secret_bytes": len(decapsulated_secret),
            })
        )

    samples: list[BenchmarkSample] = []
    for operation, trials in samples_by_operation.items():
        latencies = [latency for latency, _ in trials]
        median = sorted(latencies)[len(latencies) // 2] if len(latencies) % 2 else (
            sorted(latencies)[len(latencies) // 2 - 1]
            + sorted(latencies)[len(latencies) // 2]
        ) / 2
        p95 = _percentile_95(latencies)
        for iteration, (latency, sizes) in enumerate(trials, start=1):
            samples.append(BenchmarkSample(
                operation=operation,
                iteration=iteration,
                latency_us=latency,
                median_latency_us=median,
                p95_latency_us=p95,
                **sizes,
            ))

    run_id, timestamp_utc = create_run_id("mlkem")
    metadata = runtime_metadata()
    rows = [
        {
            "run_id": run_id,
            "timestamp_utc": timestamp_utc,
            "algorithm": config.algorithm,
            "operation": sample.operation,
            "iteration": sample.iteration,
            "latency_us": sample.latency_us,
            "median_latency_us": sample.median_latency_us,
            "p95_latency_us": sample.p95_latency_us,
            "public_key_bytes": sample.public_key_bytes,
            "secret_key_bytes": sample.secret_key_bytes,
            "ciphertext_bytes": sample.ciphertext_bytes,
            "shared_secret_bytes": sample.shared_secret_bytes,
            "warmup_iterations": config.warmup_iterations,
            "measured_iterations": config.measured_iterations,
            "implementation": implementation.implementation,
            "implementation_version": implementation.implementation_version,
            **metadata,
        }
        for sample in samples
    ]
    output_path = Path(output_dir) / f"{run_id}.csv"
    write_csv_exclusive(output_path, MLKEM_CSV_FIELDS, rows)

    for operation in OPERATIONS:
        operation_samples = [sample for sample in samples if sample.operation == operation]
        logger.info(
            "%s: median=%.3f us, p95=%.3f us, n=%d",
            operation,
            operation_samples[0].median_latency_us,
            operation_samples[0].p95_latency_us,
            len(operation_samples),
        )
    return BenchmarkResults(
        run_id=run_id,
        timestamp_utc=timestamp_utc,
        samples=tuple(samples),
        output_path=output_path,
        warmup_iterations=config.warmup_iterations,
        measured_iterations=config.measured_iterations,
        implementation=implementation.implementation,
        implementation_version=implementation.implementation_version,
    )
