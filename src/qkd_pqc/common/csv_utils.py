"""CSV writing helpers with a no-overwrite policy."""

import csv
from io import StringIO
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


def write_csv_exclusive(
    path: str | Path,
    fieldnames: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
) -> Path:
    """Write CSV rows without replacing an existing file."""
    destination = Path(path)
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="raise")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", newline="", encoding="utf-8") as stream:
        stream.write(buffer.getvalue())
    return destination
