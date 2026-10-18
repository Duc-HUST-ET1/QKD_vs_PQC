import csv

import pytest

from qkd_pqc.config import PQCConfig
from qkd_pqc.pqc import mlkem_benchmark


def test_mlkem_csv_schema_has_required_fields():
    assert {
        "run_id",
        "algorithm",
        "operation",
        "latency_us",
        "public_key_bytes",
        "secret_key_bytes",
        "ciphertext_bytes",
        "shared_secret_bytes",
        "warmup_iterations",
        "measured_iterations",
        "implementation",
        "implementation_version",
        "platform",
    }.issubset(mlkem_benchmark.MLKEM_CSV_FIELDS)


@pytest.mark.skipif(
    mlkem_benchmark.detect_mlkem_implementation() is None,
    reason="Optional verified pqcrypto ML-KEM-768 implementation is not installed.",
)
def test_mlkem_shared_secret_equality_when_implementation_available():
    implementation = mlkem_benchmark.detect_mlkem_implementation()
    assert implementation is not None
    public_key, secret_key = implementation.module.generate_keypair()
    ciphertext, encapsulated_secret = implementation.module.encrypt(public_key)
    decapsulated_secret = implementation.module.decrypt(secret_key, ciphertext)

    assert encapsulated_secret == decapsulated_secret


def test_missing_mlkem_is_reported_without_substitution(monkeypatch, tmp_path):
    monkeypatch.setattr(mlkem_benchmark, "detect_mlkem_implementation", lambda: None)

    with pytest.raises(mlkem_benchmark.MLKEMUnavailableError, match="no substitute"):
        mlkem_benchmark.run_mlkem_benchmark(
            PQCConfig("ML-KEM-768", warmup_iterations=0, measured_iterations=1),
            tmp_path,
        )
    assert list(tmp_path.iterdir()) == []


@pytest.mark.skipif(
    mlkem_benchmark.detect_mlkem_implementation() is None,
    reason="Optional verified pqcrypto ML-KEM-768 implementation is not installed.",
)
def test_mlkem_benchmark_exports_operation_samples_when_available(tmp_path):
    results = mlkem_benchmark.run_mlkem_benchmark(
        PQCConfig("ML-KEM-768", warmup_iterations=1, measured_iterations=2),
        tmp_path,
    )

    with results.output_path.open("r", newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 6
    assert {row["operation"] for row in rows} == {
        "key_generation",
        "encapsulation",
        "decapsulation",
    }
    assert all(float(row["median_latency_us"]) >= 0 for row in rows)
    assert all(float(row["p95_latency_us"]) >= 0 for row in rows)
