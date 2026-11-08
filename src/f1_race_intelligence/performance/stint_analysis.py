import pandas as pd


def count_stints_by_compound(stints: pd.DataFrame) -> pd.Series:
    """
    Count the number of stints for each tyre compound.
    """

    compounds = stints["compound"].value_counts()

    return compounds

def count_stints_by_driver_and_compound(stints: pd.DataFrame) -> pd.DataFrame:

    drivers = pd.crosstab(stints["driver_number"], stints["compound"])

    return drivers

def add_team_to_stints(stints: pd.DataFrame,drivers: pd.DataFrame) -> pd.DataFrame:

    teams = stints.merge(drivers, on = "driver_number", how = "left")
    
    return teams


def count_stints_by_team_and_compound(stints: pd.DataFrame) -> pd.DataFrame:

    teams_compound = pd.crosstab(stints["team_name"], stints["compound"])

    return teams_compound

def calculate_stint_length(stints: pd.DataFrame) -> pd.DataFrame:

    stints_copy = stints.copy()

    start = stints_copy["lap_start"]
    end = stints_copy["lap_end"]

    stints_copy["stint_length"] = end-start + 1

    
    return stints_copy


def calculate_team_test_laps(stints: pd.DataFrame) -> pd.Series:

    test_laps = stints.groupby("team_name")["stint_length"].sum()
    return test_laps

