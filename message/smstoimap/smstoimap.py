from imaplib import IMAP4_SSL
from email.header import decode_header
import email
from datetime import datetime
from typing import Generator
from typing import Union

class otp_imap():
    def __init__(self, server, email, pwd):
        self.mail = IMAP4_SSL(server)
        self.mail.login(email, pwd)

        self.mail.select("inbox")

    def getMail(self, forwarded_email: str, timestamp: int) -> Union[None,  Generator[str, None, None]]:
        """ Yields IMAP Emails 
        
        Parameters:
        (str)forwarded_email: The email to check
        (int)timestamp: Only messages sent after the timestmap are yielded

        Returns:
        (Union[None,  Generator[str, None, None]]): None if no messages were sent; Yields the message if one is sent
        
        """
        self.mail.noop() # Get new emails


        search_criteria = f"FROM {forwarded_email}"
        status, messages = self.mail.search(None, search_criteria)
        if (not messages[0]):
            return None
        email_ids = messages[0].split()
        for email_id in email_ids:
            status, msg_data = self.mail.fetch(email_id, "(BODY[])")
            raw_email = msg_data[-2][1]
            msg = email.message_from_bytes(raw_email)

            # Get timestamps
            sent_date = msg.get("Date")
            try:
                formatted_time = datetime.strptime(sent_date, "%a, %d %b %Y %H:%M:%S %z (%Z)")
            except:
                formatted_time = datetime.strptime(sent_date, "%a, %d %b %Y %H:%M:%S %Z")
            
            # Check if it was sent before timestamp
            if (formatted_time.timestamp() < timestamp):
                continue
            if msg.is_multipart():
                for part in msg.get_payload():
                    # Check if the part is text/plain
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        yield body
                        break  # Break the loop once we find the text/plain part
        return None
            

    def __del__(self):
        if (self.mail):
            self.mail.close()
            self.mail.logout()


if __name__ == "__main__": # Testing
    import json
    with open("./config.json") as f:
        acc = json.load(f)['email']
        imap = otp_imap(acc['server'], acc['imapServer'], acc['password'])
        import time
        while True:
            print(list(imap.getMail("+14076860266@tmomail.net", 0)))
            time.sleep(2)
        del imap
