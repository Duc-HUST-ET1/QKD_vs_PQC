"""A reproducible, educational classical abstraction of BB84."""

from dataclasses import dataclass
import logging
import random
from pathlib import Path

from qkd_pqc import __version__
from qkd_pqc.common.csv_utils import write_csv_exclusive
from qkd_pqc.common.metadata import create_run_id, runtime_metadata
from qkd_pqc.config import QKDConfig

logger = logging.getLogger(__name__)

BB84_CSV_FIELDS = (
    "run_id",
    "timestamp_utc",
    "seed",
    "n_signals",
    "channel_error_rate",
    "eve_probability",
    "qber_threshold",
    "sifted_bits",
    "error_bits",
    "qber",
    "sifted_fraction",
    "illustrative_status",
    "simulator_version",
    "python_version",
    "platform",
)


@dataclass(frozen=True)
class BB84Result:
    """Run-level measurements from the simplified BB84 teaching simulation."""

    run_id: str
    timestamp_utc: str
    seed: int
    n_signals: int
    channel_error_rate: float
    eve_probability: float
    qber_threshold: float
    sifted_bits: int
    error_bits: int
    qber: float | None
    sifted_fraction: float
    illustrative_status: str
    simulator_version: str
    python_version: str
    platform: str

    def as_csv_row(self) -> dict[str, object]:
        """Serialize the run result using the documented CSV field names."""
        return {
            field: getattr(self, field)
            for field in BB84_CSV_FIELDS
        }


def simulate_bb84(config: QKDConfig, seed: int | None = None) -> BB84Result:
    """Simulate BB84-like bit/basis behavior; this is not a quantum implementation."""
    if seed is None:
        raise ValueError("A random seed is required for reproducible BB84 simulation.")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a non-negative integer.")
    if isinstance(config.n_signals, bool) or not isinstance(config.n_signals, int):
        raise ValueError("n_signals must be an integer.")
    if config.n_signals < 1:
        raise ValueError("n_signals must be positive.")
    for name, probability in (
        ("channel_error_rate", config.channel_error_rate),
        ("eve_probability", config.eve_probability),
        ("qber_threshold", config.qber_threshold),
    ):
        if (isinstance(probability, bool) or not isinstance(probability, (int, float))
                or not 0.0 <= probability <= 1.0):
            raise ValueError(f"{name} must be between 0 and 1 inclusive.")

    rng = random.Random(seed)
    sifted_bits = 0
    error_bits = 0

    for _ in range(config.n_signals):
        alice_bit = rng.randrange(2)
        alice_basis = rng.randrange(2)

        transmitted_bit = alice_bit
        transmitted_basis = alice_basis
        if rng.random() < config.eve_probability:
            eve_basis = rng.randrange(2)
            eve_bit = alice_bit if eve_basis == alice_basis else rng.randrange(2)
            transmitted_bit = eve_bit
            transmitted_basis = eve_basis

        if rng.random() < config.channel_error_rate:
            transmitted_bit ^= 1

        bob_basis = rng.randrange(2)
        bob_bit = (transmitted_bit if bob_basis == transmitted_basis
                   else rng.randrange(2))

        if bob_basis == alice_basis:
            sifted_bits += 1
            error_bits += bob_bit != alice_bit

    qber = error_bits / sifted_bits if sifted_bits else None
    sifted_fraction = sifted_bits / config.n_signals
    illustrative_status = (
        "illustrative_reject"
        if qber is None or qber > config.qber_threshold
        else "illustrative_accept"
    )
    run_id, timestamp_utc = create_run_id("qkd")
    result = BB84Result(
        run_id=run_id,
        timestamp_utc=timestamp_utc,
        seed=seed,
        n_signals=config.n_signals,
        channel_error_rate=config.channel_error_rate,
        eve_probability=config.eve_probability,
        qber_threshold=config.qber_threshold,
        sifted_bits=sifted_bits,
        error_bits=error_bits,
        qber=qber,
        sifted_fraction=sifted_fraction,
        illustrative_status=illustrative_status,
        simulator_version=__version__,
        **runtime_metadata(),
    )
    logger.info(
        "BB84 simulation complete: %s, sifted=%d/%d, QBER=%s, status=%s",
        result.run_id,
        result.sifted_bits,
        result.n_signals,
        result.qber,
        result.illustrative_status,
    )
    return result


def write_bb84_result(result: BB84Result, output_dir: str | Path) -> Path:
    """Write one run-level BB84 result to a new CSV file."""
    path = Path(output_dir) / f"{result.run_id}.csv"
    return write_csv_exclusive(path, BB84_CSV_FIELDS, [result.as_csv_row()])
