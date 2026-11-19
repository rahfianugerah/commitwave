# Security Policy

Commit Wave holds GitHub tokens that can write to your repositories, so a flaw in how it handles them matters more than its size suggests. **Report a vulnerability privately, never in a public issue**, so it can be fixed before anyone else learns of it.

## Supported Versions

Only `main`, the Python version, receives security fixes. The older JavaScript versions are kept as archive branches and are not maintained.

| Version | Branch | Supported |
| :- | :- | :- |
| 3.x, Python | `main` | <code style="color: green">Supported</code> |
| 2.0.1, JavaScript | `v2.0.1` | <code style="color: red">Not Supported</code> |
| 1.0.1, JavaScript | `v1.0.1` | <code style="color: red">Not Supported</code> |

## Report a Vulnerability Privately, Not in an Issue

Open the repository's **Security** tab and choose **Report a vulnerability**. The report stays private between you and the maintainer until a fix is published.

Include:

- What an attacker could do, and to whose account or repository.
- The steps that reproduce it, against a repository of your own.
- The version or commit you tested.

Never include a real token in a report. Replace it with `ghp_EXAMPLE` and describe where it would appear.

You will get a reply in the private advisory thread. When a fix lands, the advisory is published with credit to you, unless you ask to stay anonymous.

## What Counts as a Vulnerability

- A token written to a log, a file, a commit, terminal output, or an error message.
- A token sent anywhere other than `https://api.github.com`.
- Input from a prompt, a setting, or an API response that is run as a shell command.
- A run that writes to a repository other than the target it showed before you typed `yes`.

## What Does Not

- GitHub's achievement rules, or GitHub acting against an account that used this tool. That is the risk the README describes, not a flaw in the code.
- A token you committed or shared yourself. Revoke it on GitHub at once; there is nothing to report here.
- GitHub rate limiting a run. The app stops on purpose when that happens.
