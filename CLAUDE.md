# Commit Wave

A terminal app that fills a GitHub contribution graph and automates three GitHub achievement badges.

@README.md
@../docs/memory/memory.rules.md

## Rules Come From the Vault, Not From Here

`../docs/rules/` is the human-authored control plane and it wins on conflict with
anything inferred from this code. The ones this project is held to are `codes.rules.md`,
`docs.rules.md`, `badge.rules.md`, `env.rules.md`, `secret.rules.md`, `commit.rules.md`, and
`branch.rules.md`.

Two of them are broken by accident more often than the rest:

- **No tool or AI attribution.** `commit.rules.md` forbids a `Co-authored-by` naming an AI, a
  generated-with line, a model name, or any watermark, in a commit message or a pull request.
  This overrides the default trailer an agent adds. The human `Co-authored-by` trailers that
  `commitwave/farm.py` writes into GitHub commits are a different thing and are correct.
- **Never read a real environment file.** `env.rules.md` allows `.env.example` and forbids
  `.env`, including a command whose only purpose is checking that it exists. Test for the path.

## Things This Repository Would Otherwise Trip You On

- **`data/temp.txt` is tracked on purpose** while the rest of `data/` is ignored. The wave mode
  works by changing that file's content on every commit. See the negations in `.gitignore`.
- **`print` belongs in `tui.py` and `main.py` only.** `codes.rules.md` bans it in library code.
  Those two are the presentation layer of a terminal app, so they are the exception. Every
  other module returns a value or raises.
- **`config.py` is the only module that reads the environment.** Settings load once into a
  frozen dataclass. Do not scatter `os.getenv`.
- **The badge thresholds are community-sourced.** GitHub documents no achievement rules and
  publishes no achievements API. If a number in `farm.py` looks wrong, it is a constant to be
  corrected, not a bug to be worked around.
- **`github.py` takes an explicit token on every call.** Two badges act as two different
  accounts, and a shared client would hide which account is speaking.

## Development

```bash
ruff check .          # lint
ruff format .         # format
pytest                # tests, no network
```
