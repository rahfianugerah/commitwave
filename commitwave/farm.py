"""GitHub achievement badges: the tier table, the progress ledger, and the three runners."""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass

from commitwave import github
from commitwave.config import DATA_DIR, Settings

LEDGER = DATA_DIR / "progress.json"

# Write requests each unit costs. One pull request is a branch, a file, a pull request,
# a merge, and a branch deletion. One accepted answer is three GraphQL mutations.
WRITES_PER_PULL = 5
WRITES_PER_ANSWER = 3

Report = Callable[[int, str], None]


@dataclass(frozen=True)
class Tier:
    """One step of a badge, as GitHub grades it."""

    label: str
    grade: str
    target: int


@dataclass(frozen=True)
class Badge:
    key: str
    name: str
    unit: str
    tiers: tuple[Tier, ...]
    requires: tuple[str, ...]
    note: str

    def writes_per_unit(self) -> int:
        return WRITES_PER_ANSWER if self.key == "galaxy-brain" else WRITES_PER_PULL


BADGES: tuple[Badge, ...] = (
    Badge(
        key="pull-shark",
        name="Pull Shark",
        unit="merged pull requests",
        tiers=(
            Tier("Bronze", "x2", 16),
            Tier("Silver", "x3", 128),
            Tier("Gold", "x4", 1024),
        ),
        requires=("GITHUB_TOKEN", "GITHUB_REPO"),
        note="One account is enough. Each unit opens a pull request and merges it.",
    ),
    Badge(
        key="galaxy-brain",
        name="Galaxy Brain",
        unit="accepted answers",
        tiers=(
            Tier("Bronze", "x2", 8),
            Tier("Silver", "x3", 16),
            Tier("Gold", "x4", 32),
        ),
        requires=("GITHUB_TOKEN", "GITHUB_REPO", "SECONDARY_GITHUB_TOKEN"),
        note=(
            "Two GitHub accounts. The second account asks the question and marks your "
            "reply as the answer, because marking your own answer does not count."
        ),
    ),
    Badge(
        key="pair-extraordinaire",
        name="Pair Extraordinaire",
        unit="co-authored merged pull requests",
        tiers=(
            Tier("Bronze", "x2", 10),
            Tier("Silver", "x3", 24),
            Tier("Gold", "x4", 48),
        ),
        requires=("GITHUB_TOKEN", "GITHUB_REPO", "COAUTHOR_USERNAME"),
        note=(
            "Two GitHub accounts. The second one only has to exist. Its login becomes "
            "the Co-authored-by trailer and no token is read from it."
        ),
    ),
)

