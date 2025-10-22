import streamlit as st
import smtplib
from email.message import EmailMessage
from typing import Tuple


def send_email_smtp(recipient_email: str, subject: str, email_body: str, sender_name: str) -> Tuple[bool, str]:
    """
    Send an email using Gmail's SMTP server (smtp.gmail.com) over TLS.

    Parameters:
    - recipient_email: The recipient's email address (str).
    - subject: The subject line for the email (str).
    - email_body: The plain-text body of the email (str).
    - sender_name: The display name to show as the sender (str).

    The function reads SMTP credentials from Streamlit secrets:
    - st.secrets["SENDER_EMAIL"]: The Gmail address used to send emails.
    - st.secrets["EMAIL_PASSWORD"]: The Gmail App Password (recommended) or account password.

    Returns:
    - (success: bool, message: str): A tuple where `success` is True on successful send,
      otherwise False; `message` contains information or the error string.

    Notes:
    - This function uses smtp.gmail.com on port 587 with STARTTLS.
    - For Gmail accounts, it is strongly recommended to enable 2FA and create an
      App Password for EMAIL_PASSWORD. Plain account passwords may not work.

    Example:
        success, msg = send_email_smtp(
            "recipient@example.com",
            "Hello from Streamlit",
            "This is the email body.",
            "Your App Name",
        )
    """
    try:
        # Retrieve credentials from Streamlit secrets
        sender_email = st.secrets.get("SENDER_EMAIL")
        sender_password = st.secrets.get("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            return (False, "Missing email credentials in st.secrets. Please set SENDER_EMAIL and EMAIL_PASSWORD.")

        # Compose the email
        msg = EmailMessage()
        msg["From"] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject or ""
        msg.set_content(email_body or "")

        # Connect to Gmail SMTP server with TLS
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return (True, "Email sent successfully.")

    except smtplib.SMTPAuthenticationError as auth_err:
        return (False, f"Authentication failed: {auth_err}")
    except smtplib.SMTPRecipientsRefused as r_err:
        return (False, f"Recipient refused: {r_err}")
    except smtplib.SMTPException as smtp_err:
        return (False, f"SMTP error occurred: {smtp_err}")
    except Exception as e:
        return (False, f"Unexpected error: {e}")

# Keep existing helper functions (if any) below or import them from elsewhere in the project.
from LLM_Help import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 7 lines"
    elif length == "Medium":
        return "6 to 12 lines" 
    elif length == "Long":
        return "11 to 20 lines"
    else:
        return "6 to 10 lines"

def generate_email(length, language, tag, writer_name="Your Name", email_subject=None):
    prompt = get_prompt(length, language, tag, writer_name, email_subject)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag, writer_name, email_subject):
    length_str = get_length_str(length)
    subject_text = email_subject if email_subject else f"Regarding {tag}"
    examples = few_shot.get_filtered_examples(length, language, tag)

    # Build prompt with description and date included in examples
    prompt = f'''
Generate a professional email containing a subject, greeting, body, polite closing, and signature including the writer's name.

Topic: {tag}
Length: {length_str}
Language: {language}
Subject: {subject_text}
Writer's Name: {writer_name}

'''

    if examples:
        prompt += "Here are some example emails to follow:\n"
        for i, ex in enumerate(examples[:2]):  # Use up to 2 examples
            prompt += f"\nExample {i+1}:\n"
            prompt += f"Description: {ex['description']}\n" if ex['description'] else ""
            prompt += f"Date: {ex['date']}\n" if ex['date'] else ""
            prompt += f"Subject: {ex['subject']}\n"
            prompt += f"Greeting: {ex['greeting']}\n"
            prompt += f"Body:\n{ex['body']}\n"
            prompt += f"Closing: {ex['closing']}\n"
            prompt += f"Signature: {ex['signature']}\n"

    prompt += f"\nPlease write an email consistent with the above details and examples. Include \"{writer_name}\" in the signature."

    return prompt


if __name__ == "__main__":
    print(generate_email("Medium", "English", "Job Search", "Alice", "Application Follow-Up"))
