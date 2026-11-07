
import pandas as pd

from f1_race_intelligence.performance.stint_analysis import (
    count_stints_by_compound,
    count_stints_by_driver_and_compound,
)


# Small dataset with known results
stints = pd.DataFrame({
    "driver_number": [1, 1, 3, 3, 3, 16],
    "compound": [
        "SOFT",
        "MEDIUM",
        "SOFT",
        "SOFT",
        "HARD",
        "HARD",
    ],
})


def test_count_stints_by_compound():
    result = count_stints_by_compound(stints)

    expected = {
        "SOFT": 3,
        "HARD": 2,
        "MEDIUM": 1,
    }

    assert result.to_dict() == expected


def test_count_stints_by_driver_and_compound():
    result = count_stints_by_driver_and_compound(stints)

    assert result.loc[1, "SOFT"] == 1
    assert result.loc[3, "SOFT"] == 2
    assert result.loc[3, "HARD"] == 1
    assert result.loc[16, "HARD"] == 1
