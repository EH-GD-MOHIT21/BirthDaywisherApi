from django.conf import settings
from email.message import EmailMessage
import smtplib

def send_mail(to,subject=None,message=None,not_bulk=True,password=None):
    sender_mail = settings.EMAIL_SENDER   
    password_sender = settings.EMAIL_PASS

    messageEX = EmailMessage()
    if not_bulk:
        messageEX['To'] = to
    else:
        messageEX['Bcc'] = to
    messageEX['From'] = sender_mail
    if subject == None:
        messageEX['Subject'] = "Welcome User to Nested.com"
    else:
        messageEX['Subject'] = subject
    if message == None:
        messageEX.set_content(f"Hello User welcome to Nested.com Your password is {password}. \n \n \n You are not allowed to change this again.\n \n \n Regards\n Nested.com")
    else:
        messageEX.set_content(message)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_mail, password_sender)
        server.send_message(messageEX)
        return True
    except Exception as e:
        return False