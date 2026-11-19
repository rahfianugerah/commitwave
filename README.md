# Commit Wave

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0-ECD53F?logo=dotenv&logoColor=black)
![Git](https://img.shields.io/badge/Git-2.55-F05032?logo=git&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub_API-2022--11--28-181717?logo=github&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-0.16-D7FF64?logo=ruff&logoColor=black)
![pytest](https://img.shields.io/badge/pytest-9.1-0A9EDC?logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-MIT-750014)

<img src="img/bot.png" alt="Commit Wave" width="120">

Commit Wave is a terminal app that fills a GitHub contribution graph with backdated commits and works towards three GitHub achievement badges by opening and merging pull requests or by posting and accepting discussion answers. **It writes only to repositories you own, and every badge run asks you to type `yes` before it creates anything.**

It exists for learning and experiment: GitHub documents neither how the contribution graph counts backdated work nor what earns an achievement, and this is a way to find out on a repository of your own.

## Table of Contents

1. [Setup](#setup)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Data](#data)
5. [Project Structure](#project-structure)
6. [Development](#development)
7. [Known Limitations](#known-limitations)
8. [License](#license)

## Setup

Nothing is done on a fresh clone. A returning reader with `.env` already filled in starts at [Usage](#usage).

**1. Repository.** Fork the repository on GitHub, then clone your fork.

```bash
git clone https://github.com/<your-login>/commitwave.git
cd commitwave
```

**The wave mode pushes to this checkout's own `origin` remote.** A clone of someone else's repository makes every commit locally and then stops at the push with `Git stopped: remote: Permission to <owner>/commitwave.git denied to <your-login>.` Forking first gives you a remote you can push to.

**2. Environment.** Any Python 3.10 or newer. Substitute your own Conda environment name for `general`.

```bash
conda activate general
pip install -r requirements.txt
```

Or use a virtual environment instead:

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS and Linux: source .venv/bin/activate
pip install -r requirements.txt
```

**3. Configuration.** Copy the template and fill it in by hand.

```bash
copy .env.example .env          # macOS and Linux: cp .env.example .env
```

The Contribution Wave mode needs nothing in `.env`. Every Badge Farm mode needs `GITHUB_TOKEN`, and two of them need a second account as well; [Configuration](#configuration) lists every name.

## Usage

```bash
python main.py
```

### One Menu, Four Choices

```text
Commit Wave: Hello. I am your commit bot.
Commit Wave: What would you like to do?
  1. Contribution Wave, backdated commits across a date range
  2. Badge Farm, work towards a GitHub achievement
  3. Status, what each badge stands at
  4. Quit
  > 1
Commit Wave: Please enter the start date (YYYY-MM-DD):
  > 2025-08-01
Commit Wave: Please enter the end date (YYYY-MM-DD):
  > 2025-08-02
Commit Wave: How many commits would you like to make?
  > 3
Commit Wave: Making 3 commits. This repository is the one that receives them.
  [3/3] Sat Aug 02 14:09:41 UTC 2025
Commit Wave: All commits are done and pushed to the remote.
```

**Run it from the repository's own directory.** The wave mode commits on the branch that is checked out and pushes that branch once at the end, so run it on `main` only if `main` is where you want the commits. Badge Farm writes to `GITHUB_REPO` instead, or to the `origin` remote of this directory when that variable is unset.

### Three Badges, Three Tiers Each

| Badge | Bronze, x2 | Silver, x3 | Gold, x4 | Unit | Accounts |
| :- | -: | -: | -: | :- | :- |
| Pull Shark | 16 | 128 | 1024 | Merged pull requests | One |
| Galaxy Brain | 8 | 16 | 32 | Accepted answers | Two |
| Pair Extraordinaire | 10 | 24 | 48 | Co-authored merged pull requests | Two |

Pick the badge, then the tier. Commit Wave reads how far along you already are, tells you how many units are left and roughly how long they take, and asks you to type `yes` before it writes anything.

```text
  > 2
Commit Wave: Which badge?
  1. Pull Shark           merged pull requests (Bronze 16, Silver 128, Gold 1024)
  2. Galaxy Brain         accepted answers (Bronze 8, Silver 16, Gold 32)
  3. Pair Extraordinaire  co-authored merged pull requests (Bronze 10, Silver 24, Gold 48)
  > 1
Commit Wave: One account is enough. Each unit opens a pull request and merges it.
Commit Wave: Which tier?
  1. x2 Bronze  16 merged pull requests
  2. x3 Silver  128 merged pull requests
  3. x4 Gold    1024 merged pull requests
  > 1
Commit Wave: You stand at 4 of 16. Reaching Pull Shark x2 Bronze means creating 12 more merged
             pull requests in rahfianugerah/commitwave, which takes about 8 minutes at the
             current request delay.
Commit Wave: This writes to that repository and cannot be undone in bulk. Type yes to continue.
  > yes
  [12/12] merged pull request #37
Commit Wave: Created 12 merged pull requests. GitHub awards achievements on its own schedule,
             so give your profile a day or two.
```

### A Missing Setting Stops the Run Before It Starts

Galaxy Brain and Pair Extraordinaire each need a second GitHub account. Commit Wave checks before it starts and names what is absent, rather than failing partway through a run.

```text
  > 2
Commit Wave: Which badge?
  > 2
Commit Wave: Two GitHub accounts. The second account asks the question and marks your reply as
             the answer, because marking your own answer does not count.
Commit Wave: Which tier?
  > 1
Commit Wave: Galaxy Brain needs settings this project does not have yet.
  Missing in .env: GITHUB_TOKEN, SECONDARY_GITHUB_TOKEN
  Copy .env.example to .env and fill those names in.
  SECONDARY_GITHUB_TOKEN is a token from a different GitHub account.
```

### What Each Badge Needs From You

- **Pull Shark.** One account. `GITHUB_TOKEN` needs the classic `public_repo` scope, or a fine-grained token scoped to the target repository with Contents and Pull requests set to read and write.
- **Pair Extraordinaire.** Two accounts, but only one token. Set `COAUTHOR_USERNAME` to the second account's login. Commit Wave reads that account's numeric id from the API and builds the `Co-authored-by` address itself, because a hand-typed address produces a commit that looks co-authored and counts for nothing.
- **Galaxy Brain.** Two accounts and two tokens, both needing Discussions write access. The second account asks the question and marks your reply as the answer. Marking your own answer does not earn the badge. Discussions must already be on for the repository, with an answerable question and answer category, because GitHub has no API to create one.

To change the question and answer text, edit `QA_TEMPLATES` in `commitwave/farm.py`. It ships with placeholder text.

### Running on a Schedule Instead

Commit Wave is interactive, so it does not run itself. To keep a graph active without a machine being on, this workflow does the same job from GitHub Actions. It is not installed here. Copy it to `.github/workflows/commitwave.yml` if you want it, and set the two git config values to your own.

```yaml
name: Commit Wave

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up git
        run: |
          git config user.name 'username'
          git config user.email 'youremail@email.com'

      - name: Pick a commit count
        id: random
        run: echo "count=$(shuf -i 1-2 -n 1)" >> "$GITHUB_OUTPUT"

      - name: Make commits
        run: |
          for ((i = 0; i < ${{ steps.random.outputs.count }}; i++)); do
            date >> commit.txt
            git add commit.txt
            git commit -m "chore: scheduled commit at $(date -u +%FT%TZ)"
          done
          git push
```

`cron: '0 0 * * *'` runs at midnight UTC daily. `cron: '0 */6 * * *'` runs every six hours. GitHub delays scheduled workflows under load, so the times are approximate.

## Configuration

Every variable the app reads. Names only. Real values belong in `.env`, which is gitignored.

| Variable | Required | Description |
| :- | :- | :- |
| `GITHUB_TOKEN` | For Badge Farm | Token for the account that earns the badge |
| `GITHUB_REPO` | No | Target repository as `owner/name`. Defaults to the `origin` remote |
| `SECONDARY_GITHUB_TOKEN` | For Galaxy Brain | Token for the second account, which asks and accepts |
| `COAUTHOR_USERNAME` | For Pair Extraordinaire | Login of the second account named as co-author |
| `REQUEST_DELAY` | No | Seconds between GitHub write requests. Defaults to `8.0` |

`REQUEST_DELAY` is the calibration knob. GitHub allows roughly 500 content-generating requests per hour, one pull request costs five of them, and those figures are described as general rather than exact. Raise the delay if you see rate limit errors.

## Data

Commit Wave reads no dataset. Everything under `data/` is written by the app itself, and only `temp.txt` is committed.

| Item | Location | Notes |
| :- | :- | :- |
| Wave content | `data/temp.txt` | Committed. Every wave commit rewrites it with that commit's timestamp |
| Wave log | `data/commit.txt` | Gitignored. One line appended per wave commit |
| Badge ledger | `data/progress.json` | Gitignored. Units created per badge, so a rerun resumes where the last one stopped |

## Project Structure

```text
main.py                # entrypoint and menu
commitwave/
  config.py            # every setting, read once into a frozen object
  tui.py               # banner, typewriter output, prompts
  git.py               # git commands, run without a shell
  wave.py              # backdated commits across a date range
  github.py            # REST and GraphQL over urllib
  farm.py              # badge tiers, progress ledger, the three runners
tests/
data/                  # see Data
```

## Development

`pytest` and `ruff` are not in `requirements.txt`, so install them once into the same environment.

```bash
pip install pytest ruff
ruff check .          # lint
ruff format .         # format
pytest                # tests
```

The tests touch no network. They cover the date arithmetic and the badge tier logic, which are the parts that can be wrong without an API call telling you.

## Known Limitations

- **Commit Wave cannot confirm a badge.** GitHub publishes no achievements API, in REST or in GraphQL. The app counts what it created and nothing more. Check your profile after a day or two.
- **Pair Extraordinaire has no live count.** GitHub has no co-author search qualifier, so that badge reads from `data/progress.json` alone. Delete that file and the count restarts at zero. Pull Shark and Galaxy Brain are read from GitHub itself and stay accurate.
- **Achievement rules are undocumented.** GitHub documents no thresholds and no eligibility rules; the numbers in the badge table are community-maintained and could change without notice. Run the Bronze tier first and confirm the badge arrives before spending longer.
- **Gold Pull Shark is 1024 pull requests.** At the default delay that is roughly eleven hours of continuous running. Interrupting it is safe, and rerunning carries on from the ledger.
- **A rate limit stops the run.** Commit Wave honours GitHub's backoff headers and tries each request five times, then stops with the reason. Continuing to call a limited endpoint can get an account banned, so it does not push past that.
- **The wave mode commits to this checkout only.** It has no target option, and it pushes once at the end using whatever git credentials the machine already has.
- **GitHub treats badge farming as inauthentic activity.** GitHub staff have publicly described coordinated badge farming, self-marked answers in particular, as inauthentic, and disabled achievements in GitHub Community Discussions in 2024 because of it. The enforcement is undocumented, and the risk of using this is yours. Keep it to one repository of your own, and do not use it to misrepresent project progress or to inflate activity somewhere it will mislead people.

## License

MIT. See [LICENSE](LICENSE).

Author: [@rahfianugerah](https://github.com/rahfianugerah)
