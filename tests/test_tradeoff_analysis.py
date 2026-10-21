import pytest

from qkd_pqc.system.tradeoff_analysis import analyze_tradeoffs


def test_tradeoffs_separate_qualitative_claims_and_measured_data():
    items = analyze_tradeoffs(
        qkd_metrics={"mean_qber": 0.05},
        pqc_metrics={"key_generation_median_latency_us": 3.2},
    )

    measured = [item for item in items if item.evidence_type == "measured_project_data"]
    assert len(measured) == 2
    assert measured[0].qkd == "0.05"
    assert measured[0].pqc == "not applicable"
    assert measured[1].qkd == "not applicable"
    assert measured[1].pqc == "3.2"
    assert {item.evidence_type for item in items} == {
        "qualitative_reference_based",
        "qualitative_assumption",
        "project_scope_limit",
        "measured_project_data",
    }


def test_tradeoff_claims_keep_authentication_and_sources_explicit():
    items = {item.dimension: item for item in analyze_tradeoffs()}

    assert "authenticated classical channel" in items["Authentication"].qkd
    assert "does not authenticate endpoints" in items["Authentication"].pqc
    assert "[1, 2]" in items["Security basis"].qkd
    assert "[3]" in items["Security basis"].pqc


def test_tradeoff_metrics_are_sorted_deterministically():
    items = analyze_tradeoffs(qkd_metrics={"z_metric": 2, "a_metric": 1})
    measured_dimensions = [
        item.dimension for item in items
        if item.evidence_type == "measured_project_data"
    ]

    assert measured_dimensions == ["Measured QKD: a_metric", "Measured QKD: z_metric"]


@pytest.mark.parametrize(
    "metrics",
    [
        {"": 1},
        {"measurement": float("nan")},
        {"measurement": True},
        {"measurement": ""},
        {1: 1},
        {"valid": 1, 2: 2},
    ],
)
def test_tradeoffs_reject_invalid_measurements(metrics):
    with pytest.raises(ValueError):
        analyze_tradeoffs(pqc_metrics=metrics)


def test_tradeoffs_reject_non_mapping_measurements():
    with pytest.raises(ValueError, match="must be a mapping"):
        analyze_tradeoffs(qkd_metrics=[("measurement", 1)])
