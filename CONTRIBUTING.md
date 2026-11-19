# Contributing

Thank you for helping. A change is welcome when it fits what [PRD.md](PRD.md) says is built. **Read its "What Is Not Built" section before starting**, because a pull request that adds something listed there will be closed however well it is written.

Taking part means following the [Code of Conduct](CODE_OF_CONDUCT.md). A security problem goes through [SECURITY.md](SECURITY.md), never through a public issue.

## Table of Contents

1. [Setup](#setup)
2. [Test Badge Runs on Your Fork, Never Here](#test-badge-runs-on-your-fork-never-here)
3. [Code Rules That Keep the App Safe](#code-rules-that-keep-the-app-safe)
4. [Checks That Must Pass](#checks-that-must-pass)
5. [Branches](#branches)
6. [Commit Messages](#commit-messages)
7. [Pull Requests](#pull-requests)

## Setup

Follow [Setup in the README](README.md#setup), then install the development tools into the same environment:

```bash
pip install pytest ruff
```

## Test Badge Runs on Your Fork, Never Here

**Set `GITHUB_REPO` to your fork, or leave it unset inside your fork's clone.** A badge run opens pull requests or discussions in whatever repository it targets, and a run against this repository fills it with units that have to be cleaned up by hand. Never paste a token into an issue, a pull request, or a log.

## Code Rules That Keep the App Safe

- **Only `tui.py` and `main.py` print.** Every other module returns a value or raises, so output stays in one place.
- **Only `config.py` reads the environment.** Settings load once into a frozen object. Do not call `os.getenv` anywhere else.
- **Every function in `github.py` takes the token as an argument.** Two badges act as two different accounts, and a shared client would hide which account is speaking.
- **Git runs as an argument list, never through a shell**, so no user input is ever parsed as a command.
- **Badge thresholds are constants in `farm.py`.** GitHub documents none of them, so a change to a threshold cites where the new number comes from.
- **Tests touch no network.** Anything that needs GitHub is kept out of `tests/`.

## Checks That Must Pass

```bash
ruff check .          # lint
ruff format .         # format, 100 character lines
pytest                # tests
```

Code runs on Python 3.10 or newer, so do not use a feature that needs a later version.

## Branches

Branch off `main` and name the branch `<type>/<description>`, using the same types as a commit message, for example `feat/python-rewrite-badge-farm` or `docs/readme-project-template`. One branch carries one concern.

## Commit Messages

Commits follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), with a body that lists each change.

```text
fix: run on Python 3.10 instead of requiring 3.12

- Replace datetime.UTC with timezone.utc, since the alias only exists from 3.11
- Lower requires-python and the Ruff target to 3.10, and match the README badge
- Show the conda activation in Setup, with the virtual environment as the alternative
- Exit cleanly when stdin ends, rather than raising EOFError out of the menu
```

- The subject is imperative, starts lowercase, has no trailing period, and stays within 72 characters.
- The body is required and is a flat `-` list, one item per change.
- One concern per commit. A change that fits two types is two commits.
- No emoji, and no tool, bot, or generated-with attribution.

## Pull Requests

The title follows the same form as a commit subject. The description carries these sections:

```markdown
## Summary

What the pull request does and why, in one or two sentences.

## Changes

- One item per change, starting with an imperative verb

## Results

What changed in behaviour, with real output where it helps.

## Test Plan

- The commands run, and what each one showed

## Related Issues

The issue it closes, or "None".
```

Keep a pull request to one concern. Two unrelated fixes are two pull requests.
