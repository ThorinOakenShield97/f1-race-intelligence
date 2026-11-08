
import pandas as pd

from f1_race_intelligence.performance.stint_analysis import (
    count_stints_by_compound,
    count_stints_by_driver_and_compound,
    calculate_stint_length,
    calculate_team_test_laps
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


from f1_race_intelligence.performance.stint_analysis import (
    add_team_to_stints,
)


def test_add_team_to_stints():

    stints = pd.DataFrame({
        "driver_number": [1, 1, 3, 16],
        "compound": ["SOFT", "MEDIUM", "HARD", "SOFT"],
    })

    drivers = pd.DataFrame({
        "driver_number": [1, 3, 16],
        "team_name": ["McLaren", "Red Bull Racing", "Ferrari"],
    })

    result = add_team_to_stints(stints, drivers)

    assert len(result) == 4
    assert "team_name" in result.columns
    assert result["team_name"].notna().all()

    assert result.loc[0, "team_name"] == "McLaren"
    assert result.loc[2, "team_name"] == "Red Bull Racing"
    assert result.loc[3, "team_name"] == "Ferrari"

def test_count_stints_by_team_and_compound():

    from f1_race_intelligence.performance.stint_analysis import (
        count_stints_by_team_and_compound,
    )

    data = pd.DataFrame({
        "team_name": [
            "McLaren", "McLaren", "Ferrari",
            "Ferrari", "Red Bull Racing"
        ],
        "compound": [
            "SOFT", "MEDIUM", "SOFT",
            "SOFT", "HARD"
        ],
    })

    result = count_stints_by_team_and_compound(data)

    assert result.loc["McLaren", "SOFT"] == 1
    assert result.loc["McLaren", "MEDIUM"] == 1
    assert result.loc["Ferrari", "SOFT"] == 2
    assert result.loc["Red Bull Racing", "HARD"] == 1
    assert result.to_numpy().sum() == 5


def test_calculate_stint_length():

    data = pd.DataFrame({
        "lap_start": [1, 5, 16],
        "lap_end": [4, 15, 20],
    })

    result = calculate_stint_length(data)

    expected = [4, 11, 5]

    assert result["stint_length"].tolist() == expected
    assert isinstance(result, pd.DataFrame)

def test_calculate_team_test_laps():

    data = pd.DataFrame({
        "team_name": ["McLaren", "McLaren", "Ferrari", "Ferrari"],
        "stint_length": [5, 10, 8, 12],
    })

    result = calculate_team_test_laps(data)

    assert result["McLaren"] == 15
    assert result["Ferrari"] == 20
    assert result.sum() == 35