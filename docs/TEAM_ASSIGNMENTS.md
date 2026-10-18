# Team assignments

All workstreams can begin in parallel using the interfaces in the README and the schemas in
`DATA_DICTIONARY.md`. Coordinate shared-file changes through pull requests; do not overwrite a
member's principal deliverable.

## Member 1 — Security model and literature

- **Responsibilities:** Research question and scope; threat model and security assumptions;
  literature and standards references; comparison of security principles and authentication
  requirements; accuracy review of conclusions.
- **Principal deliverable:** `docs/THREAT_MODEL.md` and security-related references in
  `docs/REFERENCES.md`.
- **Acceptance criteria:** Claims distinguish QKD protocol assumptions from computational
  assumptions; authentication is treated explicitly; references are traceable; simulator
  limitations and no-security-guarantee warning are unambiguous.
- **Interface:** Coordinate terminology and evidence labels with Member 4; review Member 5's
  summary claims before final reporting.

## Member 2 — BB84 simulation

- **Responsibilities:** Alice's random bits/bases; Bob's random bases and outcomes; Eve
  intercept-resend probability; channel bit-flip noise; basis sifting; QBER, sifted count/rate,
  illustrative status; deterministic seed.
- **Principal deliverable:** `src/qkd_pqc/qkd/bb84_simulator.py` and `scripts/run_qkd.py`.
- **Acceptance criteria:** Fixed-seed runs reproduce; operation order is documented; zero sifted
  bits are safe; tests verify noise, sifting, and CSV output; no claim of production security.
- **Interface:** Return `BB84Result` from `simulate_bb84(QKDConfig, seed=None)` and write the
  documented run-level CSV through the shared CSV utility.

## Member 3 — ML-KEM-768 benchmark

- **Responsibilities:** Verify actual implementation support; separately measure key generation,
  encapsulation, and decapsulation; verify shared-secret equality; report sizes, software/platform,
  warmups, repetitions, median, and p95; export machine-readable samples.
- **Principal deliverable:** `src/qkd_pqc/pqc/mlkem_benchmark.py` and
  `scripts/run_pqc_benchmark.py`.
- **Acceptance criteria:** Only the exact ML-KEM-768 implementation is accepted; missing or
  incompatible support has an actionable diagnostic; timing uses a monotonic high-resolution
  clock and excludes setup/I/O; correctness is checked; optional tests skip honestly.
- **Interface:** Return `BenchmarkResults` and write individual operation samples with the schema
  in `DATA_DICTIONARY.md`; use `MLKEMUnavailableError` for unsupported environments.

## Member 4 — Infrastructure and system trade-offs

- **Responsibilities:** Compare security assumptions; explain quantum and authenticated-classical
  QKD channels; describe classical ML-KEM infrastructure; analyze authentication, deployment,
  scalability, operations, and failure modes; distinguish measured from literature-based or
  assumed values.
- **Principal deliverable:** `src/qkd_pqc/system/tradeoff_analysis.py` and coordinated
  contributions to `docs/THREAT_MODEL.md`.
- **Acceptance criteria:** Trade-offs are qualitative unless backed by actual project data;
  evidence type is present; no unsupported distance/cost/throughput claims; inputs are validated.
- **Interface:** Return typed `TradeoffItem` values for Member 5's comparison table; coordinate
  threat-model edits with Member 1.

## Member 5 — Integration, reproducibility, and visualization

- **Responsibilities:** Shared interfaces and runnable pipeline; validate documented CSV schemas;
  generate figures and comparison tables from actual data; run tests; maintain final report assets.
- **Principal deliverable:** `src/qkd_pqc/analysis/plotting.py`, `scripts/run_analysis.py`,
  `scripts/run_all.py`, and integration/setup sections of `README.md`.
- **Acceptance criteria:** Pipeline reports completed/skipped/failed stages accurately; analysis
  validates columns and never fabricates points; figures have units and labeled axes; tests and
  reproduction commands are documented.
- **Interface:** Consume Member 2's run-level QKD CSV and Member 3's per-operation ML-KEM CSV;
  consume the typed trade-off items from Member 4 and security-reviewed language from Member 1.
