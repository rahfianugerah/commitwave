"""Terminal output and prompts. The only module that writes to stdout."""

from __future__ import annotations

import random
import sys
import time

HEADER = "Commit Wave: "
WRAP_AT = 95

# A Windows console defaults to cp1252, which cannot encode the banner's box drawing and
# raises rather than degrading. Replace unencodable characters so a terminal without the
# glyphs prints something instead of stopping the app on its first line.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BANNER = r"""
 ██████╗ ██████╗ ███╗   ███╗███╗   ███╗██╗████████╗    ██╗    ██╗ █████╗ ██╗   ██╗███████╗
██╔════╝██╔═══██╗████╗ ████║████╗ ████║██║╚══██╔══╝    ██║    ██║██╔══██╗██║   ██║██╔════╝
██║     ██║   ██║██╔████╔██║██╔████╔██║██║   ██║       ██║ █╗ ██║███████║██║   ██║█████╗
██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║       ██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║   ██║       ╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝        ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝
"""


def banner() -> None:
    print(BANNER)


def say(text: str, header: str = HEADER) -> None:
    """Print one character at a time, wrapping on a space near column 95."""
    sys.stdout.write(header)
    column = len(header)

    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(random.uniform(0.02, 0.04))
        column += 1
        if column >= WRAP_AT and character == " ":
            sys.stdout.write("\n" + " " * len(header))
            column = len(header)

    sys.stdout.write("\n")
    sys.stdout.flush()


def tell(text: str = "") -> None:
    """Print a line at once. Used for lists and tables the typewriter would make tedious."""
    print(text)


def ask(question: str) -> str:
    say(question)
    return input("  > ").strip()


def menu(title: str, options: list[str]) -> int:
    """Show a numbered list and return the zero-based index the reader picks."""
    say(title)
    for number, option in enumerate(options, start=1):
        tell(f"  {number}. {option}")

    while True:
        answer = input("  > ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        tell(f"  Enter a number between 1 and {len(options)}.")


def confirm(text: str) -> bool:
    """Ask for a typed yes. Anything else means no."""
    say(f"{text} Type yes to continue.")
    return input("  > ").strip().lower() == "yes"


def progress(done: int, total: int, label: str) -> None:
    """Rewrite a single progress line in place, then break the line when finished."""
    print(f"\r  [{done}/{total}] {label:<62}", end="", flush=True)
    if done >= total:
        print()
