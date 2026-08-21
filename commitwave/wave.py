"""The contribution wave: backdated commits spread across a date range."""

from __future__ import annotations

import random
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from commitwave import git
from commitwave.config import DATA_DIR

TEMP_FILE = DATA_DIR / "temp.txt"
LOG_FILE = DATA_DIR / "commit.txt"

_DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def format_date(moment: datetime) -> str:
    """Format as `Wed Sep 18 21:55:00 UTC 2024`, the form git accepts for --date."""
    utc = moment.astimezone(UTC)
    return (
        f"{_DAYS[utc.weekday()]} {_MONTHS[utc.month - 1]} {utc.day:02d} "
        f"{utc.hour:02d}:{utc.minute:02d}:{utc.second:02d} UTC {utc.year}"
    )


def parse_range(start_text: str, end_text: str) -> tuple[datetime, datetime]:
    """Parse two YYYY-MM-DD strings into a half-open range that covers both days."""
    start = _parse_day(start_text)
    end = _parse_day(end_text)
    if end < start:
        raise ValueError("The end date must not be earlier than the start date")
    # The end date is inclusive to a reader, so the range runs to the end of that day.
    return start, end + timedelta(days=1)


def random_dates(start: datetime, end: datetime, count: int) -> list[datetime]:
    """Pick `count` distinct second-resolution timestamps inside a half-open range."""
    if count <= 0:
        raise ValueError("The commit count must be a positive number")

    span = int((end - start).total_seconds())
    if span < count:
        raise ValueError(
            f"That range holds {span} seconds, which cannot carry {count} distinct commits"
        )

    # Distinct on purpose. Two commits with the same second write the same file
    # content, and the second one fails with "nothing to commit".
    offsets = random.sample(range(span), count)
    return sorted(start + timedelta(seconds=offset) for offset in offsets)


def run_wave(moments: list[datetime], on_commit: Callable[[int, str], None]) -> None:
    """Make one backdated commit per moment, then push once at the end."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for index, moment in enumerate(moments, start=1):
        stamp = format_date(moment)
        TEMP_FILE.write_text(f"{stamp}\n", encoding="utf-8")
        with LOG_FILE.open("a", encoding="utf-8") as log:
            log.write(f"{stamp}\n")

        git.add(TEMP_FILE)
        git.commit(stamp, stamp)
        on_commit(index, stamp)

    git.push()


def _parse_day(text: str) -> datetime:
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError as error:
        raise ValueError(f"'{text.strip()}' is not a date in YYYY-MM-DD form") from error
