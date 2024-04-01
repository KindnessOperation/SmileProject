import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ImapToSMS:
    def __init__(self, smtpServer, email, pwd) -> None:
        self.smtpServer = smtpServer
        self.email = email
        self.pwd = pwd
        self.SMTP_PORT = 587

    def send_message(self, content: str, email: str) -> None:
        """ Sends a message with IMAP - Used to send messages over SMS
        
        Parameters:
        (str)content: The content of the message
        (str)email: The email to send the message to
        
        """

        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = email
        message['Subject'] = 'Hi helo'

        message.attach(MIMEText(content, 'plain'))

        with smtplib.SMTP(
            self.smtpServer, self.SMTP_PORT
        ) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(self.email, self.pwd)
            smtp.sendmail(self.email, email, message.as_string())


    if __name__ == "__main__":
        send_message("hi how is ur day", "4076860266@tmomail.net")