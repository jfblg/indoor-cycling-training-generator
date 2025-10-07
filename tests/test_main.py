import pytest
from indoor_cycling_training_generator.main import time_to_milliseconds

@pytest.mark.parametrize("time_str, expected_ms", [
    ("00:01", 1000),
    ("01:00", 60000),
    ("10:30", 630000),
    ("00:00", 0),
])
def test_time_to_milliseconds(time_str, expected_ms):
    assert time_to_milliseconds(time_str) == expected_ms

def test_time_to_milliseconds_invalid_format():
    """Tests that invalid time formats return None."""
    assert time_to_milliseconds("1:2:3") is None
    assert time_to_milliseconds("abc") is None
    assert time_to_milliseconds("10:") is None