# Placeholder question and answer text. Edit this list to post real content instead.
# The unit index is appended to the title so no two discussions collide.
QA_TEMPLATES: tuple[tuple[str, str, str], ...] = (
    (
        "Lorem ipsum dolor sit amet, consectetur?",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
        "incididunt ut labore et dolore magna aliqua.",
        "Lorem ipsum dolor sit amet. Ut enim ad minim veniam, quis nostrud exercitation "
        "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    ),
    (
        "Quis nostrud exercitation ullamco laboris?",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
        "fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia "
        "deserunt mollit anim id est laborum.",
    ),
    (
        "Sed ut perspiciatis unde omnis iste natus?",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium "
        "doloremque laudantium, totam rem aperiam.",
        "Eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae "
        "dicta sunt explicabo.",
    ),
    (
        "Nemo enim ipsam voluptatem quia voluptas?",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed "
        "quia consequuntur magni dolores eos.",
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, "
        "adipisci velit, sed quia non numquam.",
    ),
    (
        "Ut enim ad minima veniam, quis nostrum?",
        "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit "
        "laboriosam, nisi ut aliquid ex ea commodi.",
        "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil "
        "molestiae consequatur.",
    ),
    (
        "At vero eos et accusamus et iusto odio?",
        "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis "
        "praesentium voluptatum deleniti atque corrupti.",
        "Et quas molestias excepturi sint occaecati cupiditate non provident, similique "
        "sunt in culpa qui officia deserunt.",
    ),
)


def find_badge(key: str) -> Badge:
    for badge in BADGES:
        if badge.key == key:
            return badge
    raise KeyError(f"No badge named {key}")


def template_for(index: int) -> tuple[str, str, str]:
    """Return a unique question and answer for unit `index`, cycling the template list."""
    title, question, answer = QA_TEMPLATES[index % len(QA_TEMPLATES)]
    return f"{title} ({index})", question, answer


def estimate_seconds(badge: Badge, units: int, delay: float) -> float:
    return units * badge.writes_per_unit() * delay


def load_ledger() -> dict[str, int]:
    if not LEDGER.exists():
        return {}
    try:
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    except ValueError:
        return {}


def ledger_count(badge: Badge) -> int:
    return load_ledger().get(badge.key, 0)


def current_count(badge: Badge, settings: Settings) -> int:
    """Count units already earned, asking GitHub wherever an exact query exists.

    Raises GitHubError when the live query fails, so the caller can say so rather than
    quietly showing a stale local number.
    """
    if badge.key == "pair-extraordinaire" or not settings.github_token:
        # GitHub exposes no co-author search qualifier, so the local ledger is all there is.
        return ledger_count(badge)

    login = github.whoami(settings.github_token)["login"]
    if badge.key == "pull-shark":
        return github.merged_pull_count(login, settings.github_token)
    return github.accepted_answer_count(login, settings.github_token)


def run(badge: Badge, units: int, settings: Settings, report: Report) -> int:
    """Create `units` of the badge's unit. Returns how many completed."""
    if badge.key == "galaxy-brain":
        return _run_answers(units, settings, report)

    coauthor = None
    if badge.key == "pair-extraordinaire":
        login = settings.coauthor_username
        coauthor = (login, github.noreply_email(login, settings.github_token))
    return _run_pulls(badge, units, settings, coauthor, report)


def _run_pulls(
    badge: Badge,
    units: int,
    settings: Settings,
    coauthor: tuple[str, str] | None,
    report: Report,
) -> int:
    """Open and merge one pull request per unit, carrying the head sha forward."""
    owner, name = settings.github_repo.split("/", 1)
    token = settings.github_token

    base = github.repository(owner, name, token)["default_branch"]
    head = github.branch_sha(owner, name, base, token)

    trailer = ""
    if coauthor is not None:
        # The blank line matters. A trailer glued to the subject is not a trailer.
        trailer = f"\n\nCo-authored-by: {coauthor[0]} <{coauthor[1]}>"

    pause = badge.writes_per_unit() * settings.request_delay
    done = 0

    for _ in range(units):
        tag = str(time.time_ns())
        branch = f"commitwave/{tag}"
        title = f"chore: commit wave unit {tag}"

        github.create_branch(owner, name, branch, head, token)
        github.commit_file(
            owner,
            name,
            branch,
            f"commitwave/{tag}.md",
            f"Commit Wave unit {tag}.\n",
            f"{title}{trailer}",
            token,
        )
        number = github.open_pull(owner, name, branch, base, title, token)
        # The trailer goes in the squash message too. A squash rewrites the message, and
        # GitHub deduplicates a repeated trailer, so writing it twice is the safe order.
        head = github.merge_pull(owner, name, number, title, trailer.strip(), token)
        github.delete_branch(owner, name, branch, token)

        done += 1
        _record(badge)
        report(done, f"merged pull request #{number}")
        if done < units:
            time.sleep(pause)

    return done


def _run_answers(units: int, settings: Settings, report: Report) -> int:
    """Second account asks, primary account answers, second account accepts."""
    owner, name = settings.github_repo.split("/", 1)
    primary = settings.github_token
    secondary = settings.secondary_github_token

    repo_id, category_id = github.discussion_target(owner, name, secondary)
    badge = find_badge("galaxy-brain")
    pause = badge.writes_per_unit() * settings.request_delay
    start = ledger_count(badge)
    done = 0

    for step in range(units):
        title, question, answer = template_for(start + step)

        discussion_id = github.create_discussion(repo_id, category_id, title, question, secondary)
        comment_id = github.add_comment(discussion_id, answer, primary)
        github.mark_answer(comment_id, secondary)

        done += 1
        _record(badge)
        report(done, f"accepted answer on '{title}'")
        if done < units:
            time.sleep(pause)

    return done


def _record(badge: Badge) -> None:
    """Write the ledger after every unit, so an interrupted run resumes where it stopped."""
    ledger = load_ledger()
    ledger[badge.key] = ledger.get(badge.key, 0) + 1
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")
