"""Git commands, run as an argument list so no value is ever parsed by a shell."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """A git command exited non-zero."""


def add(path: Path) -> None:
    """Stage one path, forcing it past .gitignore because data/ is otherwise ignored."""
    _run(["add", "-f", str(path)])


def commit(message: str, date: str) -> None:
    """Commit the staged changes with both the author and committer date set to `date`."""
    # --date sets the author date only. Without GIT_COMMITTER_DATE, git log shows a
    # backdated commit next to today's committer date, which reads as tampering.
    environment = os.environ.copy()
    environment["GIT_COMMITTER_DATE"] = date
    _run(["commit", "-m", message, "--date", date], environment)


def push() -> str:
    return _run(["push"])


def _run(arguments: list[str], environment: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", *arguments],
        capture_output=True,
        text=True,
        env=environment,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise GitError(detail or f"git {arguments[0]} failed")
    return result.stdout.strip()
