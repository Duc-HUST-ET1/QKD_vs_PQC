"""Structured qualitative QKD and PQC trade-off descriptions."""

from dataclasses import dataclass
import math
from typing import Mapping


@dataclass(frozen=True)
class TradeoffItem:
    """One comparison dimension with evidence provenance."""

    dimension: str
    qkd: str
    pqc: str
    evidence_type: str


def _validated_metrics(
    metrics: Mapping[str, str | float | int] | None,
    label: str,
) -> list[tuple[str, str]]:
    if metrics is None:
        return []
    if not isinstance(metrics, Mapping):
        raise ValueError(f"{label} metrics must be a mapping.")
    normalized: list[tuple[str, str]] = []
    for name, value in sorted(metrics.items()):
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{label} metric names must be non-empty strings.")
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            raise ValueError(f"Metric '{name}' must be a string or finite number.")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"Metric '{name}' must be finite.")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"Metric '{name}' must not be empty.")
        normalized.append((name, str(value)))
    return normalized


def analyze_tradeoffs(
    qkd_metrics: Mapping[str, str | float | int] | None = None,
    pqc_metrics: Mapping[str, str | float | int] | None = None,
) -> list[TradeoffItem]:
    """Return literature-led qualitative claims plus only explicitly supplied measurements."""
    validated_qkd_metrics = _validated_metrics(qkd_metrics, "QKD")
    validated_pqc_metrics = _validated_metrics(pqc_metrics, "PQC")
    items = [
        TradeoffItem(
            "Security basis",
            "Protocol security is based on quantum-state measurement behavior under protocol and "
            "implementation assumptions.",
            "Computational security relies on the Module-LWE-based construction specified by "
            "NIST FIPS 203.",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Key establishment",
            "Transmits quantum states, then uses classical post-processing.",
            "Encapsulation produces a shared secret over classical inputs and outputs.",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Quantum adversary",
            "The protocol's security motivation concerns information gain from quantum measurement; "
            "real deployment security remains device- and proof-dependent.",
            "ML-KEM-768 is designed for post-quantum security under its computational assumptions; "
            "this is not an unconditional guarantee.",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Authentication",
            "Requires an authenticated classical channel; QKD does not remove the authentication "
            "bootstrap requirement.",
            "ML-KEM alone does not authenticate endpoints; an authenticated protocol is still "
            "required.",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Infrastructure",
            "Requires quantum transmission equipment/channel plus authenticated classical "
            "communications.",
            "Uses classical computation and communication; deployed applications still need "
            "cryptographic protocol integration.",
            "qualitative_reference_based",
        ),
        TradeoffItem(
            "Deployment and operations",
            "Hardware, channel conditions, integration, and operational constraints require "
            "deployment-specific assessment.",
            "Implementation support, protocol integration, key handling, and system constraints "
            "require deployment-specific assessment.",
            "qualitative_assumption",
        ),
        TradeoffItem(
            "Scalability and limitations",
            "This project has no field deployment data; the toy simulation cannot establish range, "
            "cost, throughput, or security.",
            "This software primitive benchmark cannot establish network performance, cost, or "
            "universal superiority over QKD.",
            "project_scope_limit",
        ),
    ]
    if validated_qkd_metrics:
        for name, value in validated_qkd_metrics:
            items.append(TradeoffItem(
                dimension=f"Measured QKD: {name}",
                qkd=value,
                pqc="not applicable",
                evidence_type="measured_project_data",
            ))
    if validated_pqc_metrics:
        for name, value in validated_pqc_metrics:
            items.append(TradeoffItem(
                dimension=f"Measured ML-KEM-768: {name}",
                qkd="not applicable",
                pqc=value,
                evidence_type="measured_project_data",
            ))
    return items
