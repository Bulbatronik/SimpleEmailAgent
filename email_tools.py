"""
Email connection and tool functions for listing and summarizing emails.
"""
import json
from imap_tools import MailBox, AND
from langchain.tools import tool
from config import IMAP_HOST, IMAP_USER, IMAP_PASSWORD, IMAP_FOLDER


def connect():
    mail_box = MailBox(IMAP_HOST)
    mail_box.login(IMAP_USER, IMAP_PASSWORD, initial_folder=IMAP_FOLDER)
    return mail_box


@tool   
def list_unread_email():
    """Returns a bulleted list of EVERY UNREAD message's UID, subject, data and sender."""
    print("Listing Unread Emails Tool Called")
    try:
        with connect() as mailbox:
            unread_emails = list(mailbox.fetch(criteria=AND(seen=False), headers=True, mark_seen=False))
    except Exception as e:
        print(f"Error connecting to mailbox: {e}")
        return None
        #return f"Error connecting to mailbox: {e}"
    if not unread_emails:
        return "No unread emails found."
    response = json.dumps([
        {
            'uid': email.uid,
            'date': email.date.astimezone().strftime('%Y-%m-%d %H:%M'),
            'subject': email.subject,
            'from': email.from_,
        } for email in unread_emails
    ], indent=2, ensure_ascii=False)
    print(f"Found {len(unread_emails)} unread emails.")
    return response


def summarize_email_factory(raw_llm):
    @tool
    def summarize_email(uid):
        """Summarizes a single email given it's IMAP UID. Returns a short summary of the email content / body in the plain text."""
        print(f"Summarize Email Tool Called on {uid}")
        try:
            with connect() as mailbox:
                email = mailbox.fetch(criteria=AND(uid=uid), mark_seen=False)
                email = next(email, None)
        except Exception as e:
            return f"Error connecting to mailbox: {e}"
        if not email:
            return f"Could not summarize email with UID {uid}. It may not exist or is already read."
        prompt = (
            f"Summarize concisely the following email:\n\n"
            f"Subject: {email.subject}\n"
            f"From: {email.from_}\n"
            f"Date: {email.date.astimezone().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"{email.text or email.html}"
        )
        return raw_llm.invoke(prompt).content
    return summarize_email
