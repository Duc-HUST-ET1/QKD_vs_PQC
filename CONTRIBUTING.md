# Contributing

## Work areas and branches

Start work independently in the assigned area and use a focused branch, for example:

- `feature/bb84-simulator`
- `feature/mlkem-benchmark`
- `feature/system-analysis`
- `feature/integration`
- `docs/security-model`

Do not directly edit another member's principal deliverable without coordinating with its owner.
When interfaces or shared files need a change, open a pull request and describe the impact.

## Pull requests

Each pull request should explain its purpose, list changed interfaces, state assumptions and
limitations, identify the tests run, and link relevant references. Do not report unrun checks as
passing. Keep experiment inputs and implementation versions traceable in committed documentation
or the generated run metadata.

## Local setup and checks

Use Python 3.11 or later and an isolated virtual environment. Install the project and development
dependencies with `python -m pip install -e ".[dev]"`, then run `python -m pytest`. Install the
optional ML-KEM dependency only when working on or running that benchmark:
`python -m pip install -e ".[mlkem,dev]"`.

## Data and security

Never commit virtual environments, private keys, credentials, `.env` files, generated raw
measurements, or large generated artifacts. Keep illustrative material in `data/example/` and
actual experiment outputs in `data/raw/`. Do not overwrite a raw run; the tools create uniquely
named run files. Report assumptions, seed, configuration, platform, implementation, and software
version with results. Never put real secret keys or shared-secret values in experiment output.
