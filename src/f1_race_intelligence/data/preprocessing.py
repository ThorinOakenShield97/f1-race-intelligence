import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "openf1"


def load_session_data(
    session_key: int,
    year: int,
) -> dict[str, pd.DataFrame]:
    """
    Load raw session datasets into Pandas DataFrames.

    Parameters
    ----------
    session_key : int
        OpenF1 session identifier.

    year : int
        Championship season.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing session datasets.
    """

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    session_dir = RAW_DATA_DIR / str(year) / f"session_{session_key}"

    if not session_dir.is_dir():
        raise FileNotFoundError(
            f"Session directory not found: {session_dir}"
        )

    datasets = {}

    for name in ["laps", "stints", "drivers", "weather"]:

        filepath = session_dir / f"{name}.json"

        if not filepath.is_file():
            raise FileNotFoundError(
                f"Dataset not found: {filepath}"
            )

        with filepath.open(encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(
                f"Expected a list of records in {filepath}"
            )

        datasets[name] = pd.DataFrame.from_records(records)

    return datasets


def prepare_laps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare lap timing data for statistical analysis.

    Preserves original records and does not remove missing values.
    """

    df = df.copy()

    numeric_columns = [
        "driver_number",
        "lap_number",
        "lap_duration",
        "duration_sector_1",
        "duration_sector_2",
        "duration_sector_3",
        "i1_speed",
        "i2_speed",
        "st_speed",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "date_start" in df.columns:
        df["date_start"] = pd.to_datetime(
            df["date_start"],
            errors="coerce",
            utc=True
        )

    if "is_pit_out_lap" in df.columns:
        df["is_pit_out_lap"] = df["is_pit_out_lap"].astype(
            "boolean"
        )

    # Data quality indicators
    df["has_lap_time"] = df["lap_duration"].notna()

    sector_columns = [
        "duration_sector_1",
        "duration_sector_2",
        "duration_sector_3",
    ]

    df["has_complete_sectors"] = (
        df[sector_columns].notna().all(axis=1)
    )

    return df
