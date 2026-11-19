# PRD: Commit Wave

- **Owner:** Naufal Rahfi Anugerah ([@rahfianugerah](https://github.com/rahfianugerah))
- **Date:** 2026-11-19
- **Status:** Draft
- **Goal:** Let the owner observe how GitHub's contribution graph and achievements respond to activity, on a repository of their own, without creating that activity by hand.

## Table of Contents

1. [Problem](#problem)
2. [Users](#users)
3. [What Is Built](#what-is-built)
4. [What Is Not Built](#what-is-not-built)
5. [Success Measure](#success-measure)
6. [Constraints](#constraints)
7. [Data](#data)
8. [Open Questions](#open-questions)

## Problem

GitHub documents neither how backdated commits appear on the contribution graph nor what earns an achievement. The only way to find out is to create the activity and watch the profile. By hand, that means opening and merging up to 1024 pull requests, or having two accounts ask and accept up to 32 discussion answers, over many hours. Doing it by hand also fails quietly: a co-author address typed with one wrong character produces a commit that looks co-authored and counts for nothing, and nobody notices until the badge fails to arrive.

## Users

- **The owner, Naufal Rahfi Anugerah**, who runs it on their own repository, with a second GitHub account that is also theirs.
- **Anyone who forks the repository** to run the same experiment on a repository of their own. A fork is the only supported way to use it, because every run writes to the repository it targets.

## What Is Built

- **Backdated commits across a date range.** The user gives a start date, an end date, and a commit count. Each commit lands at a distinct random second inside that range, and the whole set is pushed once at the end.
- **Badge runs towards a chosen tier** for Pull Shark, Galaxy Brain, and Pair Extraordinaire. Before writing anything, a run reads where the account already stands, states how many units are left and roughly how long they take, and waits for the user to type `yes`.
- **A status view** showing where each badge stands against its three tiers.
- **Missing settings named up front.** A badge that needs a second account says which setting is absent before the run starts, not partway through it.
- **A run that survives interruption.** Progress is recorded after every unit, so rerunning carries on from where the last run stopped.
- **A run that stops at a rate limit.** It waits as GitHub instructs, tries each request five times, and then stops with the reason rather than pushing past the limit.

## What Is Not Built

- **No confirmation that a badge was awarded.** GitHub has no achievements API, so the app counts what it created and leaves the profile to the user.
- **No scheduler or background service.** The app is interactive and runs only while someone is at the terminal. A scheduled GitHub Actions workflow is documented in the README for anyone who wants one, and is not installed.
- **No target option for the backdated commits.** They go to the repository the app runs from, and nowhere else.
- **No achievements beyond the three.** Other achievements are either one-off or depend on other people, so there is nothing to automate.
- **No more than two accounts.** Two is what the badges need, and more would turn an experiment into an account farm.
- **No pacing designed to make automated activity look human.** The delay between writes exists to stay under GitHub's rate limits and for no other reason.
- **No graphical interface.** A terminal prompt is enough for one user running an experiment.

## Success Measure

- **Each badge reaches the chosen tier within two days** of a run finishing, checked on the owner's profile. As of 2026-11-19, Pull Shark and Galaxy Brain show x4, and Pair Extraordinaire shows x2 after a run of 48 units finished that day.
- **A backdated run of N commits shows N contributions** on the chosen dates of the contribution graph after the push.
- **An interrupted run, rerun, ends at the target** and creates no units beyond it.

## Constraints

- **GitHub publishes no achievements API and no achievement rules.** Every tier threshold is community-sourced and may change without notice.
- **GitHub allows roughly 500 content-creating requests per hour.** One pull request costs five of them, which sets the pace of every badge run.
- **GitHub staff have described coordinated badge farming as inauthentic activity.** Runs are limited to repositories the user owns, and the risk to the account is the user's.
- **Galaxy Brain needs Discussions turned on** with an answerable question and answer category. GitHub has no API to create one, so the user sets it up by hand.
- **Marking your own answer does not count.** The second account has to ask the question and accept the answer.
- **Tokens never enter the repository.** They live in the user's local environment file only.

## Data

| Data | Direction | Where | Personal |
| :- | :- | :- | :- |
| GitHub tokens for one or two accounts | Read | The user's local environment file | Credentials, never committed or logged |
| The account's merged pull request and accepted answer counts | Read | GitHub | No |
| Backdated commits | Written | The repository the app runs from | No |
| Branches, files, pull requests, discussions, and comments | Written | The target repository on GitHub | No |
| Co-author trailers | Written | Commit messages in the target repository | Yes: the second account's login and its GitHub no-reply address, both public |
| Progress per badge, and a log of backdated timestamps | Written | `data/progress.json` and `data/commit.txt`, local and gitignored | No |

## Open Questions

- **Is 48 the real Gold threshold for Pair Extraordinaire?** A run of exactly 48 finished on 2026-11-19 with the profile at x2. The owner decides after watching the profile for two days whether the threshold in the code needs correcting.
- **Does Pair Extraordinaire count merged pull requests or co-authored commits?** Each unit is one of each today, so the two cannot be told apart yet. The owner decides whether this is worth testing.
- **Should the discussion text stay placeholder text?** The question and answer templates ship as lorem ipsum. The owner decides whether real content replaces it.
