"""
Test file for the weather station functions - Template

Copy this file to `test_weather.py` and replace every TODO with your own tests.
Keep `weather.py` in the same folder so the import below works.
"""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_kz2635 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (-273.15, -459.67),
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Check the conversion for freezing, boiling, -40, body temperature and absolute zero."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


# TODO: add @pytest.mark.parametrize with at least 4 (bad_input, expected_error) cases.
@pytest.mark.parametrize("bad_input, expected_error", [
    ("hot", TypeError),
    (None, TypeError),
    (-273.16, ValueError),
    (True, TypeError),
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check that invalid inputs raise the documented errors."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Check mean, min, max and n_missing for a list that contains one NaN."""
    # Arrange
    temps = [10.0, float("nan"), 20.0, 30.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert result["mean"] == pytest.approx(20.0)
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Raw station readings with one NaN, one sensor error (999.0) and unsorted rows."""
    return pd.DataFrame({
    "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
    "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
    "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
})

def test_raw_readings_fixture(raw_readings):
    """Check the columns, the number of rows and the number of missing values."""
    assert list(raw_readings.columns) == list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1



# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Check that clean_readings drops bad rows, adds temp_f and sorts the result."""

    expected = pd.DataFrame(
    [
        ("CPK", "2026-07-01", 25.0, 77.0),
        ("JFK", "2026-07-02", 30.0, 86.0),
        ("LGA", "2026-07-01", 28.0, 82.4),
    ],
    columns=["station", "date", "temp_c", "temp_f"],
)


    result = clean_readings(raw_readings)


    assert_frame_equal(result, expected)

