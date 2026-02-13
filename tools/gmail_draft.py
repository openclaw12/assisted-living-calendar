"""Save a draft email in Gmail using IMAP with an app password."""

import argparse
from email.message import EmailMessage
import imaplib
import ssl
import time

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a Gmail draft via IMAP")
    parser.add_argument("--email", required=True)
    parser.add_argument("--app-password", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    return parser.parse_args()


def create_message(sender: str, to: str, subject: str, body: str) -> bytes:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return msg.as_bytes()


def save_draft(email: str, app_password: str, raw_message: bytes) -> None:
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context) as imap:
        imap.login(email, app_password)
        imap.append("[Gmail]/Drafts", "", imaplib.Time2Internaldate(time.time()), raw_message)
        imap.logout()


def main() -> None:
    args = parse_args()
    raw = create_message(args.email, args.to, args.subject, args.body)
    save_draft(args.email, args.app_password, raw)


if __name__ == "__main__":
    main()
