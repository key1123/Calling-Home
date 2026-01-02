"""
Compliance guardrails for Calling Home.

This app is a "message generator" — it does not scrape or send.
Still, we add guardrails to encourage compliant usage:

- Make user confirm they have a lawful basis to contact the recipient.
- Provide a quick checklist aligned to:
  - TCPA (SMS / automated texting in the U.S.)
  - CAN-SPAM (commercial email in the U.S.)
  - Common best practices (rate limiting, do-not-contact lists, logging)

These guardrails reduce risk, but they are NOT a substitute for legal advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Audience = Literal["lawyer", "lawmaker"]
Channel = Literal["sms", "email"]


@dataclass(frozen=True)
class ComplianceChecklist:
    """
    Stores human-readable checklist items shown in-app.
    """
    title: str
    items: list[str]


def checklist_for(channel: Channel) -> ComplianceChecklist:
    """
    Return a channel-specific checklist.
    Kept concise so users actually read it.
    """
    if channel == "sms":
        return ComplianceChecklist(
            title="SMS Consent Checklist (TCPA-aligned best practices)",
            items=[
                "You have a lawful reason to initiate contact (e.g., existing relationship, inbound request, or verified permission).",
                "You are NOT using an autodialer/robocall system to blast unsolicited messages.",
                "Your first message is an opt-in request (asks permission before follow-up).",
                "Your message includes clear decline language (reply NO) and you honor it.",
                "You keep a do-not-contact list and do not re-contact opted-out numbers.",
            ],
        )

    return ComplianceChecklist(
        title="Email Checklist (CAN-SPAM-aligned best practices)",
        items=[
            "You have a lawful basis to email (professional inquiry or opt-in request; avoid deceptive subjects).",
            "You use honest identification (who you are) and avoid misleading headers.",
            "If you later send marketing/promotional emails, include: physical mailing address + clear unsubscribe.",
            "You do not continue emailing after a NO/opt-out request.",
            "You keep basic logs of consent and outreach attempts for auditability.",
        ],
    )


def require_user_ack(prompt_fn=input) -> bool:
    """
    Ask user to acknowledge compliance basics before generating messages.

    This is not a legal gatekeeper, but it forces an explicit "I understand" step.
    """
    resp = prompt_fn("Type I AGREE to confirm you will use this tool in a compliant way: ").strip().upper()
    return resp == "I AGREE"
