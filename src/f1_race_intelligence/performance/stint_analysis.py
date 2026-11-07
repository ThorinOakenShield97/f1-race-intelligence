import pandas as pd


def count_stints_by_compound(stints: pd.DataFrame) -> pd.Series:
    """
    Count the number of stints for each tyre compound.
    """

    compounds = stints["compound"].value_counts()

    return compounds

def count_stints_by_driver_and_compound(stints: pd.DataFrame) -> pd.DataFrame:

    driver_stints = pd.crosstab(stints["driver_number"], stints["compound"])

    return driver_stints