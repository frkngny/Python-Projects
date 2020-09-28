import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email


host = 'imap.gmail.com'
# TODO: change 'username' and 'password'
username = 'YOUR_MAIL_ADDRESS'
password = 'YOUR_MAIL_PASSWORD'

blank_mail = {'From': 'Oops!!', 'To': '-', 'Subject': 'Oops!!', 'Date': '-', 'Body': 'There is no unseen mail left!!'}


def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select('inbox')

    _, search_data = mail.search(None, 'UNSEEN')

    counter = 0
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_msg = email.message_from_bytes(b)

        for header in ['From', 'To', 'Subject', 'Date']:
            email_data[header] = email_msg[header]

        for part in email_msg.walk():
            if part.get_content_type() == 'text/plain':
                email_data['Body'] = part.get_payload(decode=False)

        counter += 1
        if counter == 1:
            return email_data

    return blank_mail

# TODO: change 'from_email'. I put constant text and subject, you can also change those
def send_mail(text="Email body", subject="Hello World",
              from_email="YOUR_MAIL_ADDRESS", to_email=None):

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_email)
    msg['Subject'] = subject

    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    msg_str = msg.as_string()
    # login to smtp
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_email, msg_str)

    server.quit()