# Experiment protocol

## Shared provenance and output policy

Use the committed YAML configuration or record the exact alternate configuration. Run IDs are
unique; result files are created exclusively and never overwrite prior raw runs. Store actual
measurements in `data/raw/`, illustrative examples only in `data/example/`, derived tables in
`data/processed/`, and figures in `figures/`. Runtime metadata records the UTC run ID/time,
Python version, and platform where applicable. Do not write key material or shared-secret bytes.

## Experiment A — simplified BB84

Inputs are `n_signals`, `channel_error_rate`, `eve_probability`, `seed`, and `qber_threshold`.
The implementation uses a seeded Python pseudorandom generator.

For each signal, in order:

1. Alice independently chooses a random bit and one of two bases.
2. Eve independently intercepts with the configured probability. For an intercepted signal, she
   chooses a random basis, measures the prepared state (a random bit if her basis differs from
   Alice's), and resends a state in her measurement basis.
3. Channel bit-flip noise is applied to the resent bit (or Alice's prepared bit if not intercepted).
4. Bob independently chooses a random basis and measures: he gets the transmitted bit if his
   basis matches the transmitted state's basis, otherwise a random bit.
5. Alice and Bob publicly compare bases and retain only matching-basis positions. The simulator
   counts retained bits and mismatches and computes QBER = mismatches / retained bits. Sifted
   fraction = retained bits / signals.

When no bits are sifted, QBER is empty/`None`; no division is performed, and status is
`illustrative_reject` because no usable sifted observations remain. Otherwise, the result is
`illustrative_reject` only when QBER is greater than the configured threshold; it is
`illustrative_accept` when QBER is at or below the threshold. These names are pedagogical labels,
not a security decision. In the
classical bit/basis model, Eve's wrong-basis resend randomizes the state relative to the original
basis. This is not a physical quantum-channel implementation.

The run-level CSV records configuration, seed, counts, QBER, fraction, status, run ID, and
environment and simulator-version metadata. The deterministic seed and inputs enable replay. No
sifted key bits are exported.

## Experiment B — ML-KEM-768

The adapter accepts only the `pqcrypto.kem.ml_kem_768` API; it never silently substitutes an
algorithm. It checks the module's keypair, encapsulation, decapsulation functions by executing a
correctness round trip before timing.

Use `time.perf_counter_ns()` for elapsed times. For each warm-up and measured repetition, prepare
inputs outside the relevant timed section where needed. Key generation times only keypair
generation. Encapsulation uses a pre-generated keypair and times only encapsulation. Decapsulation
uses a keypair and ciphertext prepared before its timed section and times only decapsulation.
Shared-secret equality is checked after timing. No output-file I/O is in the timed region.

Each measured trial is retained separately in the CSV; median and nearest-rank p95 (rank
`ceil(0.95 * n)`) are included for each operation. Latencies are reported in microseconds.
Unapplicable sizes are empty. The CSV does not contain public/secret keys, ciphertext bytes, or
shared-secret contents. Package version and platform are recorded. A failed equality check is an
error, not a successful-looking result.

The adapter does not time an OpenSSL subprocess. Process startup and file I/O would be included in
such a timing, so OpenSSL CLI capability is reported separately rather than treated as an
equivalent in-process operation benchmark.

## Experiment C — qualitative system comparison

The system analysis returns named comparison dimensions with an evidence label. Qualitative
statements cite `REFERENCES.md` and identify assumptions. Project measurements may be supplied
separately; absent data is represented as unavailable, never as an invented number. QBER and
cryptographic operation latency are different kinds of measures and must not be compared directly.

## Analysis

Analysis validates required CSV headers and numeric values, skips rows whose specific plotted
measurement is empty, labels axes and units, and writes figures only when their actual input
measurements exist. Missing files or malformed schemas are reported explicitly. No example or
synthetic measurement is generated to fill a gap.
