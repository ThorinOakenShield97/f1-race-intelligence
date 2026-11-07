
from typing import Any

import httpx


BASE_URL = "https://api.openf1.org/v1"
DEFAULT_TIMEOUT = 20.0


class OpenF1APIError(RuntimeError):
    """Raised when an OpenF1 API request fails."""


def _get(
    endpoint: str,
    params: dict[str, int | str]
) -> list[dict[str, Any]]:
    """
    Perform a GET request to the OpenF1 API.

    Parameters
    ----------
    endpoint : str
        API endpoint.

    params : dict
        Query parameters.

    Returns
    -------
    list[dict]
        JSON records returned by the API.
    """

    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=DEFAULT_TIMEOUT
        )

        response.raise_for_status()

    except httpx.TimeoutException as exc:
        raise OpenF1APIError(
            f"Request to {endpoint} timed out."
        ) from exc

    except httpx.HTTPStatusError as exc:
        raise OpenF1APIError(
            f"OpenF1 returned HTTP "
            f"{exc.response.status_code} for {endpoint}."
        ) from exc

    except httpx.RequestError as exc:
        raise OpenF1APIError(
            f"Could not connect to OpenF1: {exc}"
        ) from exc

    try:
        data = response.json()

    except ValueError as exc:
        raise OpenF1APIError(
            f"Invalid JSON response from {endpoint}."
        ) from exc

    if not isinstance(data, list):
        raise OpenF1APIError(
            f"Unexpected response format from {endpoint}."
        )

    if not all(isinstance(record, dict) for record in data):
        raise OpenF1APIError(
            f"Unexpected record format from {endpoint}."
        )

    return data


def get_sessions(
    year: int,
    session_name: str = "Qualifying",
    country_name: str | None = None
) -> list[dict[str, Any]]:
    """Retrieve sessions for a given season."""

    if year < 1950:
        raise ValueError("The year must be 1950 or later.")

    params: dict[str, int | str] = {
        "year": year,
        "session_name": session_name
    }

    if country_name:
        params["country_name"] = country_name

    return _get("sessions", params)


def get_laps(
    session_key: int
) -> list[dict[str, Any]]:
    """Retrieve lap timing data for a session."""

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    return _get(
        "laps",
        {"session_key": session_key}
    )


def get_session_results(
    session_key: int
) -> list[dict[str, Any]]:
    """Retrieve final session results."""

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    return _get(
        "session_result",
        {"session_key": session_key}
    )


def get_stints(
    session_key: int
) -> list[dict[str, Any]]:
    """Retrieve tyre stint information."""

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    return _get(
        "stints",
        {"session_key": session_key}
    )


def get_drivers(
    session_key: int
) -> list[dict[str, Any]]:
    """Retrieve driver and team information."""

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    return _get(
        "drivers",
        {"session_key": session_key}
    )


def get_weather(
    session_key: int
) -> list[dict[str, Any]]:
    """Retrieve weather observations for a session."""

    if session_key <= 0:
        raise ValueError("session_key must be positive.")

    return _get(
        "weather",
        {"session_key": session_key}
    )
