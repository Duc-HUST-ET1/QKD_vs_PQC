from unittest.mock import patch

import pytest

from qkd_pqc.config import QKDConfig
from qkd_pqc.qkd.bb84_simulator import simulate_bb84


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
            self.random_values = iter((1.0, 1.0))

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


@pytest.mark.parametrize(
    "config",
    [
        QKDConfig(10, float("nan"), 0.0, 0.11),
        QKDConfig(10, 0.0, float("inf"), 0.11),
        QKDConfig(10, 0.0, 0.0, float("nan")),
        QKDConfig(10, -0.01, 0.0, 0.11),
        QKDConfig(10, 0.0, 1.01, 0.11),
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
