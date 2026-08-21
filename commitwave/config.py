"""Settings, read once at startup. No other module touches the environment."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EXAMPLE_ENV = ROOT / ".env.example"

# GitHub allows about 500 content-generating requests per hour. One pull request
# costs four of them, so 8 seconds between writes sits just under the ceiling.
DEFAULT_DELAY = 8.0

_REMOTE = re.compile(r"github\.com[:/](?P<owner>[^/]+)/(?P<name>[^/]+?)(?:\.git)?/?$")


class ConfigError(RuntimeError):
    """A required setting is missing or unusable."""


@dataclass(frozen=True)
class Settings:
    """Every value the app reads from the environment."""

    github_token: str | None
    github_repo: str | None
    secondary_github_token: str | None
    coauthor_username: str | None
    request_delay: float

    def missing(self, names: tuple[str, ...]) -> list[str]:
        """Return the variable names in `names` that hold no usable value."""
        return [name for name in names if not getattr(self, name.lower(), None)]


def load_settings() -> Settings:
    """Read `.env` and the process environment into one frozen Settings object."""
    load_dotenv(ROOT / ".env")
    placeholders = _placeholder_values()

    return Settings(
        github_token=_value("GITHUB_TOKEN", placeholders),
        github_repo=_value("GITHUB_REPO", placeholders) or _repo_from_remote(),
        secondary_github_token=_value("SECONDARY_GITHUB_TOKEN", placeholders),
        coauthor_username=_value("COAUTHOR_USERNAME", placeholders),
        request_delay=_delay(_value("REQUEST_DELAY", placeholders)),
    )


def _value(name: str, placeholders: set[str]) -> str | None:
    """Return the variable's value, or None when it is unset or still a placeholder."""
    raw = os.environ.get(name, "").strip()
    if not raw or raw in placeholders:
        return None
    return raw


def _placeholder_values() -> set[str]:
    """Read the example file so a copied placeholder counts as unset in one place only."""
    if not EXAMPLE_ENV.exists():
        return set()
    values = set()
    for line in EXAMPLE_ENV.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        values.add(stripped.split("=", 1)[1].strip())
    return values


def _delay(raw: str | None) -> float:
    if raw is None:
        return DEFAULT_DELAY
    try:
        return max(0.0, float(raw))
    except ValueError as error:
        raise ConfigError("REQUEST_DELAY must be a number of seconds") from error


def _repo_from_remote() -> str | None:
    """Fall back to the owner/name of the `origin` remote of the current directory."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return parse_remote(result.stdout.strip())


def parse_remote(url: str) -> str | None:
    """Turn a GitHub remote URL into `owner/name`, or None when it is not GitHub."""
    match = _REMOTE.search(url.strip())
    if match is None:
        return None
    return f"{match['owner']}/{match['name']}"
