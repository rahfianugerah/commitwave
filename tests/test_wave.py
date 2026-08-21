"""Date generation, the part of the wave that is not a git call."""

from datetime import datetime, timezone

import pytest

from commitwave.wave import format_date, parse_range, random_dates


def test_format_date_matches_the_form_git_accepts():
    moment = datetime(2024, 9, 18, 21, 55, 0, tzinfo=timezone.utc)
    assert format_date(moment) == "Wed Sep 18 21:55:00 UTC 2024"


def test_format_date_pads_a_single_digit_day():
    moment = datetime(2025, 1, 5, 3, 7, 9, tzinfo=timezone.utc)
    assert format_date(moment) == "Sun Jan 05 03:07:09 UTC 2025"


def test_parse_range_covers_the_whole_end_day():
    start, end = parse_range("2025-08-01", "2025-08-02")
    assert start == datetime(2025, 8, 1, tzinfo=timezone.utc)
    assert end == datetime(2025, 8, 3, tzinfo=timezone.utc)


def test_parse_range_accepts_a_single_day():
    start, end = parse_range("2025-08-01", "2025-08-01")
    assert (end - start).total_seconds() == 86400


def test_parse_range_rejects_a_backwards_range():
    with pytest.raises(ValueError, match="not be earlier"):
        parse_range("2025-08-05", "2025-08-01")


def test_parse_range_rejects_a_malformed_date():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        parse_range("01-08-2025", "2025-08-02")


def test_random_dates_stay_inside_the_range_and_are_distinct():
    start, end = parse_range("2025-08-01", "2025-08-03")
    moments = random_dates(start, end, 50)

    assert len(moments) == 50
    assert len(set(moments)) == 50
    assert moments == sorted(moments)
    assert all(start <= moment < end for moment in moments)


def test_random_dates_rejects_a_count_the_range_cannot_hold():
    start, end = parse_range("2025-08-01", "2025-08-01")
    with pytest.raises(ValueError, match="distinct commits"):
        random_dates(start, end, 86401)


def test_random_dates_rejects_a_non_positive_count():
    start, end = parse_range("2025-08-01", "2025-08-02")
    with pytest.raises(ValueError, match="positive number"):
        random_dates(start, end, 0)
