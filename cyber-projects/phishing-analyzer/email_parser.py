import email

def parse_email(raw_email):
    msg = email.message_from_string(raw_email)
    return {
        "subject": msg["Subject"],
        "from": msg["From"],
        "to": msg["To"],
        "date": msg["Date"],
        "body": get_email_body(msg)
    }

def get_email_body(msg):
    if msg.is_multipart():
        return ''.join(part.get_payload(decode=True).decode() for part in msg.walk() if part.get_content_type() == 'text/plain')
    else:
        return msg.get_payload(decode=True).decode()