import csv

import pytest

from qkd_pqc.common.csv_utils import write_csv_exclusive
from qkd_pqc.config import QKDConfig
from qkd_pqc.qkd.bb84_simulator import BB84_CSV_FIELDS, simulate_bb84, write_bb84_result


def test_bb84_csv_contains_documented_headers(tmp_path):
    result = simulate_bb84(QKDConfig(20, 0.01, 0.0, 0.11), seed=42)
    output = write_bb84_result(result, tmp_path)

    with output.open("r", newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert tuple(reader.fieldnames or ()) == BB84_CSV_FIELDS
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["seed"] == "42"
    assert rows[0]["sifted_bits"] == str(result.sifted_bits)
    assert rows[0]["qber"] == str(result.qber)


def test_csv_writer_never_overwrites_existing_file(tmp_path):
    output = tmp_path / "run.csv"
    output.write_text("original\n", encoding="utf-8")

    with pytest.raises(FileExistsError):
        write_csv_exclusive(output, ("value",), [{"value": 1}])

    assert output.read_text(encoding="utf-8") == "original\n"
