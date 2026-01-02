# Calling Home (red/white/blue CLI)

Calling Home is a small console app that generates **compliance-friendly opt-in messages**
for contacting professionals in a given **city/state**. It supports two audiences
(lawyers and lawmakers) and two channels (SMS and email).

## What it does
- Prompts for **city/state**
- Lets you choose **audience** (lawyer / lawmaker) and **channel** (sms / email)
- Generates an **opt-in** message (asks permission before any follow-up)
- Lets you **re-read** the last message
- Lets you **save** the message to a `.txt` file
- Shows a **red/white/blue** themed console UI

## What it does NOT do
- No scraping / harvesting contacts
- No automated emailing or texting
- No bulk outreach features

This is intentional: it helps keep the tool aligned with anti-spam and consent regulations.

## Compliance notes (high level)
This tool is designed around best practices aligned to common U.S. requirements:

### SMS (TCPA-aligned best practices)
- Ask permission before sending follow-ups
- Include a clear decline option (NO)
- Honor opt-outs and maintain a do-not-contact list
- Avoid automated bulk texting without verified consent

### Email (CAN-SPAM-aligned best practices)
- Avoid deceptive subject lines and headers
- If you later send **commercial/promotional** email, include:
  - a valid physical address
  - a clear unsubscribe mechanism
- Honor opt-outs

**Important:** This README is not legal advice. Validate requirements for your
exact use case and jurisdictions (especially state laws and sector rules).

## Install (dev)
```bash
pip install colorama
python -m calling_home.main
