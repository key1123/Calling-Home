"""
UI helpers for Calling Home (console app).

- Provides a consistent red/white/blue theme.
- Provides banner, menus, and message display boxes.
- Designed to work even if colorama is not installed (falls back to plain text).
"""

from __future__ import annotations

import os

# Optional dependency for Windows-friendly ANSI colors.
try:
    from colorama import init as colorama_init
    from colorama import Fore, Style

    colorama_init(autoreset=True)
except Exception:  # pragma: no cover
    # Minimal fallback so app still runs without colorama.
    class _Fore:
        RED = BLUE = WHITE = ""

    class _Style:
        BRIGHT = RESET_ALL = ""

    Fore = _Fore()
    Style = _Style()


APP_NAME = "Calling Home"


def clear_screen() -> None:
    """Clear the terminal screen on Windows/macOS/Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def banner() -> None:
    """Print a simple red/white/blue banner."""
    print(Style.BRIGHT + Fore.RED + "╔" + "═" * 58 + "╗")
    print(Style.BRIGHT + Fore.WHITE + "║" + Fore.BLUE + f"{APP_NAME:^58}" + Fore.WHITE + "║")
    print(Style.BRIGHT + Fore.RED + "╚" + "═" * 58 + "╝" + Style.RESET_ALL)


def prompt_nonempty(label: str, default: str | None = None) -> str:
    """
    Prompt until the user provides a non-empty string.
    If `default` is provided, ENTER uses the default.
    """
    while True:
        if default:
            raw = input(Fore.WHITE + f"{label} " + Fore.BLUE + f"[{default}]" + Fore.WHITE + ": ").strip()
            val = raw or default
        else:
            val = input(Fore.WHITE + f"{label}: ").strip()

        if val:
            return val

        print(Fore.RED + "Please enter a value.")


def choose(label: str, options: list[str], default_index: int = 0) -> str:
    """
    Present a numbered choice list and return the selected option string.

    Example:
        choose("Audience:", ["lawyer", "lawmaker"]) -> "lawyer"
    """
    print(Fore.WHITE + label)
    for i, opt in enumerate(options, start=1):
        color = Fore.BLUE if i - 1 == default_index else Fore.WHITE
        print(color + f"  {i}) {opt}")

    while True:
        raw = input(
            Fore.WHITE + f"Choose 1-{len(options)} " + Fore.BLUE + f"[{default_index + 1}]" + Fore.WHITE + ": "
        ).strip()

        if not raw:
            return options[default_index]

        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= len(options):
                return options[n - 1]

        print(Fore.RED + "Invalid choice.")


def print_message_box(msg: str, max_width: int = 90) -> None:
    """
    Print a bordered message box with basic wrapping.
    Keeps formatting readable for both SMS (single paragraph) and email (multi-line).
    """
    lines = msg.splitlines() if msg else [""]
    width = min(max(len(line) for line in lines) + 4, max_width)

    print(Fore.RED + "┌" + "─" * (width - 2) + "┐")
    for line in lines:
        # Naive wrapping so long lines don't break the box.
        while len(line) > width - 4:
            chunk, line = line[: width - 4], line[width - 4 :]
            print(Fore.WHITE + "│ " + Fore.BLUE + chunk.ljust(width - 4) + Fore.WHITE + " │")

        print(Fore.WHITE + "│ " + Fore.BLUE + line.ljust(width - 4) + Fore.WHITE + " │")
    print(Fore.RED + "└" + "─" * (width - 2) + "┘")
