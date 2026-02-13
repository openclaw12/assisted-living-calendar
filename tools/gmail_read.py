"""Read emails from Gmail via IMAP."""

import argparse
import email
import imaplib
import ssl
from email.message import Message
from typing import List, Tuple

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read Gmail via IMAP")
    parser.add_argument("--email", required=True)
    parser.add_argument("--app-password", required=True)
    parser.add_argument("--mailbox", default="INBOX")
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args()


def fetch_recent(mailbox: str, limit: int, imap: imaplib.IMAP4_SSL) -> List[Tuple[str, Message]]:
    imap.select(mailbox)
    status, data = imap.search(None, "ALL")
    if status != "OK" or not data or not data[0]:
        return []

    ids = data[0].split()
    recent_ids = ids[-limit:]
    results = []
    for msg_id in reversed(recent_ids):
        status, msg_data = imap.fetch(msg_id, "(RFC822)")
        if status != "OK" or not msg_data:
            continue
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        results.append((msg_id.decode(), msg))
    return results


def show_summary(messages: List[Tuple[str, Message]]) -> None:
    for msg_id, msg in messages:
        subject = msg.get("Subject", "(no subject)")
        sender = msg.get("From", "(unknown)")
        print(f"ID: {msg_id}\nFrom: {sender}\nSubject: {subject}\n")


def main() -> None:
    args = parse_args()
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context) as imap:
        imap.login(args.email, args.app_password)
        messages = fetch_recent(args.mailbox, args.limit, imap)
        show_summary(messages)
        imap.logout()


if __name__ == "__main__":
    main()
