import ssl
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG = None
with open("./config.json", "r") as f:
    CONFIG = json.load(f)

def send_message(content: str, email: str) -> None:
    """ Sends a message with IMAP - Used to send messages over SMS
    
    Parameters:
    (str)content: The content of the message
    (str)email: The email to send the message to
    
    """
    acc = CONFIG['email']
    SMTP_SERVER, SMTP_PORT = acc['smtpServer'], 587
    sender_email, sender_passowrd = acc['email'], acc['password']

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Hi helo'

    message.attach(MIMEText(content, 'plain'))

    with smtplib.SMTP(
        SMTP_SERVER, SMTP_PORT
    ) as smtp:
        smtp.ehlo()
        smtp.starttls(context=ssl.create_default_context())
        smtp.ehlo()
        smtp.login(sender_email, sender_passowrd)
        smtp.sendmail(sender_email, email, message.as_string())


if __name__ == "__main__":
    send_message("hi how is ur day", "4076860266@tmomail.net")