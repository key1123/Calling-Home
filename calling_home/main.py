"""
Calling Home - main entrypoint.

What this program DOES:
- Lets user input city/state
- Lets user choose audience + channel
- Generates an opt-in message and displays it
- Allows rereading and saving message to a .txt file
- Uses red/white/blue console theme

What it DOES NOT do:
- No scraping
- No auto-emailing or auto-texting
- No contact harvesting

This keeps the app aligned with compliance requirements and platform policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from calling_home.ui import Fore, clear_screen, banner, prompt_nonempty, choose, print_message_box
from calling_home.templates import MessageContext, build_opt_in_message
from calling_home.compliance import checklist_for, require_user_ack


@dataclass
class Session:
    """In-memory session state for the CLI."""
    sender_name: str = "Your Name"
    city: str = ""
    state: str = ""
    audience: str = "lawyer"   # lawyer | lawmaker
    channel: str = "sms"       # sms | email
    last_message: str = ""
    acknowledged: bool = False


def save_message_to_file(city: str, state: str, message: str) -> str:
    """Save the last generated message to a timestamped text file."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city = "".join(c for c in city if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    safe_state = "".join(c for c in state if c.isalnum()).strip()
    filename = f"calling_home_{safe_city}_{safe_state}_{ts}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)
        f.write("\n")

    return filename


def show_checklist(session: Session) -> None:
    """Display compliance checklist for the selected channel."""
    clear_screen()
    banner()
    cl = checklist_for(session.channel)  # channel-specific
    print(Fore.WHITE + cl.title + "\n")
    for i, item in enumerate(cl.items, start=1):
        print(Fore.BLUE + f"  {i}. {item}")
    print()
    input(Fore.WHITE + "Press Enter to return to menu...")


def generate_message(session: Session) -> None:
    """Generate and display the opt-in message (with compliance acknowledgement)."""
    if not session.city or not session.state:
        print(Fore.RED + "Set city/state first (menu option 2).")
        input(Fore.WHITE + "Press Enter to continue...")
        return

    # Require acknowledgement at least once per session.
    if not session.acknowledged:
        clear_screen()
        banner()
        print(Fore.WHITE + "Before generating messages, please review the compliance checklist.\n")
        cl = checklist_for(session.channel)
        print(Fore.WHITE + cl.title + "\n")
        for i, item in enumerate(cl.items, start=1):
            print(Fore.BLUE + f"  {i}. {item}")

        print("\n" + Fore.WHITE + "This tool generates text only. You are responsible for compliant use.")
        print(Fore.WHITE + "If you do not agree, exit the app.\n")

        session.acknowledged = require_user_ack()
        if not session.acknowledged:
            print(Fore.RED + "Acknowledgement not provided. Message generation blocked.")
            input(Fore.WHITE + "Press Enter to continue...")
            return

    ctx = MessageContext(
        sender_name=session.sender_name,
        city=session.city,
        state=session.state,
        audience=session.audience,  # type: ignore
        channel=session.channel,    # type: ignore
    )
    session.last_message = build_opt_in_message(ctx)

    clear_screen()
    banner()
    print(Fore.WHITE + f"Generated opt-in message ({session.audience} / {session.channel}):\n")
    print_message_box(session.last_message)
    print()
    input(Fore.WHITE + "Press Enter to return to menu...")


def reread_message(session: Session) -> None:
    """Display the last generated message if one exists."""
    clear_screen()
    banner()
    if not session.last_message:
        print(Fore.RED + "No message yet. Generate one with option 6.")
    else:
        print(Fore.WHITE + "Last generated message:\n")
        print_message_box(session.last_message)
    print()
    input(Fore.WHITE + "Press Enter to return to menu...")


def main() -> None:
    """Main menu loop."""
    session = Session()

    while True:
        clear_screen()
        banner()

        print(Fore.WHITE + "Current settings:")
        loc = f"{session.city}, {session.state}".strip().strip(",")
        print(Fore.BLUE + f"  Sender:   {session.sender_name}")
        print(Fore.BLUE + f"  Location: {loc if loc else '(not set)'}")
        print(Fore.BLUE + f"  Audience: {session.audience}")
        print(Fore.BLUE + f"  Channel:  {session.channel}")
        print(Fore.BLUE + f"  Compliant-use acknowledged: {'YES' if session.acknowledged else 'NO'}")
        print()

        print(Fore.WHITE + "Menu:")
        print(Fore.BLUE + "  1) Set sender name")
        print(Fore.BLUE + "  2) Set city/state")
        print(Fore.BLUE + "  3) Choose audience (lawyer / lawmaker)")
        print(Fore.BLUE + "  4) Choose channel (sms / email)")
        print(Fore.BLUE + "  5) View compliance checklist")
        print(Fore.BLUE + "  6) Generate opt-in message")
        print(Fore.BLUE + "  7) Re-read last message")
        print(Fore.BLUE + "  8) Save last message to file")
        print(Fore.RED +  "  0) Exit")
        print()

        choice = input(Fore.WHITE + "Select: " + Fore.BLUE).strip()

        if choice == "0":
            print(Fore.WHITE + "Goodbye.")
            return

        if choice == "1":
            session.sender_name = prompt_nonempty("Enter sender name", default=session.sender_name)

        elif choice == "2":
            session.city = prompt_nonempty("Enter city", default=session.city or None)
            session.state = prompt_nonempty("Enter state (e.g., TX)", default=session.state or None)
            # Changing context resets acknowledgement so user re-accepts if needed
            session.acknowledged = False

        elif choice == "3":
            session.audience = choose("Audience:", ["lawyer", "lawmaker"], default_index=0)
            session.acknowledged = False

        elif choice == "4":
            session.channel = choose("Channel:", ["sms", "email"], default_index=0)
            session.acknowledged = False

        elif choice == "5":
            show_checklist(session)

        elif choice == "6":
            generate_message(session)

        elif choice == "7":
            reread_message(session)

        elif choice == "8":
            if not session.last_message:
                print(Fore.RED + "No message yet. Generate one with option 6.")
                input(Fore.WHITE + "Press Enter to continue...")
                continue
            path = save_message_to_file(session.city, session.state, session.last_message)
            print(Fore.WHITE + "Saved to: " + Fore.BLUE + path)
            input(Fore.WHITE + "Press Enter to continue...")

        else:
            print(Fore.RED + "Unknown option.")
            input(Fore.WHITE + "Press Enter to continue...")


if __name__ == "__main__":
    main()
