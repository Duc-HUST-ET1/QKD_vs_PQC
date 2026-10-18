# Data dictionary

All run CSVs are UTF-8 with a header row. Empty fields mean a measurement does not apply or is
unavailable; they are not zero. Actual runs belong in `data/raw/`. Illustrative material belongs
only in `data/example/` and must be labelled as such.

## Configuration

`configs/experiment_config.yaml` contains:

| Key | Type | Default | Validation |
|---|---|---:|---|
| `project.name` | string | `QKD vs PQC` | Non-empty |
| `project.random_seed` | integer | `42` | Non-negative |
| `qkd.n_signals` | integer | `100000` | Positive |
| `qkd.channel_error_rate` | probability | `0.01` | Inclusive range [0, 1] |
| `qkd.eve_probability` | probability | `0.0` | Inclusive range [0, 1] |
| `qkd.qber_threshold` | probability | `0.11` | Inclusive range [0, 1] |
| `pqc.algorithm` | string | `ML-KEM-768` | Must match supported algorithm |
| `pqc.warmup_iterations` | integer | `50` | Non-negative |
| `pqc.measured_iterations` | integer | `1000` | Positive |
| `output.*_dir` | relative path | see YAML | Relative paths resolve from project root |

## BB84 run-level CSV

One row represents one simulation run. A run is replayable from its inputs, implementation
version, and seed. It does not publish sifted key bits.

| Column | Meaning |
|---|---|
| `run_id` | Unique UTC-based run identifier |
| `timestamp_utc` | Run creation time in UTC |
| `seed` | Pseudorandom generator seed |
| `n_signals` | Number of simulated signals |
| `channel_error_rate` | Configured independent channel bit-flip probability |
| `eve_probability` | Configured per-signal intercept probability |
| `qber_threshold` | Configured pedagogical threshold |
| `sifted_bits` | Number of matching-basis positions |
| `error_bits` | Mismatches among sifted positions |
| `qber` | `error_bits / sifted_bits`; empty if no bits were sifted |
| `sifted_fraction` | `sifted_bits / n_signals` |
| `illustrative_status` | `illustrative_accept` or `illustrative_reject` |
| `simulator_version` | Version of the project simulator |
| `python_version` | Python runtime version |
| `platform` | Runtime platform description |

## ML-KEM-768 benchmark CSV

One row represents one measured operation in one measured iteration. Three operation names are
used: `key_generation`, `encapsulation`, and `decapsulation`. Summary columns repeat the
operation-level statistic on its rows. The input preparation and timing boundaries are defined in
`EXPERIMENT_PROTOCOL.md`.

| Column | Meaning |
|---|---|
| `run_id`, `timestamp_utc` | Unique run identity and UTC creation time |
| `algorithm` | Standardized algorithm name (`ML-KEM-768`) |
| `operation` | Timed operation name |
| `iteration` | 1-based measured sample number |
| `latency_us` | Individual elapsed time in microseconds |
| `median_latency_us` | Operation median in microseconds |
| `p95_latency_us` | Operation nearest-rank p95 in microseconds |
| `public_key_bytes` | Public-key length where available |
| `secret_key_bytes` | Secret-key length where available |
| `ciphertext_bytes` | Ciphertext length where available |
| `shared_secret_bytes` | Shared-secret length where available |
| `warmup_iterations` | Warm-up count per operation |
| `measured_iterations` | Measured samples per operation |
| `implementation` | Adapter/library identity |
| `implementation_version` | Installed library version |
| `platform` | Runtime platform description |
| `python_version` | Python runtime version |

Key and ciphertext sizes may be empty where a size is not relevant to that operation or the API
does not expose it. Secret material and contents are never recorded.

## Trade-off comparison table

The derived CSV has `dimension`, `qkd`, `pqc`, and `evidence_type` columns. Evidence types include
`qualitative_reference_based` and `measured_project_data`. Missing project measurements are
labelled unavailable; qualitative claims are not represented as experimental results.
