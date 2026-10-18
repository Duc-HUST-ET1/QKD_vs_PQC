"""Run and environment metadata."""

from datetime import datetime, timezone
import platform
import sys
from uuid import uuid4


def create_run_id(prefix: str) -> tuple[str, str]:
    """Return a unique run identifier and its UTC creation timestamp."""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat(timespec="microseconds")
    stamp = now.strftime("%Y%m%dT%H%M%S")
    return f"{prefix}_{stamp}_{uuid4().hex[:8]}", timestamp


def runtime_metadata() -> dict[str, str]:
    """Return non-secret runtime details for experiment provenance."""
    return {"python_version": platform.python_version(), "platform": platform.platform()}
