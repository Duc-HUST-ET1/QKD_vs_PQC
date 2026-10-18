import pytest

from qkd_pqc.system.tradeoff_analysis import analyze_tradeoffs


def test_tradeoffs_separate_qualitative_claims_and_measured_data():
    items = analyze_tradeoffs(qkd_metrics={"mean_qber": 0.05})

    measured = [item for item in items if item.evidence_type == "measured_project_data"]
    qualitative = [item for item in items if item.evidence_type.startswith("qualitative")]
    assert len(measured) == 1
    assert measured[0].qkd == "0.05"
    assert qualitative


@pytest.mark.parametrize(
    "metrics",
    [
        {"": 1},
        {"measurement": float("nan")},
        {"measurement": True},
        {"measurement": ""},
    ],
)
def test_tradeoffs_reject_invalid_measurements(metrics):
    with pytest.raises(ValueError):
        analyze_tradeoffs(pqc_metrics=metrics)
