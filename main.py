"""Commit Wave entrypoint. Run it with `python main.py`."""

from __future__ import annotations

from commitwave import farm, git, tui, wave
from commitwave.config import ConfigError, Settings, load_settings
from commitwave.farm import Badge, Tier
from commitwave.github import GitHubError

MENU = [
    "Contribution Wave, backdated commits across a date range",
    "Badge Farm, work towards a GitHub achievement",
    "Status, what each badge stands at",
    "Quit",
]


def main() -> None:
    tui.banner()
    try:
        settings = load_settings()
    except ConfigError as error:
        tui.say(f"Configuration problem: {error}")
        return

    tui.say("Hello. I am your commit bot.")
    while True:
        choice = tui.menu("What would you like to do?", MENU)
        if choice == 0:
            contribution_wave()
        elif choice == 1:
            badge_farm(settings)
        elif choice == 2:
            status(settings)
        else:
            tui.say("Goodbye.")
            return


def contribution_wave() -> None:
    """Ask for a date range and a count, then make that many backdated commits."""
    try:
        start, end = wave.parse_range(
            tui.ask("Please enter the start date (YYYY-MM-DD):"),
            tui.ask("Please enter the end date (YYYY-MM-DD):"),
        )
        count = _positive_int(tui.ask("How many commits would you like to make?"))
        moments = wave.random_dates(start, end, count)
    except ValueError as error:
        tui.say(str(error))
        return

    tui.say(f"Making {count} commits. This repository is the one that receives them.")
    try:
        wave.run_wave(moments, lambda done, stamp: tui.progress(done, count, stamp))
    except git.GitError as error:
        tui.say(f"Git stopped: {error}")
        return
    tui.say("All commits are done and pushed to the remote.")


def badge_farm(settings: Settings) -> None:
    """Pick a badge and a tier, check what is missing, then run to the target."""
    badge = farm.BADGES[tui.menu("Which badge?", [_badge_line(b) for b in farm.BADGES])]
    tui.say(badge.note)

    tier = badge.tiers[tui.menu("Which tier?", [_tier_line(badge, t) for t in badge.tiers])]

    missing = settings.missing(badge.requires)
    if missing:
        _explain(badge, missing)
        return

    try:
        current = farm.current_count(badge, settings)
    except GitHubError as error:
        tui.say(f"Could not read your current count: {error.message}")
        return

    units = tier.target - current
    if units <= 0:
        tui.say(f"You already stand at {current} {badge.unit}. {tier.label} needs {tier.target}.")
        return

    minutes = farm.estimate_seconds(badge, units, settings.request_delay) / 60
    tui.say(
        f"You stand at {current} of {tier.target}. Reaching {badge.name} {tier.grade} "
        f"{tier.label} means creating {units} more {badge.unit} in {settings.github_repo}, "
        f"which takes about {minutes:.0f} minutes at the current request delay."
    )
    if not tui.confirm("This writes to that repository and cannot be undone in bulk."):
        tui.say("Nothing was created.")
        return

    _run(badge, units, settings)


def status(settings: Settings) -> None:
    """Show where each badge stands against its three tiers."""
    tui.say(f"Target repository: {settings.github_repo or 'not set'}")
    for badge in farm.BADGES:
        source = "local ledger"
        try:
            count = farm.current_count(badge, settings)
            if badge.key != "pair-extraordinaire" and settings.github_token:
                source = "GitHub"
        except GitHubError as error:
            count = farm.ledger_count(badge)
            source = f"local ledger, GitHub said: {error.message}"

        tui.tell(f"  {badge.name}: {count} {badge.unit} ({source})")
        for tier in badge.tiers:
            state = "earned" if count >= tier.target else f"{tier.target - count} to go"
            tui.tell(f"    {tier.grade} {tier.label:<7} {tier.target:>5}  {state}")
    tui.tell()
    tui.say(
        "GitHub publishes no achievements API, so nothing here reads the badge itself. "
        "Check your profile after a day or two."
    )


def _run(badge: Badge, units: int, settings: Settings) -> None:
    # The ledger is written after every unit, so its movement is how far the run got.
    before = farm.ledger_count(badge)
    try:
        done = farm.run(badge, units, settings, lambda n, label: tui.progress(n, units, label))
    except GitHubError as error:
        tui.tell()
        tui.say(f"Stopped after {farm.ledger_count(badge) - before} of {units}: {error.message}")
        tui.say("Run this again to carry on from where it stopped.")
        return
    except KeyboardInterrupt:
        tui.tell()
        tui.say(f"Stopped after {farm.ledger_count(badge) - before} of {units}, on request.")
        return

    tui.say(
        f"Created {done} {badge.unit}. GitHub awards achievements on its own schedule, "
        "so give your profile a day or two."
    )


def _explain(badge: Badge, missing: list[str]) -> None:
    tui.say(f"{badge.name} needs settings this project does not have yet.")
    tui.tell(f"  Missing in .env: {', '.join(missing)}")
    tui.tell("  Copy .env.example to .env and fill those names in.")
    if "SECONDARY_GITHUB_TOKEN" in missing:
        tui.tell("  SECONDARY_GITHUB_TOKEN is a token from a different GitHub account.")
    if "COAUTHOR_USERNAME" in missing:
        tui.tell("  COAUTHOR_USERNAME is the login of a different GitHub account.")


def _badge_line(badge: Badge) -> str:
    targets = ", ".join(f"{tier.label} {tier.target}" for tier in badge.tiers)
    return f"{badge.name:<20} {badge.unit} ({targets})"


def _tier_line(badge: Badge, tier: Tier) -> str:
    return f"{tier.grade} {tier.label:<7} {tier.target} {badge.unit}"


def _positive_int(text: str) -> int:
    if not text.isdigit() or int(text) <= 0:
        raise ValueError("Please enter a valid positive number for commits")
    return int(text)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # EOFError is Ctrl+D, or stdin running out when the app is driven by a pipe.
        tui.tell()
        tui.say("Goodbye.")
