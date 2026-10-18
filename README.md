# Quantum Key Distribution versus Post-Quantum Cryptography

This university project compares a simplified BB84 quantum key distribution (QKD) simulation with
a benchmark of standardized ML-KEM-768, and discusses their security assumptions and deployment
trade-offs.

**Research question:** “How do QKD and PQC differ in their security assumptions and
key-establishment performance, and how do their infrastructure requirements affect deployment
suitability?”

The simulator is educational, not a production-secure QKD implementation. The ML-KEM benchmark
uses a real implementation only when its ML-KEM-768 API is present and verified. A software
microbenchmark is not evidence that PQC is universally faster than QKD. QBER is not execution
time; they are separate metrics and are not compared as if they were equivalent.

## Scope and limitations

- Experiment A simulates BB84 state preparation, optional intercept-resend, channel bit flips,
  basis sifting, QBER, sifted fraction, and an explicitly illustrative threshold status.
- Experiment B measures ML-KEM-768 key generation, encapsulation, and decapsulation separately.
  It verifies shared-secret equality and reports raw samples and summary statistics. It does not
  silently substitute Kyber or another algorithm.
- Experiment C is a qualitative, reference-led comparison. It does not invent cost, distance,
  throughput, or other deployment measurements.
- This project does not implement quantum hardware, authenticated channel protocols, error
  correction, privacy amplification, finite-key security proofs, or production key management.
  Real QKD requires an authenticated classical channel and further security processing.

See [docs/PROJECT_SCOPE.md](docs/PROJECT_SCOPE.md), [docs/EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md),
and [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) before interpreting results.

## Repository map

```text
configs/                  Validated experiment defaults
data/raw/                 Actual run CSVs (not committed)
data/processed/           Derived tables
data/example/             Clearly labelled illustrative material only
docs/                     Scope, protocol, interfaces, team, references
figures/                  Plots generated from actual CSV input
scripts/                  Experiment and analysis entry points
src/qkd_pqc/              Installable Python package
tests/                    Offline unit tests
```

The principal responsibilities are summarized in [docs/TEAM_ASSIGNMENTS.md](docs/TEAM_ASSIGNMENTS.md).

## Setup

Python 3.11 or later is required. From the repository root:

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

To add the optional PQC implementation:

```powershell
python -m pip install -e ".[mlkem,dev]"
```

If PowerShell blocks activation, either use `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
according to your organization's policy, or invoke `.venv\Scripts\python.exe` directly.

### Linux / macOS

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

To add the optional PQC implementation:

```sh
python -m pip install -e ".[mlkem,dev]"
```

The project needs no network access at test or experiment runtime once dependencies are installed.
Installation may require package access. `requirements.txt` lists the core runtime dependencies.

## Check ML-KEM-768 support

The adapter currently supports the `pqcrypto.kem.ml_kem_768` API. Check the optional package:

```powershell
python -c "from qkd_pqc.pqc.mlkem_benchmark import detect_mlkem_implementation; print(detect_mlkem_implementation())"
```

```sh
python -c 'from qkd_pqc.pqc.mlkem_benchmark import detect_mlkem_implementation; print(detect_mlkem_implementation())'
```

For OpenSSL, check its version and advertised KEM algorithms using `openssl version` and
`openssl list -kem-algorithms`. OpenSSL CLI support is not currently used by this project's timing
adapter: process startup and file I/O would contaminate operation timings unless a suitable
in-process API is available. Do not infer ML-KEM support merely from an OpenSSL version number.

## Run experiments and analysis

All commands below run from the repository root and use `configs/experiment_config.yaml` by
default. An alternate YAML configuration may be provided with `--config PATH`.

```powershell
python scripts/run_qkd.py
python scripts/run_pqc_benchmark.py
python scripts/run_analysis.py
python scripts/run_all.py
python -m pytest
```

Use the same commands in Linux/macOS shells. `run_pqc_benchmark.py` returns a nonzero exit code
when ML-KEM-768 is unavailable; the full pipeline reports that optional stage as skipped and
continues. `run_analysis.py` reports missing inputs and exits without fabricating any data.

Every run writes a uniquely named CSV under `data/raw/`; existing run files are never replaced.
Analysis writes figures under `figures/` and a qualitative/measured comparison table under
`data/processed/`. QKD CSV rows contain run-level outputs and enough input/seed metadata to
reproduce the simulation. ML-KEM CSV rows contain individual timed samples and repeated summary
statistics. Empty cells mean “not applicable or unavailable,” not zero.

## Stable Python interfaces

- `load_config(path=None) -> ExperimentConfig` loads and validates all experiment settings.
- `simulate_bb84(config: QKDConfig, seed: int | None = None) -> BB84Result` runs one reproducible
  educational BB84 simulation. `write_bb84_result(result, output_dir) -> Path` persists it.
- `detect_mlkem_implementation() -> MLKEMImplementation | None` checks the exact supported API.
- `run_mlkem_benchmark(config: PQCConfig, output_dir) -> BenchmarkResults` raises
  `MLKEMUnavailableError` if that implementation is missing or incompatible.
- `analyze_tradeoffs(qkd_metrics=None, pqc_metrics=None) -> list[TradeoffItem]` returns qualitative
  claims separately from measured values.
- `create_plots(qkd_csv=None, pqc_csv=None, figures_dir=..., processed_dir=...) -> list[Path]`
  validates actual input CSVs and creates only figures supported by their contents.

Configuration values and CSV fields are documented in
[docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md). The operation order and timing boundaries are
in [docs/EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md).

## Team assignments

1. Security model and literature
2. BB84 simulation
3. ML-KEM-768 benchmark
4. Infrastructure and system trade-offs
5. Integration, reproducibility, and visualization

Detailed ownership, acceptance criteria, and workstream interfaces are in
[docs/TEAM_ASSIGNMENTS.md](docs/TEAM_ASSIGNMENTS.md).

## Git collaboration

This initial directory may not yet be a Git repository. If so, review the new files and then
initialize it with:

```powershell
git init
git add .
git commit -m "Initialize QKD vs PQC research repository"
```

On Linux/macOS the same commands apply. Do not initialize over an existing repository; preserve
its history. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for branches, pull requests, data handling,
and review expectations.
