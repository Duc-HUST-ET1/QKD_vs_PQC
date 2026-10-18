# Threat model and security assumptions

This document describes the comparison boundary, not a security certification.

## Assets and actors

The compared systems establish shared key material for later use. Relevant actors are legitimate
communicating endpoints, a passive network observer, an active network attacker, a potential
quantum-capable attacker, and (for the BB84 teaching scenario) an intercept-resend Eve. Endpoint
compromise, implementation vulnerabilities, supply-chain compromise, and denial of service remain
out of scope for the toy simulation.

## BB84 / QKD assumptions and boundaries

The textbook BB84 security intuition uses quantum-state measurement disturbance and the no-cloning
principle. A practical QKD deployment additionally depends on device and implementation security,
authenticated classical communication, key management, and protocol-specific security processing.
Authentication prevents an active attacker from replacing the parties in classical
reconciliation; it must itself be bootstrapped from a trusted credential or an existing secret.

The project's simulator is a seeded classical abstraction of bits and two bases. It models
intercept-resend choices and independent channel bit flips, but not actual quantum states, detectors,
optical losses, side channels, finite-key proofs, error correction, or privacy amplification. A
QBER at or below 0.11 does **not** prove that a key is secure. Its accept/reject label is an
illustrative teaching result only.

## ML-KEM-768 / PQC assumptions and boundaries

ML-KEM-768 is a classical key-encapsulation mechanism standardized in NIST FIPS 203. Its security
is computational and based on the Module Learning With Errors problem as specified in the
standard. It is designed to resist known classical and quantum attacks under those assumptions;
this is not an unconditional guarantee. Correct implementation, parameter selection, random-number
generation, protocol composition, authentication, and key handling remain necessary.

ML-KEM is not an authentication mechanism by itself. Applications still need authenticated
identities and an authenticated protocol to resist active man-in-the-middle attacks. The project
benchmark measures primitive operations, not a complete network handshake or application.

## Comparative interpretation

QKD requires a quantum channel plus a classical channel that is authenticated and suitable
infrastructure at both endpoints; distance, operating conditions, and integration are deployment
constraints to assess using external evidence. ML-KEM uses ordinary classical computation and
communications, and does not require quantum transmission hardware; deployed systems still require
protocol integration and authentication.

This repository collects no infrastructure cost, network distance, or throughput measurement.
Avoid universal statements that one approach is faster, cheaper, or more secure. Keep QBER separate
from software operation latency. Cite any qualitative claims with the sources in `REFERENCES.md`
and label assumptions explicitly.

## Sources

See [REFERENCES.md](REFERENCES.md), especially NIST FIPS 203 for ML-KEM and the foundational
BB84 paper for protocol context. The team's security reviewer should verify cited editions and
claims before final publication.
