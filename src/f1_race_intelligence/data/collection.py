import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from f1_race_intelligence.data.providers.openf1 import (
    get_laps,
    get_stints,
    get_drivers,
    get_weather,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "openf1"


def save_json(
    data: list[dict[str, Any]],
    filepath: Path,
) -> None:
    """
    Save raw API records as a JSON file.

    The temporary file prevents leaving a partially
    written JSON file if the operation fails.
    """

    filepath.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = filepath.with_suffix(".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    temporary_path.replace(filepath)


def collect_session_data(
    session_key: int,
    year: int,
    event_name: str,
    session_name: str,
) -> Path:
    """
    Download and store the raw datasets of an F1 session.

    Returns
    -------
    Path
        Directory containing the downloaded datasets.
    """

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    if year < 1950:
        raise ValueError("Invalid championship year.")

    # Retrieve datasets
    datasets = {
        "laps": get_laps(session_key),
        "stints": get_stints(session_key),
        "drivers": get_drivers(session_key),
        "weather": get_weather(session_key),
    }

    # Create session directory
    output_dir = RAW_DATA_DIR / str(year) / f"session_{session_key}"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Save raw datasets
    for name, records in datasets.items():
        save_json(
            records,
            output_dir / f"{name}.json",
        )

    # Create collection metadata
    metadata = {
        "source": "OpenF1",
        "session_key": session_key,
        "year": year,
        "event_name": event_name,
        "session_name": session_name,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "record_counts": {
            name: len(records)
            for name, records in datasets.items()
        },
    }

    metadata_path = output_dir / "metadata.json"

    temporary_path = metadata_path.with_suffix(".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)

    temporary_path.replace(metadata_path)

    return output_dir
