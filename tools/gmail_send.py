"""Send email via Gmail SMTP using an app password."""

import argparse
import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send Gmail via SMTP")
    parser.add_argument("--email", required=True)
    parser.add_argument("--app-password", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    return parser.parse_args()


def create_message(sender: str, to: str, subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


def send_email(email: str, app_password: str, message: EmailMessage) -> None:
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(email, app_password)
        smtp.send_message(message)


def main() -> None:
    args = parse_args()
    msg = create_message(args.email, args.to, args.subject, args.body)
    send_email(args.email, args.app_password, msg)


if __name__ == "__main__":
    main()
