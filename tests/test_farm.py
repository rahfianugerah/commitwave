"""The badge table, the settings check, and the arithmetic the confirmation screen shows."""

import pytest

from commitwave.config import Settings, parse_remote
from commitwave.farm import BADGES, QA_TEMPLATES, estimate_seconds, find_badge, template_for


def _settings(**overrides) -> Settings:
    values = {
        "github_token": "token",
        "github_repo": "owner/name",
        "secondary_github_token": None,
        "coauthor_username": None,
        "request_delay": 8.0,
    }
    return Settings(**{**values, **overrides})


def test_every_badge_has_the_three_documented_tiers():
    for badge in BADGES:
        assert [tier.label for tier in badge.tiers] == ["Bronze", "Silver", "Gold"]
        assert [tier.grade for tier in badge.tiers] == ["x2", "x3", "x4"]


def test_the_tier_targets_match_github():
    targets = {badge.key: [tier.target for tier in badge.tiers] for badge in BADGES}
    assert targets == {
        "pull-shark": [16, 128, 1024],
        "galaxy-brain": [8, 16, 32],
        "pair-extraordinaire": [10, 24, 48],
    }


def test_find_badge_rejects_an_unknown_key():
    with pytest.raises(KeyError):
        find_badge("quickdraw")


def test_pull_shark_needs_nothing_beyond_a_token_and_a_repository():
    assert _settings().missing(find_badge("pull-shark").requires) == []


def test_galaxy_brain_reports_the_second_account_token_as_missing():
    missing = _settings().missing(find_badge("galaxy-brain").requires)
    assert missing == ["SECONDARY_GITHUB_TOKEN"]


def test_pair_extraordinaire_reports_the_coauthor_login_as_missing():
    missing = _settings().missing(find_badge("pair-extraordinaire").requires)
    assert missing == ["COAUTHOR_USERNAME"]


def test_a_filled_in_setting_stops_being_reported_as_missing():
    settings = _settings(secondary_github_token="other", coauthor_username="octocat")
    for badge in BADGES:
        assert settings.missing(badge.requires) == []


def test_template_titles_are_unique_past_one_full_cycle():
    count = len(QA_TEMPLATES) * 3
    titles = [template_for(index)[0] for index in range(count)]
    assert len(set(titles)) == count


def test_estimate_counts_every_write_request_not_just_the_unit():
    # A pull request is five writes, an accepted answer is three.
    assert estimate_seconds(find_badge("pull-shark"), 10, 8.0) == 400.0
    assert estimate_seconds(find_badge("galaxy-brain"), 10, 8.0) == 240.0


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/rahfianugerah/commitwave.git",
        "https://github.com/rahfianugerah/commitwave",
        "git@github.com:rahfianugerah/commitwave.git",
        "ssh://git@github.com/rahfianugerah/commitwave/",
    ],
)
def test_parse_remote_reads_every_github_url_form(url):
    assert parse_remote(url) == "rahfianugerah/commitwave"


def test_parse_remote_ignores_a_remote_that_is_not_github():
    assert parse_remote("https://gitlab.com/owner/name.git") is None
