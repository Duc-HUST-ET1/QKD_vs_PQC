from unittest.mock import patch
import csv

import pytest

from qkd_pqc.config import QKDConfig
from qkd_pqc.qkd.bb84_simulator import (
    BB84_CSV_FIELDS,
    simulate_bb84,
    write_bb84_result,
)


def test_simulation_is_reproducible_for_fixed_seed():
    config = QKDConfig(200, 0.03, 0.2, 0.11)

    first = simulate_bb84(config, seed=123)
    second = simulate_bb84(config, seed=123)

    assert first.seed == second.seed
    assert first.sifted_bits == second.sifted_bits
    assert first.error_bits == second.error_bits
    assert first.qber == second.qber
    assert first.sifted_fraction == second.sifted_fraction
    assert first.illustrative_status == second.illustrative_status


def test_qber_is_error_bits_divided_by_sifted_bits():
    result = simulate_bb84(
        QKDConfig(
            n_signals=1000,
            channel_error_rate=1.0,
            eve_probability=0.0,
            qber_threshold=0.11,
        ),
        seed=7,
    )

    assert result.sifted_bits > 0
    assert result.error_bits == result.sifted_bits
    assert result.qber == 1.0
    assert result.illustrative_status == "illustrative_reject"


def test_zero_sifted_bits_has_no_division_by_zero():
    class NoMatchingBasesRandom:
        def __init__(self, _seed):
            self.randrange_values = iter((0, 0, 1, 0))
            self.random_values = iter((1.0, 1.0, 1.0))

        def randrange(self, _stop):
            return next(self.randrange_values)

        def random(self):
            return next(self.random_values)

    with patch("qkd_pqc.qkd.bb84_simulator.random.Random", NoMatchingBasesRandom):
        result = simulate_bb84(QKDConfig(1, 0.0, 0.0, 0.11), seed=9)

    assert result.sifted_bits == 0
    assert result.error_bits == 0
    assert result.qber is None
    assert result.illustrative_status == "illustrative_reject"


def test_simulator_requires_seed():
    try:
        simulate_bb84(QKDConfig(10, 0.0, 0.0, 0.11))
    except ValueError as exc:
        assert "seed" in str(exc)
    else:
        raise AssertionError("Missing seed should be rejected.")


@pytest.mark.parametrize("n_signals", [0, -1, True, 1.5])
def test_invalid_signal_counts_are_rejected(n_signals):
    with pytest.raises(ValueError, match="n_signals"):
        simulate_bb84(QKDConfig(n_signals, 0.0, 0.0, 0.11), seed=1)


@pytest.mark.parametrize("seed", [-1, True, 1.5])
def test_invalid_seeds_are_rejected(seed):
    with pytest.raises(ValueError, match="seed"):
        simulate_bb84(QKDConfig(10, 0.0, 0.0, 0.11), seed=seed)


@pytest.mark.parametrize(
    "config",
    [
        QKDConfig(10, float("nan"), 0.0, 0.11),
        QKDConfig(10, 0.0, float("inf"), 0.11),
        QKDConfig(10, 0.0, 0.0, float("nan")),
        QKDConfig(10, -0.01, 0.0, 0.11),
        QKDConfig(10, 0.0, 1.01, 0.11),
        QKDConfig(10, 0.0, 0.0, 0.11, -0.01),
        QKDConfig(10, 0.0, 0.0, 0.11, 1.01),
    ],
)
def test_invalid_probabilities_are_rejected(config):
    with pytest.raises(ValueError):
        simulate_bb84(config, seed=1)


def test_no_eve_and_no_channel_error_keeps_matching_bits_error_free():
    result = simulate_bb84(QKDConfig(10_000, 0.0, 0.0, 0.11), seed=42)

    assert result.sifted_bits > 0
    assert result.error_bits == 0
    assert result.qber == 0.0


def test_intercept_resend_produces_expected_error_trend():
    result = simulate_bb84(QKDConfig(100_000, 0.0, 1.0, 0.11), seed=42)

    # Full intercept-resend gives an expected 25% error rate in sifted bits.
    assert result.qber == pytest.approx(0.25, abs=0.01)


def test_intercept_resend_qber_tracks_attack_probability():
    probabilities = (0.0, 0.25, 0.5, 0.75, 1.0)
    qbers = [
        simulate_bb84(QKDConfig(100_000, 0.0, probability, 0.11), seed=84).qber
        for probability in probabilities
    ]

    assert qbers == sorted(qbers)
    for probability, qber in zip(probabilities, qbers):
        assert qber == pytest.approx(probability / 4, abs=0.01)


def test_channel_noise_qber_tracks_bit_flip_probability():
    probabilities = (0.0, 0.05, 0.1, 0.2)
    qbers = [
        simulate_bb84(QKDConfig(100_000, probability, 0.0, 0.11), seed=85).qber
        for probability in probabilities
    ]

    assert qbers == sorted(qbers)
    for probability, qber in zip(probabilities, qbers):
        assert qber == pytest.approx(probability, abs=0.01)


def test_channel_loss_reduces_received_signals_without_counting_as_bit_errors():
    config = QKDConfig(10_000, 0.0, 0.0, 0.11, 1.0)
    result = simulate_bb84(config, seed=42)

    assert result.received_signals == 0
    assert result.lost_signals == config.n_signals
    assert result.loss_fraction == 1.0
    assert result.sifted_bits == 0
    assert result.error_bits == 0
    assert result.qber is None


def test_channel_loss_only_reduces_received_and_sifted_signal_counts():
    n_signals = 100_000
    losses = (0.0, 0.2, 0.5, 0.8)
    results = [
        simulate_bb84(QKDConfig(n_signals, 0.0, 0.0, 0.11, loss), seed=86)
        for loss in losses
    ]

    assert [result.received_signals for result in results] == sorted(
        (result.received_signals for result in results), reverse=True
    )
    for loss, result in zip(losses, results):
        assert result.qber == 0.0
        assert result.received_signals / n_signals == pytest.approx(1 - loss, abs=0.01)
        assert result.sifted_fraction == pytest.approx((1 - loss) / 2, abs=0.01)


def test_channel_loss_zero_preserves_all_signals():
    result = simulate_bb84(QKDConfig(1000, 0.0, 0.0, 0.11), seed=42)

    assert result.received_signals == result.n_signals
    assert result.lost_signals == 0
    assert result.loss_fraction == 0.0


def test_result_csv_matches_documented_schema(tmp_path):
    result = simulate_bb84(QKDConfig(100, 0.0, 0.0, 0.11), seed=42)
    path = write_bb84_result(result, tmp_path)

    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)

    assert tuple(reader.fieldnames) == BB84_CSV_FIELDS
    assert len(rows) == 1
    assert int(rows[0]["received_signals"]) == result.received_signals
    assert float(rows[0]["loss_fraction"]) == result.loss_fraction
