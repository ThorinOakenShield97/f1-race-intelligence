from pathlib import Path

import fastf1
from fastf1.core import Session


# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[3]
CACHE_DIR = PROJECT_ROOT / "data" / "cache"

# Create cache directory if it does not exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Configure FastF1 cache
fastf1.Cache.configure(cache_dir=str(CACHE_DIR))


def load_session(
    year: int,
    grand_prix: str,
    session_type: str = "Q",
    *,
    telemetry: bool = False,
    weather: bool = False,
    messages: bool = False,
) -> Session:
    """
    Load a Formula 1 session using FastF1.

    Parameters
    ----------
    year : int
        Championship season.

    grand_prix : str
        Grand Prix name, e.g. 'Bahrain'.

    session_type : str
        Session identifier:
        Q = Qualifying
        R = Race
        FP1, FP2, FP3 = Practice

    telemetry : bool
        Whether to load car telemetry.

    weather : bool
        Whether to load weather data.

    messages : bool
        Whether to load race control messages.

    Returns
    -------
    Session
        Loaded FastF1 session.
    """

    session = fastf1.get_session(
        year,
        grand_prix,
        session_type
    )

    session.load(
        laps=True,
        telemetry=telemetry,
        weather=weather,
        messages=messages
    )

    return session
