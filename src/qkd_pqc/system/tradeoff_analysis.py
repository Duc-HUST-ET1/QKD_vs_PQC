"""Structured qualitative QKD and PQC trade-off descriptions."""

from dataclasses import dataclass
import math
from typing import Literal, Mapping

EvidenceType = Literal[
    "qualitative_reference_based",
    "qualitative_assumption",
    "project_scope_limit",
    "measured_project_data",
    "measurement_metadata",
]


@dataclass(frozen=True)
class TradeoffItem:
    """One comparison dimension with evidence provenance."""

    dimension: str
    qkd: str
    pqc: str
    evidence_type: EvidenceType


def _validated_metrics(
    metrics: Mapping[str, str | float | int] | None,
    label: str,
) -> list[tuple[str, str]]:
    if metrics is None:
        return []
    if not isinstance(metrics, Mapping):
        raise ValueError(f"{label} metrics must be a mapping.")
    if any(not isinstance(name, str) or not name.strip() for name in metrics):
        raise ValueError(f"{label} metric names must be non-empty strings.")

    normalized: list[tuple[str, str]] = []
    for name, value in sorted(metrics.items()):
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            raise ValueError(f"Metric '{name}' must be a string or finite number.")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"Metric '{name}' must be finite.")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"Metric '{name}' must not be empty.")
        if isinstance(value, str):
            try:
                numeric_value = float(value)
            except ValueError:
                pass
            else:
                if not math.isfinite(numeric_value):
                    raise ValueError(f"Metric '{name}' must be finite.")
        normalized.append((name, str(value)))
    return normalized


def _is_measurement_metadata(name: str) -> bool:
    """Identify scope/count/provenance fields that describe measurements, not values."""
    return (
        name in {"measurement_scope", "measurement_group_count", "setting_count"}
        or name.startswith("provenance_")
        or name.endswith("_scope")
        or name.endswith("_setting_count")
        or name.endswith("_rows")
    )


def analyze_tradeoffs(
    qkd_metrics: Mapping[str, str | float | int] | None = None,
    pqc_metrics: Mapping[str, str | float | int] | None = None,
) -> list[TradeoffItem]:
    """Return qualitative claims and caller-designated measurements.

    Metric mappings must contain summaries derived from validated project CSV data. This function
    labels supplied values as measured but cannot verify their source or preserve their provenance.
    """
    validated_qkd_metrics = _validated_metrics(qkd_metrics, "QKD")
    validated_pqc_metrics = _validated_metrics(pqc_metrics, "PQC")
    items = [
        TradeoffItem(
            "Security basis",
            "Protocol security is based on quantum-state measurement behavior under protocol and "
            "implementation assumptions [1, 2].",
            "Computational security relies on the Module-LWE-based construction specified by "
            "NIST FIPS 203 [3].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Key establishment",
            "Transmits quantum states, then uses classical post-processing [1, 2].",
            "Encapsulation produces a shared secret using the standardized KEM interface [3].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Performance evidence boundary",
            "The measured elapsed time and signals per second are for this Python teaching "
            "simulator only; they are not physical QKD key-generation throughput or secret-key "
            "rate.",
            "The measured key-generation, encapsulation, and decapsulation times are local "
            "primitive timings; they are not a network handshake or end-to-end protocol latency.",
            "project_scope_limit",
        ),
        TradeoffItem(
            "Quantum adversary",
            "The protocol's security motivation concerns information gain from quantum measurement; "
            "real deployment security remains device- and proof-dependent [1, 2].",
            "ML-KEM-768 is designed for post-quantum security under its computational assumptions; "
            "this is not an unconditional guarantee [3].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Authentication",
            "Requires an authenticated classical channel; QKD does not remove the authentication "
            "bootstrap requirement [2, 5].",
            "ML-KEM alone does not authenticate endpoints; an authenticated protocol is still "
            "required [3, 8].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Infrastructure",
            "A deployment needs quantum transmission equipment and a usable quantum channel, plus "
            "an authenticated classical channel and trust bootstrap. Without these prerequisites, "
            "this project cannot establish QKD deployment suitability [5, 6].",
            "A deployment can use classical computation and communication, but needs a supported "
            "ML-KEM implementation, authenticated protocol integration, and endpoint/key "
            "management. A primitive benchmark alone does not establish deployment suitability "
            "[3, 8].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Deployment and operations",
            "Suitability depends on whether the target sites can support the required QKD equipment, "
            "channel, authentication, and operations; this repository has no site, distance, cost, "
            "or field-performance data.",
            "Suitability depends on target-platform support, protocol integration, authentication, "
            "and key lifecycle; this repository does not measure application or network performance.",
            "qualitative_assumption",
        ),
        TradeoffItem(
            "Endpoint and key lifecycle",
            "Endpoint protection, authentication credentials, and key management remain necessary "
            "outside the QKD exchange [4].",
            "The KEM shared secret requires protected endpoints and application-level key handling "
            "after decapsulation [4, 8].",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Scalability and limitations",
            "This project has no field deployment data; the educational simulation cannot establish "
            "range, cost, throughput, or security.",
            "This software primitive benchmark cannot establish network performance, cost, or "
            "universal superiority over QKD.",
            "project_scope_limit",
        ),
    ]
    if validated_qkd_metrics:
        for name, value in validated_qkd_metrics:
            items.append(TradeoffItem(
                dimension=(
                    f"Measured BB84 simulator: {name}"
                    if name.startswith("simulation_")
                    else f"Measured QKD: {name}"
                ),
                qkd=value,
                pqc="not applicable",
                evidence_type=(
                    "measurement_metadata"
                    if _is_measurement_metadata(name)
                    else "measured_project_data"
                ),
            ))
    if validated_pqc_metrics:
        for name, value in validated_pqc_metrics:
            items.append(TradeoffItem(
                dimension=f"Measured ML-KEM-768: {name}",
                qkd="not applicable",
                pqc=value,
                evidence_type=(
                    "measurement_metadata"
                    if _is_measurement_metadata(name)
                    else "measured_project_data"
                ),
            ))
    return items
