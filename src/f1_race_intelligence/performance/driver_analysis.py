import pandas as pd


def summarize_driver_performance(
    laps: pd.DataFrame,
    drivers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate preliminary performance statistics by driver.

    Pit-out laps are excluded from candidate best-lap calculations.
    All original records are preserved.
    """

    laps = laps.copy()

    # Candidate lap times:
    # timed laps that are not marked as pit-out laps
    laps["candidate_lap"] = (
        laps["lap_duration"].notna()
        & ~laps["is_pit_out_lap"].fillna(False)
    )

    laps["candidate_lap_time"] = laps[
        "lap_duration"
    ].where(laps["candidate_lap"])

    # Aggregate lap statistics by driver
    summary = (
        laps.groupby("driver_number")
        .agg(
            recorded_laps=("lap_number", "size"),
            timed_laps=("has_lap_time", "sum"),
            complete_sector_laps=("has_complete_sectors", "sum"),
            candidate_laps=("candidate_lap", "sum"),
            best_lap_s=("candidate_lap_time", "min"),
        )
        .reset_index()
    )

    # Attach driver and team information
    driver_info = drivers[
        [
            "driver_number",
            "name_acronym",
            "full_name",
            "team_name",
        ]
    ].drop_duplicates(subset="driver_number")

    summary = driver_info.merge(
        summary,
        on="driver_number",
        how="left",
        validate="one_to_one",
    )

    # Identify drivers without recorded lap data
    summary["has_lap_data"] = summary["recorded_laps"].notna()

    # Convert missing lap counts into zero
    count_columns = [
    "recorded_laps",
    "timed_laps",
    "complete_sector_laps",
    "candidate_laps",
    ]

    for column in count_columns:
        summary[column] = (
        summary[column]
        .fillna(0)
        .astype("int64")
        )

    # Sort by preliminary best lap
    summary = summary.sort_values(
        "best_lap_s",
        ascending=True,
        na_position="last",
    )

    return summary.reset_index(drop=True)
