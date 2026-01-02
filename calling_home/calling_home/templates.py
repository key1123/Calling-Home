"""
Message templates for Calling Home.

These templates are designed for a compliance-friendly consent flow:
- The first message is an OPT-IN request.
- It includes clear YES/NO language.
- It avoids marketing claims, urgency, or misleading subject lines.

IMPORTANT:
This module generates text. It does NOT send messages or scrape contacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Audience = Literal["lawyer", "lawmaker"]
Channel = Literal["sms", "email"]


@dataclass(frozen=True)
class MessageContext:
    """
    Context for building the opt-in message.

    sender_name: name of the human / org sending the request
    city/state: used to localize the message
    audience: lawyer vs lawmaker (slight tone differences)
    channel: sms vs email (format differences)
    """
    sender_name: str
    city: str
    state: str
    audience: Audience
    channel: Channel


def location_string(city: str, state: str) -> str:
    """Format a location string safely."""
    loc = f"{city}, {state}".strip().strip(",")
    return loc


def build_opt_in_message(ctx: MessageContext) -> str:
    """
    Build an OPT-IN message.

    - SMS: short and direct.
    - Email: includes a subject + body.

    NOTE: For email compliance (CAN-SPAM), the strict requirements apply to
    *commercial* messages. This is an opt-in request (non-promotional) by default.
    If you later send promotional emails, you must include required elements
    (valid physical address, unsubscribe mechanism, etc.).
    """
    loc = location_string(ctx.city, ctx.state)

    if ctx.channel == "sms":
        # TCPA considerations:
        # - Request permission before sending follow-ups.
        # - Include clear opt-out path (NO).
        if ctx.audience == "lawyer":
            return (
                f"Hello, this is {ctx.sender_name}. I have a brief professional inquiry relevant to {loc}. "
                "May I have your permission to send one short follow-up message by text or email? "
                "Reply YES to opt in or NO to decline. Thank you."
            )
        else:
            return (
                f"Hello, this is {ctx.sender_name}. I’m reaching out with a brief civic/professional inquiry relevant to {loc}. "
                "May I send one short follow-up message? Reply YES to opt in or NO to decline. Thank you."
            )

    # Email format:
    if ctx.audience == "lawyer":
        subject = "Permission Request – One Brief Message"
        body = (
            f"Hello,\n\n"
            f"My name is {ctx.sender_name}, and I’m reaching out with a brief professional inquiry relevant to {loc}.\n\n"
            f"Before I share details, may I have your permission to send one short follow-up message by email?\n\n"
            f"Reply YES to opt in, or reply NO to decline (and I will not follow up).\n\n"
            f"Respectfully,\n{ctx.sender_name}\n"
        )
    else:
        subject = "Quick Opt-In Request"
        body = (
            f"Hello,\n\n"
            f"My name is {ctx.sender_name}. I’m reaching out with a brief civic/professional inquiry relevant to your role in {loc}.\n\n"
            f"Before sharing details, may I have your permission to send one short follow-up email?\n\n"
            f"Reply YES to opt in, or reply NO to decline (and I will not follow up).\n\n"
            f"Respectfully,\n{ctx.sender_name}\n"
        )

    return f"SUBJECT: {subject}\n\n{body}"
