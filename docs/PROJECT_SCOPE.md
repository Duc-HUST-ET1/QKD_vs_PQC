# Project scope

## Research question

How do QKD and PQC differ in their security assumptions and key-establishment performance, and how
do their infrastructure requirements affect deployment suitability?

## Included work

1. An educational classical simulation of BB84 state/basis behavior, channel bit flips, and a
   configurable intercept-resend Eve.
2. A benchmark adapter for a genuine ML-KEM-768 implementation compatible with NIST FIPS 203.
   It measures key generation, encapsulation, and decapsulation independently when support exists.
3. A qualitative, reference-led comparison of security models and deployment constraints.
4. CSV provenance, reproducibility, tests, and plots derived only from collected run files.

## Excluded work and interpretation

The BB84 simulation is not a quantum simulator or a secure QKD stack. It does not implement
authentication, error correction, privacy amplification, finite-key proofs, optical effects,
device side channels, or hardware. Its 0.11 QBER threshold is a teaching parameter only: passing
that threshold does not prove a key secure.

ML-KEM-768 is the NIST-standardized algorithm specified by FIPS 203. Benchmark availability
depends on an installed compatible implementation. The benchmark does not measure networking,
protocol integration, key-management overhead, or installation. It does not establish that PQC is
universally faster or more suitable than QKD.

No invented quantitative cost, range, or throughput comparison is in scope. Measured values must
be explicitly distinguished from qualitative claims and assumptions.

## Independent workstreams

All five workstreams may start in parallel against the documented interfaces. Shared interface
changes should be coordinated by pull request; ownership and acceptance criteria are in
`TEAM_ASSIGNMENTS.md`.
